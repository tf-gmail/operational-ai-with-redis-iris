from __future__ import annotations

import asyncio
import hashlib
import json
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from redis import Redis


DEFAULT_SYNC_SECONDS = 45
DEFAULT_CACHE_TTL_SECONDS = 900
DEFAULT_RDI_MAX_CUSTOMERS = 250
CUSTOMER_INDEX = "idx:customers"
TICKET_INDEX = "idx:tickets"
INCIDENT_INDEX = "idx:incidents"
INCIDENT_VECTOR_INDEX = "idx:incident_vectors"
INCIDENT_VECTOR_DIM = 16


@dataclass
class RedisContext:
    customer: dict[str, Any] | None
    incidents: list[dict[str, Any]]
    similar_incidents: list[dict[str, Any]]
    tickets: list[dict[str, Any]]
    memories: list[str]
    customer_id: str | None
    retrieval_backend: str


class RedisIRISTools:
    def __init__(self) -> None:
        host = os.getenv("REDIS_HOST", "redis")
        port = int(os.getenv("REDIS_PORT", "6379"))
        self.cache_ttl_seconds = int(os.getenv("REDIS_LANGCACHE_TTL_SECONDS", str(DEFAULT_CACHE_TTL_SECONDS)))
        self.max_customers = int(os.getenv("RDI_MAX_CUSTOMERS", str(DEFAULT_RDI_MAX_CUSTOMERS)))
        self.seed_path = self._resolve_seed_path()
        self._client = Redis(host=host, port=port, decode_responses=True)
        self._client_binary = Redis(host=host, port=port, decode_responses=False)
        self._sync_lock = asyncio.Lock()
        self._last_sync_stats: dict[str, Any] = {
            "status": "idle",
            "synced_customers": 0,
            "synced_tickets": 0,
            "synced_incidents": 0,
            "errors": 0,
        }

    @staticmethod
    def _resolve_seed_path() -> Path:
        explicit = os.getenv("CUSTOMERS_SEED_PATH")
        if explicit:
            return Path(explicit)
        return Path(__file__).resolve().parents[2] / "data" / "customers_seed.json"

    def available(self) -> bool:
        try:
            self._client.ping()
            return True
        except Exception:
            return False

    def _read_seed(self) -> dict[str, Any]:
        if not self.seed_path.exists():
            return {}
        return json.loads(self.seed_path.read_text(encoding="utf-8"))

    @staticmethod
    def _normalize_name(name: str) -> str:
        return name.strip().lower()

    def _json_get(self, key: str) -> dict[str, Any] | None:
        payload = self._client.execute_command("JSON.GET", key)
        if not payload:
            return None
        return json.loads(payload)

    def _json_set(self, key: str, value: Any) -> None:
        self._client.execute_command("JSON.SET", key, "$", json.dumps(value))

    def _ensure_search_indexes(self) -> None:
        self._ensure_index(
            CUSTOMER_INDEX,
            [
                "ON",
                "JSON",
                "PREFIX",
                "1",
                "customer:",
                "SCHEMA",
                "$.id",
                "AS",
                "customer_id",
                "TAG",
                "$.name",
                "AS",
                "name",
                "TEXT",
                "$.risk_level",
                "AS",
                "risk_level",
                "TAG",
                "$.account_owner",
                "AS",
                "account_owner",
                "TEXT",
                "$.health_score",
                "AS",
                "health_score",
                "NUMERIC",
            ],
        )
        self._ensure_index(
            TICKET_INDEX,
            [
                "ON",
                "JSON",
                "PREFIX",
                "1",
                "ticket:",
                "SCHEMA",
                "$.customer_id",
                "AS",
                "customer_id",
                "TAG",
                "$.status",
                "AS",
                "status",
                "TAG",
                "$.severity",
                "AS",
                "severity",
                "TAG",
                "$.summary",
                "AS",
                "summary",
                "TEXT",
            ],
        )
        self._ensure_index(
            INCIDENT_INDEX,
            [
                "ON",
                "JSON",
                "PREFIX",
                "1",
                "incident:",
                "SCHEMA",
                "$.customer_id",
                "AS",
                "customer_id",
                "TAG",
                "$.status",
                "AS",
                "status",
                "TAG",
                "$.service",
                "AS",
                "service",
                "TAG",
                "$.summary",
                "AS",
                "summary",
                "TEXT",
            ],
        )
        self._ensure_vector_index()

    def _ensure_vector_index(self) -> None:
        try:
            self._client_binary.execute_command(
                "FT.CREATE",
                INCIDENT_VECTOR_INDEX,
                "ON",
                "HASH",
                "PREFIX",
                "1",
                "incident_vec:",
                "SCHEMA",
                "incident_id",
                "TAG",
                "customer_id",
                "TAG",
                "summary",
                "TEXT",
                "status",
                "TAG",
                "service",
                "TAG",
                "embedding",
                "VECTOR",
                "FLAT",
                "6",
                "TYPE",
                "FLOAT32",
                "DIM",
                str(INCIDENT_VECTOR_DIM),
                "DISTANCE_METRIC",
                "COSINE",
            )
        except Exception as exc:
            if "Index already exists" not in str(exc):
                raise

    def _ensure_index(self, index_name: str, args: list[str]) -> None:
        try:
            self._client.execute_command("FT.CREATE", index_name, *args)
        except Exception as exc:
            if "Index already exists" not in str(exc):
                raise

    @staticmethod
    def _escape_tag_value(value: str) -> str:
        escaped = value.replace("\\", "\\\\")
        for ch in ["-", ".", "/", ":", "@", " "]:
            escaped = escaped.replace(ch, f"\\{ch}")
        return escaped

    def _search_keys(self, index_name: str, query: str, limit: int) -> list[str]:
        output = self._client.execute_command(
            "FT.SEARCH",
            index_name,
            query,
            "NOCONTENT",
            "LIMIT",
            "0",
            str(limit),
        )
        if not isinstance(output, list) or len(output) < 2:
            return []
        return [str(item) for item in output[1:] if isinstance(item, str)]

    @staticmethod
    def _text_to_embedding_bytes(text: str, dim: int = INCIDENT_VECTOR_DIM) -> bytes:
        # Deterministic pseudo-embedding keeps local demo dependencies light.
        material = hashlib.sha256(text.encode("utf-8")).digest()
        packed = bytearray()

        while len(packed) < dim * 4:
            material = hashlib.sha256(material).digest()
            for offset in range(0, len(material), 4):
                chunk = material[offset: offset + 4]
                if len(chunk) < 4:
                    continue
                raw = int.from_bytes(chunk, "little", signed=False)
                value = (raw / 4294967295.0) * 2.0 - 1.0
                packed.extend(struct.pack("<f", value))
                if len(packed) >= dim * 4:
                    break

        return bytes(packed)

    @staticmethod
    def _decode_scalar(value: Any) -> str:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="ignore")
        return str(value)

    def _vector_search_similar_incidents(self, customer_id: str, query_text: str, limit: int = 3) -> list[dict[str, Any]]:
        escaped_customer_id = self._escape_tag_value(customer_id)
        query = (
            f"(@customer_id:{{{escaped_customer_id}}})"
            f"=>[KNN {limit + 1} @embedding $query_vec AS score]"
        )
        query_vec = self._text_to_embedding_bytes(query_text)

        output = self._client_binary.execute_command(
            "FT.SEARCH",
            INCIDENT_VECTOR_INDEX,
            query,
            "PARAMS",
            "2",
            "query_vec",
            query_vec,
            "SORTBY",
            "score",
            "RETURN",
            "5",
            "incident_id",
            "summary",
            "status",
            "service",
            "score",
            "DIALECT",
            "2",
        )

        if not isinstance(output, list) or len(output) < 3:
            return []

        candidates: list[dict[str, Any]] = []
        for idx in range(1, len(output), 2):
            if idx + 1 >= len(output):
                break
            raw_fields = output[idx + 1]
            if not isinstance(raw_fields, list):
                continue

            row: dict[str, Any] = {}
            for field_idx in range(0, len(raw_fields), 2):
                if field_idx + 1 >= len(raw_fields):
                    break
                key = self._decode_scalar(raw_fields[field_idx])
                value = self._decode_scalar(raw_fields[field_idx + 1])
                row[key] = value

            incident_id = str(row.get("incident_id", "")).strip()
            if not incident_id:
                continue

            score_value = row.get("score")
            try:
                score = float(score_value) if score_value is not None else None
            except ValueError:
                score = None

            candidates.append(
                {
                    "incident_id": incident_id,
                    "summary": str(row.get("summary", "")),
                    "status": str(row.get("status", "")),
                    "service": str(row.get("service", "")),
                    "score": score,
                }
            )

        return candidates[:limit]

    def sync_once(self) -> dict[str, Any]:
        seed = self._read_seed()
        customers = list(seed.get("customers", []))[: self.max_customers]
        tickets = list(seed.get("tickets", []))
        incidents = list(seed.get("incidents", []))

        stats = {
            "status": "ok",
            "synced_customers": 0,
            "synced_tickets": 0,
            "synced_incidents": 0,
            "errors": 0,
        }

        try:
            self._ensure_search_indexes()

            for customer in customers:
                customer_id = str(customer.get("id", ""))
                if not customer_id:
                    continue
                customer_name = str(customer.get("name", ""))

                self._json_set(f"customer:{customer_id}", customer)
                self._client.set(f"customer_name:{self._normalize_name(customer_name)}", customer_id)
                self._client.delete(f"customer:{customer_id}:tickets")
                self._client.delete(f"customer:{customer_id}:incidents")
                stats["synced_customers"] += 1

            indexed_customer_ids = {str(customer.get("id", "")) for customer in customers}

            for ticket in tickets:
                ticket_id = str(ticket.get("ticket_id", ""))
                customer_id = str(ticket.get("customer_id", ""))
                if not ticket_id or customer_id not in indexed_customer_ids:
                    continue
                self._json_set(f"ticket:{ticket_id}", ticket)
                self._client.rpush(f"customer:{customer_id}:tickets", ticket_id)
                stats["synced_tickets"] += 1

            for incident in incidents:
                incident_id = str(incident.get("incident_id", ""))
                customer_id = str(incident.get("customer_id", ""))
                if not incident_id or customer_id not in indexed_customer_ids:
                    continue
                self._json_set(f"incident:{incident_id}", incident)
                self._client.rpush(f"customer:{customer_id}:incidents", incident_id)
                incident_summary = str(incident.get("summary", ""))
                self._client_binary.hset(
                    f"incident_vec:{incident_id}",
                    mapping={
                        b"incident_id": incident_id.encode("utf-8"),
                        b"customer_id": customer_id.encode("utf-8"),
                        b"summary": incident_summary.encode("utf-8"),
                        b"status": str(incident.get("status", "")).encode("utf-8"),
                        b"service": str(incident.get("service", "")).encode("utf-8"),
                        b"embedding": self._text_to_embedding_bytes(incident_summary),
                    },
                )
                stats["synced_incidents"] += 1

            self._last_sync_stats = stats
        except Exception:
            stats["status"] = "error"
            stats["errors"] += 1
            self._last_sync_stats = stats

        return self._last_sync_stats

    def rdi_status(self) -> dict[str, Any]:
        return {
            "seed_path": str(self.seed_path),
            "max_customers": self.max_customers,
            "last_sync": self._last_sync_stats,
            "redis_available": self.available(),
        }

    def retrieve_context(self, customer_name: str, memory_limit: int = 5) -> RedisContext:
        try:
            self._ensure_search_indexes()
            customer_query = f'"{customer_name.strip()}"'
            customer_keys = self._search_keys(CUSTOMER_INDEX, customer_query, limit=1)
        except Exception:
            customer_keys = []

        customer_key = customer_keys[0] if customer_keys else None
        customer: dict[str, Any] | None = self._json_get(customer_key) if customer_key else None

        # Fallback ID mapping only if FT.SEARCH phrase lookup has no exact match.
        customer_id = str(customer.get("id", "")) if customer else self._client.get(
            f"customer_name:{self._normalize_name(customer_name)}"
        )
        if not customer_id:
            return RedisContext(None, [], [], [], [], None, "none")

        if customer is None:
            customer = self._json_get(f"customer:{customer_id}")

        query_customer_id = self._escape_tag_value(customer_id)

        tickets: list[dict[str, Any]] = []
        for ticket_key in self._search_keys(TICKET_INDEX, f"@customer_id:{{{query_customer_id}}}", limit=10):
            ticket = self._json_get(ticket_key)
            if ticket:
                tickets.append(ticket)

        incidents: list[dict[str, Any]] = []
        for incident_key in self._search_keys(INCIDENT_INDEX, f"@customer_id:{{{query_customer_id}}}", limit=10):
            incident = self._json_get(incident_key)
            if incident:
                incidents.append(incident)

        similar_incidents: list[dict[str, Any]] = []
        if incidents:
            query_incident = incidents[0]
            query_summary = str(query_incident.get("summary", ""))
            query_incident_id = str(query_incident.get("incident_id", ""))
            if query_summary:
                try:
                    candidates = self._vector_search_similar_incidents(customer_id, query_summary, limit=3)
                    similar_incidents = [
                        row for row in candidates if str(row.get("incident_id", "")) != query_incident_id
                    ]
                except Exception:
                    similar_incidents = []

        memories = self._client.lrange(f"memory:{customer_id}", 0, max(memory_limit - 1, 0))

        return RedisContext(
            customer=customer,
            incidents=incidents,
            similar_incidents=similar_incidents,
            tickets=tickets,
            memories=memories,
            customer_id=customer_id,
            retrieval_backend="ft.search+vector" if similar_incidents else "ft.search",
        )

    def append_memory(self, customer_id: str, memory_text: str) -> None:
        if not customer_id:
            return
        self._client.lpush(f"memory:{customer_id}", memory_text)
        self._client.ltrim(f"memory:{customer_id}", 0, 99)

    @staticmethod
    def _cache_key(customer: str, message: str) -> str:
        digest = hashlib.sha256(f"{customer.strip().lower()}::{message.strip().lower()}".encode("utf-8")).hexdigest()
        return f"langcache:{digest}"

    def get_cached_response(self, customer: str, message: str) -> dict[str, Any] | None:
        raw = self._client.get(self._cache_key(customer, message))
        if not raw:
            return None
        return json.loads(raw)

    def set_cached_response(self, customer: str, message: str, response: dict[str, Any]) -> None:
        self._client.setex(
            self._cache_key(customer, message),
            self.cache_ttl_seconds,
            json.dumps(response),
        )

    def append_operational_event(self, event: dict[str, Any], max_len: int = 1000) -> str | None:
        # Persist recent operational events for replay/audit flows.
        stream_fields = {
            "event_type": str(event.get("event_type", "unknown")),
            "status": str(event.get("status", "unknown")),
            "customer": str(event.get("customer", "unknown")),
            "message": str(event.get("message") or ""),
            "source": str(event.get("source", "unknown")),
            "timestamp": str(event.get("timestamp", "")),
        }
        return self._client.xadd(
            "events:operational",
            stream_fields,
            maxlen=max_len,
            approximate=True,
        )


class RDISyncLoop:
    def __init__(self, tools: RedisIRISTools) -> None:
        self.tools = tools
        self._task: asyncio.Task[None] | None = None
        self.interval_seconds = int(os.getenv("RDI_SYNC_INTERVAL_SECONDS", str(DEFAULT_SYNC_SECONDS)))

    async def _run_forever(self) -> None:
        while True:
            try:
                if self.tools.available():
                    async with self.tools._sync_lock:
                        self.tools.sync_once()
            except Exception:
                # Keep the background loop alive; observability is provided via /api/rdi/status.
                pass
            await asyncio.sleep(self.interval_seconds)

    async def start(self) -> None:
        if self._task is not None and not self._task.done():
            return
        self._task = asyncio.create_task(self._run_forever())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None


def merge_seed_with_redis(seed: dict[str, Any], context: RedisContext) -> dict[str, Any]:
    merged = dict(seed)

    if context.customer is not None:
        merged["customer"] = context.customer
    if context.incidents:
        merged["incidents"] = context.incidents
    if context.similar_incidents:
        merged["similar_incidents"] = context.similar_incidents
    if context.tickets:
        merged["tickets"] = context.tickets
    if context.memories:
        merged["memories"] = context.memories

    return merged
