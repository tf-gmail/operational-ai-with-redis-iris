from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

from redis import Redis


_TRUE_VALUES = {"1", "true", "yes", "on"}


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in _TRUE_VALUES


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str) -> float | None:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


@dataclass(frozen=True)
class RedisConnectionConfig:
    url: str | None
    host: str
    port: int
    db: int
    username: str | None
    password: str | None
    tls: bool
    tls_insecure: bool
    tls_ca_cert: str | None
    tls_client_cert: str | None
    tls_client_key: str | None
    socket_timeout: float | None
    socket_connect_timeout: float | None

    @classmethod
    def from_env(cls) -> "RedisConnectionConfig":
        redis_url = os.getenv("REDIS_URL")
        scheme_tls = bool(redis_url and redis_url.strip().lower().startswith("rediss://"))
        return cls(
            url=redis_url.strip() if redis_url else None,
            host=os.getenv("REDIS_HOST", "redis"),
            port=_env_int("REDIS_PORT", 6379),
            db=_env_int("REDIS_DB", 0),
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD"),
            tls=_env_bool("REDIS_TLS", default=scheme_tls),
            tls_insecure=_env_bool("REDIS_TLS_INSECURE", default=False),
            tls_ca_cert=os.getenv("REDIS_TLS_CA_CERT"),
            tls_client_cert=os.getenv("REDIS_TLS_CLIENT_CERT"),
            tls_client_key=os.getenv("REDIS_TLS_CLIENT_KEY"),
            socket_timeout=_env_float("REDIS_SOCKET_TIMEOUT_SECONDS"),
            socket_connect_timeout=_env_float("REDIS_SOCKET_CONNECT_TIMEOUT_SECONDS"),
        )

    def _connection_kwargs(self, decode_responses: bool) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "decode_responses": decode_responses,
            "db": self.db,
        }
        if self.username:
            kwargs["username"] = self.username
        if self.password:
            kwargs["password"] = self.password
        if self.socket_timeout is not None:
            kwargs["socket_timeout"] = self.socket_timeout
        if self.socket_connect_timeout is not None:
            kwargs["socket_connect_timeout"] = self.socket_connect_timeout

        if self.tls:
            kwargs["ssl"] = True
            kwargs["ssl_cert_reqs"] = "none" if self.tls_insecure else "required"
            if self.tls_ca_cert:
                kwargs["ssl_ca_certs"] = self.tls_ca_cert
            if self.tls_client_cert:
                kwargs["ssl_certfile"] = self.tls_client_cert
            if self.tls_client_key:
                kwargs["ssl_keyfile"] = self.tls_client_key

        return kwargs

    def create_client(self, *, decode_responses: bool) -> Redis:
        kwargs = self._connection_kwargs(decode_responses=decode_responses)
        if self.url:
            return Redis.from_url(self.url, **kwargs)
        return Redis(host=self.host, port=self.port, **kwargs)

    def create_client_pair(self) -> tuple[Redis, Redis]:
        return (
            self.create_client(decode_responses=True),
            self.create_client(decode_responses=False),
        )

    def endpoint(self) -> tuple[str, int]:
        if self.url:
            parsed = urlparse(self.url)
            return parsed.hostname or self.host, parsed.port or self.port
        return self.host, self.port

    def public_config(self) -> dict[str, str]:
        endpoint_host, endpoint_port = self.endpoint()
        return {
            "redis_mode": "url" if self.url else "host_port",
            "redis_host": endpoint_host,
            "redis_port": str(endpoint_port),
            "redis_db": str(self.db),
            "redis_tls": "true" if self.tls else "false",
            "redis_tls_insecure": "true" if self.tls_insecure else "false",
        }


@lru_cache(maxsize=1)
def get_redis_connection_config() -> RedisConnectionConfig:
    return RedisConnectionConfig.from_env()
