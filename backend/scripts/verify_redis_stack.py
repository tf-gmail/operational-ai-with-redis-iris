from __future__ import annotations

import argparse
import json
import os
import sys

from redis import Redis
from redis.exceptions import ResponseError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Redis Stack capabilities")
    parser.add_argument("--host", default=os.getenv("REDIS_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("REDIS_PORT", "6379")))
    return parser.parse_args()


def print_result(name: str, ok: bool, details: str) -> None:
    state = "PASS" if ok else "FAIL"
    print(f"[{state}] {name}: {details}")


def check_modules(client: Redis) -> tuple[bool, str]:
    try:
        modules = client.execute_command("MODULE", "LIST")
    except Exception as exc:
        return False, f"unable to list modules: {exc}"

    names: set[str] = set()
    for entry in modules:
        if isinstance(entry, dict):
            raw_name = entry.get("name", b"")
            names.add(raw_name.decode() if isinstance(raw_name, bytes) else str(raw_name))
            continue

        # Redis can return MODULE LIST as nested arrays: [b'name', b'search', ...]
        if isinstance(entry, (list, tuple)):
            for i in range(0, len(entry) - 1, 2):
                key = entry[i]
                value = entry[i + 1]
                key_str = key.decode() if isinstance(key, bytes) else str(key)
                if key_str == "name":
                    names.add(value.decode() if isinstance(value, bytes) else str(value))
                    break

    required = {"ReJSON", "search"}
    missing = sorted(required - names)
    if missing:
        return False, f"missing modules: {', '.join(missing)}"
    return True, f"modules present: {', '.join(sorted(names))}"


def check_json(client: Redis) -> tuple[bool, str]:
    key = "verify:json"
    payload = {"customer": "Acme Corp", "risk": "high"}
    try:
        client.execute_command("JSON.SET", key, "$", json.dumps(payload))
        output = client.execute_command("JSON.GET", key, "$")
        client.delete(key)
        return True, f"JSON roundtrip ok ({output})"
    except Exception as exc:
        return False, f"JSON command failed: {exc}"


def check_search(client: Redis) -> tuple[bool, str]:
    index = "idx:verify"
    try:
        try:
            client.execute_command(
                "FT.CREATE",
                index,
                "ON",
                "JSON",
                "PREFIX",
                1,
                "verify:",
                "SCHEMA",
                "$.customer",
                "AS",
                "customer",
                "TEXT",
                "$.risk",
                "AS",
                "risk",
                "TAG",
            )
        except ResponseError as exc:
            if "Index already exists" not in str(exc):
                raise

        client.execute_command("JSON.SET", "verify:1", "$", '{"customer":"Acme Corp","risk":"high"}')
        results = client.execute_command("FT.SEARCH", index, "@customer:Acme")
        client.execute_command("FT.DROPINDEX", index, "DD")
        return True, f"FT.SEARCH returned: {results[0]} hits"
    except Exception as exc:
        return False, f"RediSearch check failed: {exc}"


def check_vector(client: Redis) -> tuple[bool, str]:
    index = "idx:vector:verify"
    try:
        try:
            client.execute_command(
                "FT.CREATE",
                index,
                "ON",
                "HASH",
                "PREFIX",
                1,
                "vec:",
                "SCHEMA",
                "embedding",
                "VECTOR",
                "FLAT",
                6,
                "TYPE",
                "FLOAT32",
                "DIM",
                2,
                "DISTANCE_METRIC",
                "COSINE",
            )
        except ResponseError as exc:
            if "Index already exists" not in str(exc):
                raise

        # Two float32 values encoded as bytes for a minimal vector write.
        vector = b"\x00\x00\x80?\x00\x00\x00@"
        client.hset("vec:1", mapping={"embedding": vector})
        query = "*=>[KNN 1 @embedding $vec AS score]"
        results = client.execute_command(
            "FT.SEARCH",
            index,
            query,
            "PARAMS",
            2,
            "vec",
            vector,
            "SORTBY",
            "score",
            "RETURN",
            1,
            "score",
            "DIALECT",
            2,
        )
        client.execute_command("FT.DROPINDEX", index, "DD")
        return True, f"Vector search returned: {results[0]} hits"
    except Exception as exc:
        return False, f"Vector check failed: {exc}"


def check_streams(client: Redis) -> tuple[bool, str]:
    stream = "verify:stream"
    try:
        event_id = client.xadd(stream, {"event_type": "incident_update", "status": "mitigated"})
        rows = client.xrange(stream, count=1)
        client.delete(stream)
        return True, f"stream event id={event_id.decode() if isinstance(event_id, bytes) else event_id}, rows={len(rows)}"
    except Exception as exc:
        return False, f"Streams check failed: {exc}"


def main() -> int:
    args = parse_args()
    client = Redis(host=args.host, port=args.port, decode_responses=False)

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
        ok, details = fn(client)
        print_result(name, ok, details)
        all_ok = all_ok and ok

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
