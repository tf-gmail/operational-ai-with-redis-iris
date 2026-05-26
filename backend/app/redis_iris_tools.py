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
LANGCACHE_INDEX_LIMIT = 80
LANGCACHE_SIMILARITY_THRESHOLD = 0.55
CUSTOMER_INDEX = "idx:customers"
TICKET_INDEX = "idx:tickets"
INCIDENT_INDEX = "idx:incidents"
INCIDENT_VECTOR_INDEX = "idx:incident_vectors"
INCIDENT_VECTOR_DIM = 16


@dataclass
class RedisContext:
    customer: dict[str, Any] | None
    contract: dict[str, Any] | None
    usage: dict[str, Any] | None
    workflow_state: dict[str, Any] | None
    incidents: list[dict[str, Any]]
    similar_incidents: list[dict[str, Any]]
    tickets: list[dict[str, Any]]
    timeline_events: list[dict[str, Any]]
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
            "synced_contracts": 0,
            "synced_usage": 0,
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

    @staticmethod
    def _memory_key(customer_id: str, kind: str = "short") -> str:
        if kind == "long":
            return f"memory:long:{customer_id}"
        return f"memory:{customer_id}"

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

    @staticmethod
    def _derive_query_hints(query_text: str | None) -> dict[str, str]:
        text = (query_text or "").lower()

        severity = ""
        if "sev-1" in text or "sev1" in text:
            severity = "sev-1"
        elif "sev-2" in text or "sev2" in text:
            severity = "sev-2"
        elif "sev-3" in text or "sev3" in text:
            severity = "sev-3"

        ticket_status = ""
        for status in ["open", "in_progress", "pending_customer", "resolved"]:
            if status in text:
                ticket_status = status
                break

        incident_status = ""
        for status in ["investigating", "mitigated", "monitoring", "resolved"]:
            if status in text:
                incident_status = status
                break

        service = ""
        for candidate in ["search-api", "billing-api", "identity-api", "events-api", "sync-worker"]:
            if candidate in text:
                service = candidate
                break

        return {
            "severity": severity,
            "ticket_status": ticket_status,
            "incident_status": incident_status,
            "service": service,
        }

    @staticmethod
    def _tokenize_memory(text: str) -> set[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return {part for part in cleaned.split() if len(part) >= 3}

    @staticmethod
    def _clip_memory_text(text: str, limit: int = 220) -> str:
        clipped = text.strip().replace("\n", " ")
        if len(clipped) <= limit:
            return clipped
        return clipped[: limit - 3].rstrip() + "..."

    def extract_memory_facts(self, customer_message: str, response_summary: str | None = None) -> list[str]:
        source = f"{customer_message} {response_summary or ''}".strip()
        lowered = source.lower()
        facts: list[str] = []

        if any(token in lowered for token in ["prefer", "preference", "executive summary"]):
            facts.append("preference:" + self._clip_memory_text(customer_message))

        if any(token in lowered for token in ["promis", "commitment", "escalat"]):
            facts.append("commitment:" + self._clip_memory_text(customer_message))

        if "renewal" in lowered or "cancel" in lowered:
            facts.append("renewal-risk:" + self._clip_memory_text(customer_message))

        if any(token in lowered for token in ["incident", "outage", "latency", "mitigat"]):
            facts.append("operational-risk:" + self._clip_memory_text(source))

        deduped: list[str] = []
        for fact in facts:
            if fact not in deduped:
                deduped.append(fact)
        return deduped[:4]

    def retrieve_memories(self, customer_id: str, query_text: str | None = None, memory_limit: int = 5) -> list[str]:
        if not customer_id:
            return []

        short_memories = self._client.lrange(self._memory_key(customer_id, "short"), 0, 39)
        long_memories = self._client.lrange(self._memory_key(customer_id, "long"), 0, 39)

        combined: list[tuple[str, str, int]] = []
        combined.extend((text, "short", idx) for idx, text in enumerate(short_memories))
        combined.extend((text, "long", idx) for idx, text in enumerate(long_memories))

        if not combined:
            return []

        query_tokens = self._tokenize_memory(query_text or "")
        scored: list[tuple[int, int, str]] = []
        for text, source, recency in combined:
            memory_tokens = self._tokenize_memory(text)
            overlap = len(query_tokens.intersection(memory_tokens)) if query_tokens else 0
            source_bonus = 1 if source == "long" else 0
            score = (overlap * 4) + source_bonus
            scored.append((score, recency, text))

        scored.sort(key=lambda item: (-item[0], item[1]))

        selected: list[str] = []
        for _, _, text in scored:
            if text and text not in selected:
                selected.append(text)
            if len(selected) >= max(memory_limit, 1):
                break
        return selected

    @staticmethod
    def _build_timeline_events(
        tickets: list[dict[str, Any]],
        incidents: list[dict[str, Any]],
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []

        for ticket in tickets:
            ticket_id = str(ticket.get("ticket_id", ""))
            for item in ticket.get("timeline", []) if isinstance(ticket.get("timeline"), list) else []:
                if not isinstance(item, dict):
                    continue
                events.append(
                    {
                        "timestamp": str(item.get("timestamp", "")),
                        "entity_type": "ticket",
                        "entity_id": ticket_id,
                        "status": str(item.get("status", "")),
                        "note": str(item.get("note", "")),
                    }
                )

        for incident in incidents:
            incident_id = str(incident.get("incident_id", ""))
            for item in incident.get("timeline", []) if isinstance(incident.get("timeline"), list) else []:
                if not isinstance(item, dict):
                    continue
                events.append(
                    {
                        "timestamp": str(item.get("timestamp", "")),
                        "entity_type": "incident",
                        "entity_id": incident_id,
                        "status": str(item.get("status", "")),
                        "note": str(item.get("note", "")),
                    }
                )

        events.sort(key=lambda row: row.get("timestamp", ""), reverse=True)
        return events[:limit]

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
            "synced_contracts": 0,
            "synced_usage": 0,
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
                contract = customer.get("contract")
                usage = customer.get("usage")

                self._json_set(f"customer:{customer_id}", customer)
                self._client.set(f"customer_name:{self._normalize_name(customer_name)}", customer_id)
                self._client.delete(f"customer:{customer_id}:tickets")
                self._client.delete(f"customer:{customer_id}:incidents")

                if isinstance(contract, dict) and contract:
                    self._json_set(f"contract:{customer_id}", contract)
                    self._client.set(f"customer:{customer_id}:contract", f"contract:{customer_id}")
                    stats["synced_contracts"] += 1
                else:
                    self._client.delete(f"contract:{customer_id}")
                    self._client.delete(f"customer:{customer_id}:contract")

                if isinstance(usage, dict) and usage:
                    self._json_set(f"usage:{customer_id}", usage)
                    self._client.set(f"customer:{customer_id}:usage", f"usage:{customer_id}")
                    stats["synced_usage"] += 1
                else:
                    self._client.delete(f"usage:{customer_id}")
                    self._client.delete(f"customer:{customer_id}:usage")

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

    def retrieve_context(
        self,
        customer_name: str,
        query_text: str | None = None,
        memory_limit: int = 5,
    ) -> RedisContext:
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
            return RedisContext(None, None, None, None, [], [], [], [], [], None, "none")

        if customer is None:
            customer = self._json_get(f"customer:{customer_id}")

        contract = self._json_get(f"contract:{customer_id}")
        usage = self._json_get(f"usage:{customer_id}")
        workflow_state = self.get_shared_workflow_state(customer_id)

        query_customer_id = self._escape_tag_value(customer_id)
        hints = self._derive_query_hints(query_text)

        tickets: list[dict[str, Any]] = []
        ticket_query = f"@customer_id:{{{query_customer_id}}}"
        if hints["severity"]:
            ticket_query += f" @severity:{{{self._escape_tag_value(hints['severity'])}}}"
        if hints["ticket_status"]:
            ticket_query += f" @status:{{{self._escape_tag_value(hints['ticket_status'])}}}"

        for ticket_key in self._search_keys(TICKET_INDEX, ticket_query, limit=10):
            ticket = self._json_get(ticket_key)
            if ticket:
                tickets.append(ticket)

        incidents: list[dict[str, Any]] = []
        incident_query = f"@customer_id:{{{query_customer_id}}}"
        if hints["incident_status"]:
            incident_query += f" @status:{{{self._escape_tag_value(hints['incident_status'])}}}"
        if hints["service"]:
            incident_query += f" @service:{{{self._escape_tag_value(hints['service'])}}}"

        for incident_key in self._search_keys(INCIDENT_INDEX, incident_query, limit=10):
            incident = self._json_get(incident_key)
            if incident:
                incidents.append(incident)

        incidents.sort(key=lambda row: str(row.get("updated_at", "")), reverse=True)
        tickets.sort(key=lambda row: str(row.get("created_at", "")), reverse=True)

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

        memories = self.retrieve_memories(customer_id, query_text=query_text, memory_limit=memory_limit)
        timeline_events = self._build_timeline_events(tickets=tickets, incidents=incidents)

        used_filters = [
            name
            for name, value in hints.items()
            if value
        ]
        retrieval_suffix = "+filters" if used_filters else ""
        backend_parts = [f"ft.search{retrieval_suffix}"]
        if similar_incidents:
            backend_parts.append("vector")
        if memories:
            backend_parts.append("memory")

        return RedisContext(
            customer=customer,
            contract=contract,
            usage=usage,
            workflow_state=workflow_state,
            incidents=incidents,
            similar_incidents=similar_incidents,
            tickets=tickets,
            timeline_events=timeline_events,
            memories=memories,
            customer_id=customer_id,
            retrieval_backend="+".join(backend_parts),
        )

    def append_memory(self, customer_id: str, memory_text: str, kind: str = "short") -> None:
        if not customer_id:
            return

        key = self._memory_key(customer_id, kind)
        text = self._clip_memory_text(memory_text)
        if not text:
            return

        self._client.lrem(key, 0, text)
        self._client.lpush(key, text)
        self._client.ltrim(key, 0, 199 if kind == "long" else 99)

    def get_shared_workflow_state(self, customer_id: str) -> dict[str, Any] | None:
        if not customer_id:
            return None
        raw = self._client.get(f"workflow_state:{customer_id}")
        if not raw:
            return None
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return decoded if isinstance(decoded, dict) else None

    def set_shared_workflow_state(self, customer_id: str, state: dict[str, Any]) -> None:
        if not customer_id:
            return
        if not isinstance(state, dict):
            return

        # Keep state intentionally bounded so shared context remains compact.
        bounded_state = {
            "turn_count": int(state.get("turn_count", 0)),
            "last_mode": str(state.get("last_mode", "iris")),
            "last_message": self._clip_memory_text(str(state.get("last_message", "")), limit=180),
            "last_summary": self._clip_memory_text(str(state.get("last_summary", "")), limit=220),
            "updated_at": str(state.get("updated_at", "")),
        }
        self._client.set(f"workflow_state:{customer_id}", json.dumps(bounded_state))

    @staticmethod
    def _cache_key(customer: str, message: str) -> str:
        digest = hashlib.sha256(f"{customer.strip().lower()}::{message.strip().lower()}".encode("utf-8")).hexdigest()
        return f"langcache:{digest}"

    @staticmethod
    def _cache_index_key(customer: str) -> str:
        return f"langcache:index:{customer.strip().lower()}"

    @staticmethod
    def _cache_tokens(text: str) -> set[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return {part for part in cleaned.split() if len(part) >= 3}

    @classmethod
    def _cache_similarity(cls, left: str, right: str) -> float:
        left_tokens = cls._cache_tokens(left)
        right_tokens = cls._cache_tokens(right)
        if not left_tokens or not right_tokens:
            return 0.0
        intersection = len(left_tokens.intersection(right_tokens))
        union = len(left_tokens.union(right_tokens))
        return intersection / max(union, 1)

    @staticmethod
    def _decode_cached_payload(raw: str) -> tuple[dict[str, Any] | None, str]:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return None, "invalid"

        if isinstance(payload, dict) and isinstance(payload.get("response"), dict):
            return payload, "wrapped"
        if isinstance(payload, dict):
            # Backward-compatible read for legacy direct response cache payloads.
            return {"message": "", "response": payload}, "legacy"
        return None, "invalid"

    def get_cached_response(self, customer: str, message: str) -> dict[str, Any] | None:
        exact_key = self._cache_key(customer, message)
        raw = self._client.get(exact_key)
        if raw:
            parsed, _ = self._decode_cached_payload(raw)
            if parsed and isinstance(parsed.get("response"), dict):
                response = dict(parsed["response"])
                response["context_signals"] = list(response.get("context_signals", []))
                response["context_signals"].append("redis-langcache-exact-hit")
                return response

        # Similarity fallback for near-duplicate prompts.
        best_response: dict[str, Any] | None = None
        best_score = 0.0
        for cache_key in self._client.lrange(self._cache_index_key(customer), 0, LANGCACHE_INDEX_LIMIT - 1):
            if cache_key == exact_key:
                continue
            candidate_raw = self._client.get(str(cache_key))
            if not candidate_raw:
                continue

            parsed, payload_mode = self._decode_cached_payload(candidate_raw)
            if parsed is None:
                continue

            cached_message = str(parsed.get("message", ""))
            if payload_mode == "legacy" and not cached_message:
                continue

            score = self._cache_similarity(message, cached_message)
            if score < LANGCACHE_SIMILARITY_THRESHOLD or score <= best_score:
                continue

            candidate_response = parsed.get("response")
            if isinstance(candidate_response, dict):
                best_score = score
                best_response = dict(candidate_response)

        if best_response is not None:
            best_response["context_signals"] = list(best_response.get("context_signals", []))
            best_response["context_signals"].append("redis-langcache-semantic-hit")
            best_response["context_signals"].append(f"redis-langcache-similarity={best_score:.3f}")
            return best_response

        return None

    def set_cached_response(self, customer: str, message: str, response: dict[str, Any]) -> None:
        cache_key = self._cache_key(customer, message)
        wrapped_payload = {
            "message": message,
            "response": response,
        }
        self._client.setex(
            cache_key,
            self.cache_ttl_seconds,
            json.dumps(wrapped_payload),
        )

        index_key = self._cache_index_key(customer)
        self._client.lrem(index_key, 0, cache_key)
        self._client.lpush(index_key, cache_key)
        self._client.ltrim(index_key, 0, LANGCACHE_INDEX_LIMIT - 1)

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

    def get_recent_operational_events(self, customer: str | None = None, limit: int = 30) -> list[dict[str, Any]]:
        normalized_customer = self._normalize_name(customer or "") if customer else ""
        count = max(1, min(limit, 200))

        entries = self._client.xrevrange("events:operational", count=count)
        events: list[dict[str, Any]] = []

        for stream_id, fields in entries:
            if not isinstance(fields, dict):
                continue

            event_customer = str(fields.get("customer", ""))
            if normalized_customer and self._normalize_name(event_customer) != normalized_customer:
                continue

            event = {
                "redis_stream_id": str(stream_id),
                "event_type": str(fields.get("event_type", "unknown")),
                "status": str(fields.get("status", "unknown")),
                "customer": event_customer,
                "message": str(fields.get("message", "")),
                "source": str(fields.get("source", "redis-stream")),
                "timestamp": str(fields.get("timestamp", "")),
            }
            events.append(event)

        return events


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
        if context.contract is not None:
            merged["customer"]["contract"] = context.contract
        if context.usage is not None:
            merged["customer"]["usage"] = context.usage
    else:
        if context.contract is not None:
            merged["contract"] = context.contract
        if context.usage is not None:
            merged["usage"] = context.usage
    if context.incidents:
        merged["incidents"] = context.incidents
    if context.similar_incidents:
        merged["similar_incidents"] = context.similar_incidents
    if context.tickets:
        merged["tickets"] = context.tickets
    if context.timeline_events:
        merged["operational_timeline"] = context.timeline_events
    if context.memories:
        merged["memories"] = context.memories
    if context.workflow_state is not None:
        merged["shared_workflow_state"] = context.workflow_state

    return merged
