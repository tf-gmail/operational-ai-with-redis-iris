from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

from redis import Redis

from app.redis_client import get_redis_connection_config


DEFAULT_BASELINE_STATE_TTL_SECONDS = 86400
DEFAULT_REPLAY_STATE_TTL_SECONDS = 14400


class RuntimeStateStore:
    def __init__(self) -> None:
        self._config = get_redis_connection_config()
        self._client: Redis = self._config.create_client(decode_responses=True)
        self._baseline_ttl_seconds = int(
            os.getenv("BASELINE_STATE_TTL_SECONDS", str(DEFAULT_BASELINE_STATE_TTL_SECONDS))
        )
        self._replay_ttl_seconds = int(
            os.getenv("REPLAY_STATE_TTL_SECONDS", str(DEFAULT_REPLAY_STATE_TTL_SECONDS))
        )

    def available(self) -> bool:
        try:
            self._client.ping()
            return True
        except Exception:
            return False

    @staticmethod
    def _normalize_customer(customer: str) -> str:
        return customer.strip().lower()

    def _baseline_key(self, customer: str) -> str:
        return f"state:baseline:{self._normalize_customer(customer)}"

    @staticmethod
    def _replay_key(run_id: str) -> str:
        return f"state:replay:{run_id}"

    def load_baseline_session(self, customer: str) -> dict[str, Any] | None:
        try:
            raw = self._client.get(self._baseline_key(customer))
            if not raw:
                return None
            decoded = json.loads(raw)
            return decoded if isinstance(decoded, dict) else None
        except Exception:
            return None

    def save_baseline_session(self, customer: str, session: dict[str, Any]) -> None:
        if not isinstance(session, dict):
            return
        try:
            self._client.setex(
                self._baseline_key(customer),
                self._baseline_ttl_seconds,
                json.dumps(session),
            )
        except Exception:
            return

    def load_replay_run(self, run_id: str) -> dict[str, Any] | None:
        try:
            raw = self._client.get(self._replay_key(run_id))
            if not raw:
                return None
            decoded = json.loads(raw)
            return decoded if isinstance(decoded, dict) else None
        except Exception:
            return None

    def save_replay_run(self, run_state: dict[str, Any]) -> None:
        run_id = str(run_state.get("run_id", "")) if isinstance(run_state, dict) else ""
        if not run_id:
            return
        try:
            self._client.setex(
                self._replay_key(run_id),
                self._replay_ttl_seconds,
                json.dumps(run_state),
            )
        except Exception:
            return


@lru_cache(maxsize=1)
def get_runtime_state_store() -> RuntimeStateStore | None:
    try:
        store = RuntimeStateStore()
        if not store.available():
            return None
        return store
    except Exception:
        return None
