#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from verify_redis_stack import (
    build_client,
    check_json,
    check_modules,
    check_search,
    check_streams,
    check_vector,
)


def _request_json(base_url: str, path: str) -> dict[str, Any]:
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    request = Request(url=url, method="GET", headers={"Accept": "application/json"})
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def _ok(message: str) -> None:
    print(f"[PASS] {message}")


def _fail(message: str) -> None:
    print(f"[FAIL] {message}")


def _check_tls_mode(redis_args: argparse.Namespace, require_tls: bool) -> bool:
    url = str(getattr(redis_args, "url", "") or "").strip().lower()
    explicit_tls = bool(getattr(redis_args, "tls", False))
    tls_enabled = explicit_tls or url.startswith("rediss://")

    if require_tls and not tls_enabled:
        _fail("TLS is required for Azure compatibility checks, but neither --tls nor rediss:// URL is enabled.")
        return False

    if tls_enabled:
        _ok("Redis connection uses TLS mode.")
    else:
        _ok("Redis connection uses non-TLS mode (allowed for local compatibility checks).")
    return True


def _check_backend_config(base_url: str, require_tls: bool) -> bool:
    try:
        payload = _request_json(base_url, "/api/config")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        _fail(f"Unable to query backend config endpoint: {exc}")
        return False

    redis_enabled = str(payload.get("redis_tools_enabled", "false")).lower() == "true"
    redis_tls = str(payload.get("redis_tls", "false")).lower() == "true"

    if not redis_enabled:
        _fail("Backend reports redis_tools_enabled=false; architecture is not ready for AMR deployment.")
        return False

    if require_tls and not redis_tls:
        _fail("Backend reports redis_tls=false while --require-tls is enabled.")
        return False

    _ok(
        "Backend config check passed "
        f"(redis_mode={payload.get('redis_mode', 'unknown')}, redis_tls={payload.get('redis_tls', 'unknown')})."
    )
    return True


def _check_redis_capabilities(redis_args: argparse.Namespace) -> bool:
    try:
        client = build_client(redis_args)
    except Exception as exc:
        _fail(f"Unable to create Redis client for capability checks: {exc}")
        return False

    checks = [
        ("Connectivity", lambda c: (bool(c.ping()), "ping ok")),
        ("Modules", check_modules),
        ("RedisJSON", check_json),
        ("RediSearch", check_search),
        ("Vector Search", check_vector),
        ("Streams", check_streams),
    ]

    all_ok = True
    for name, fn in checks:
        try:
            ok, details = fn(client)
        except Exception as exc:
            ok, details = False, str(exc)
        if ok:
            _ok(f"{name}: {details}")
        else:
            _fail(f"{name}: {details}")
        all_ok = all_ok and ok

    return all_ok


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate EPIC 7 Task 7.3 Azure compatibility requirements.")
    parser.add_argument("--url", default=os.getenv("REDIS_URL", ""))
    parser.add_argument("--host", default=os.getenv("REDIS_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("REDIS_PORT", "6379")))
    parser.add_argument("--db", type=int, default=int(os.getenv("REDIS_DB", "0")))
    parser.add_argument("--username", default=os.getenv("REDIS_USERNAME"))
    parser.add_argument("--password", default=os.getenv("REDIS_PASSWORD"))
    parser.add_argument(
        "--tls",
        action="store_true",
        default=str(os.getenv("REDIS_TLS", "false")).strip().lower() in {"1", "true", "yes", "on"},
    )
    parser.add_argument(
        "--tls-insecure",
        action="store_true",
        default=str(os.getenv("REDIS_TLS_INSECURE", "false")).strip().lower() in {"1", "true", "yes", "on"},
    )
    parser.add_argument("--tls-ca-cert", default=os.getenv("REDIS_TLS_CA_CERT"))
    parser.add_argument("--tls-client-cert", default=os.getenv("REDIS_TLS_CLIENT_CERT"))
    parser.add_argument("--tls-client-key", default=os.getenv("REDIS_TLS_CLIENT_KEY"))
    parser.add_argument(
        "--base-url",
        default=os.getenv("AZURE_COMPAT_BASE_URL", "http://localhost:8000"),
        help="Backend API base URL for runtime compatibility checks.",
    )
    parser.add_argument(
        "--require-tls",
        action="store_true",
        default=True,
        help="Require TLS-compatible Redis and backend runtime configuration (default: enabled).",
    )
    parser.add_argument(
        "--allow-non-tls",
        action="store_true",
        help="Allow non-TLS mode for local smoke checks.",
    )

    args = parser.parse_args()
    args.require_tls = False if args.allow_non_tls else bool(args.require_tls)
    return args


def main() -> int:
    args = parse_args()

    checks = [
        _check_tls_mode(args, bool(args.require_tls)),
        _check_redis_capabilities(args),
        _check_backend_config(str(args.base_url), bool(args.require_tls)),
    ]

    if all(checks):
        _ok("Azure compatibility validation passed (Search, JSON, Vector, Streams, TLS, runtime config).")
        return 0

    _fail("Azure compatibility validation failed. See failing checks above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
