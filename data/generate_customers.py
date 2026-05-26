from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path


RNG_SEED = 20260526
CUSTOMER_PREFIXES = [
    "Acme",
    "Northstar",
    "Bluewave",
    "Vertex",
    "Brightpath",
    "Summit",
    "Orbit",
    "Highland",
    "Evergreen",
    "Crestline",
]
CUSTOMER_SUFFIXES = ["Corp", "Systems", "Labs", "Solutions", "Group", "Cloud", "Tech", "Works"]
ACCOUNT_OWNERS = [
    "Sofia Patel",
    "Jordan Lee",
    "Morgan Blake",
    "Alex Kim",
    "Taylor Nguyen",
    "Riley Chen",
    "Priya Shah",
    "Noah Martinez",
]
STAKEHOLDER_FIRST_NAMES = [
    "Jordan",
    "Taylor",
    "Riley",
    "Morgan",
    "Priya",
    "Noah",
    "Avery",
    "Cameron",
    "Sofia",
    "Ethan",
    "Maya",
    "Liam",
]
STAKEHOLDER_LAST_NAMES = [
    "Lee",
    "Patel",
    "Nguyen",
    "Martinez",
    "Shah",
    "Kim",
    "Blake",
    "Chen",
    "Singh",
    "Johnson",
]
STAKEHOLDER_ROLES = [
    "VP Engineering",
    "CTO",
    "Director of IT",
    "Head of Support",
    "Platform Architect",
    "Security Lead",
]
PREFERENCES = [
    "Executive summaries first",
    "Action items with owners",
    "Timeline and risk updates",
    "Technical deep dive appendix",
]
SENTIMENTS = ["champion", "neutral", "skeptical"]
SEVERITIES = ["sev-1", "sev-2", "sev-3"]
SERVICES = ["search-api", "billing-api", "identity-api", "events-api", "sync-worker"]
INCIDENT_STATUSES = ["investigating", "mitigated", "monitoring"]
INCIDENT_TIMELINE_STAGES = ["investigating", "mitigated", "monitoring", "resolved"]
TICKET_TIMELINE_STAGES = ["open", "in_progress", "pending_customer", "resolved"]
TICKET_SUMMARIES = [
    "Latency spikes impacting executive reporting",
    "Intermittent authentication errors for admins",
    "Delayed webhook processing for CRM sync",
    "Dashboard widgets showing stale usage data",
    "Escalation path needs executive-ready update",
]
RISK_WEIGHTS = [
    ("low", 0.55),
    ("medium", 0.30),
    ("high", 0.15),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic customer seed data")
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--output", default="data/customers_seed.json")
    return parser.parse_args()


def weighted_choice(rng: random.Random) -> str:
    roll = rng.random()
    acc = 0.0
    for label, weight in RISK_WEIGHTS:
        acc += weight
        if roll <= acc:
            return label
    return RISK_WEIGHTS[-1][0]


def generate_customer(index: int, rng: random.Random) -> dict[str, object]:
    prefix = CUSTOMER_PREFIXES[index % len(CUSTOMER_PREFIXES)]
    suffix = CUSTOMER_SUFFIXES[(index // len(CUSTOMER_PREFIXES)) % len(CUSTOMER_SUFFIXES)]
    name = f"{prefix} {suffix} {index + 1:04d}"

    arr = rng.randint(60_000, 2_000_000)
    renewal_date = date(2026, 1, 1) + timedelta(days=rng.randint(0, 730))
    health_score = rng.randint(25, 96)
    risk_level = weighted_choice(rng)

    if health_score <= 40:
        risk_level = "high"
    elif health_score <= 65 and risk_level == "low":
        risk_level = "medium"

    return {
        "id": f"cust-{index + 1:04d}",
        "name": name,
        "arr": arr,
        "renewal_date": renewal_date.isoformat(),
        "health_score": health_score,
        "risk_level": risk_level,
        "account_owner": ACCOUNT_OWNERS[index % len(ACCOUNT_OWNERS)],
    }


def _stakeholder_name(index: int) -> str:
    first = STAKEHOLDER_FIRST_NAMES[index % len(STAKEHOLDER_FIRST_NAMES)]
    last = STAKEHOLDER_LAST_NAMES[(index // len(STAKEHOLDER_FIRST_NAMES)) % len(STAKEHOLDER_LAST_NAMES)]
    return f"{first} {last}"


def generate_stakeholders(customer: dict[str, object], index: int, rng: random.Random) -> list[dict[str, object]]:
    base_count = 2 + (1 if rng.random() > 0.6 else 0)
    stakeholders: list[dict[str, object]] = []
    for local_idx in range(base_count):
        global_idx = index * 3 + local_idx
        stakeholders.append(
            {
                "stakeholder_id": f"stk-{index + 1:04d}-{local_idx + 1}",
                "customer_id": customer["id"],
                "name": _stakeholder_name(global_idx),
                "role": STAKEHOLDER_ROLES[global_idx % len(STAKEHOLDER_ROLES)],
                "preference": PREFERENCES[global_idx % len(PREFERENCES)],
                "sentiment": SENTIMENTS[global_idx % len(SENTIMENTS)],
                "is_primary": local_idx == 0,
            }
        )
    return stakeholders


def generate_tickets(
    customer: dict[str, object],
    index: int,
    stakeholders: list[dict[str, object]],
    rng: random.Random,
) -> list[dict[str, object]]:
    ticket_count = 1 + (1 if rng.random() > 0.45 else 0)
    if rng.random() > 0.82:
        ticket_count += 1

    tickets: list[dict[str, object]] = []
    for local_idx in range(ticket_count):
        created_at = date(2026, 1, 1) + timedelta(days=rng.randint(0, 145))
        owner = stakeholders[local_idx % len(stakeholders)]
        timeline = _build_ticket_timeline(created_at.isoformat(), rng)
        tickets.append(
            {
                "ticket_id": f"tkt-{index + 1:04d}-{local_idx + 1}",
                "customer_id": customer["id"],
                "stakeholder_id": owner["stakeholder_id"],
                "severity": SEVERITIES[(index + local_idx) % len(SEVERITIES)],
                "summary": TICKET_SUMMARIES[(index + local_idx) % len(TICKET_SUMMARIES)],
                "status": str(timeline[-1]["status"]),
                "created_at": created_at.isoformat(),
                "timeline": timeline,
            }
        )
    return tickets


def generate_incidents(customer: dict[str, object], index: int, rng: random.Random) -> list[dict[str, object]]:
    should_emit = customer["risk_level"] == "high" or rng.random() > 0.75
    if not should_emit:
        return []

    incident_count = 1 + (1 if rng.random() > 0.88 else 0)
    incidents: list[dict[str, object]] = []
    for local_idx in range(incident_count):
        base_day = 80 + rng.randint(0, 120)
        updated = date(2026, 1, 1) + timedelta(days=base_day)
        timeline = _build_incident_timeline(updated.isoformat(), rng)
        incidents.append(
            {
                "incident_id": f"inc-{index + 1:04d}-{local_idx + 1}",
                "customer_id": customer["id"],
                "service": SERVICES[(index + local_idx) % len(SERVICES)],
                "status": str(timeline[-1]["status"]),
                "summary": "Customer-facing degradation requiring escalation and communication alignment.",
                "updated_at": f"{updated.isoformat()}T08:00:00Z",
                "timeline": timeline,
                "recurrence_count": sum(1 for entry in timeline if entry["status"] == "investigating") - 1,
            }
        )
    return incidents


def _build_ticket_timeline(created_at: str, rng: random.Random) -> list[dict[str, str]]:
    base_date = date.fromisoformat(created_at)
    stage_count = 2 + (1 if rng.random() > 0.45 else 0) + (1 if rng.random() > 0.75 else 0)
    stages = TICKET_TIMELINE_STAGES[: min(stage_count, len(TICKET_TIMELINE_STAGES))]

    timeline: list[dict[str, str]] = []
    for offset, stage in enumerate(stages):
        entry_date = base_date + timedelta(days=offset * (1 + rng.randint(0, 2)))
        timeline.append(
            {
                "timestamp": f"{entry_date.isoformat()}T09:00:00Z",
                "status": stage,
                "note": f"Ticket moved to {stage}.",
            }
        )
    return timeline


def _build_incident_timeline(base_day_iso: str, rng: random.Random) -> list[dict[str, str]]:
    base_date = date.fromisoformat(base_day_iso)
    timeline: list[dict[str, str]] = []
    stages = INCIDENT_TIMELINE_STAGES.copy()

    # High-volatility cases can reopen once before final resolution.
    if rng.random() > 0.78:
        stages.insert(2, "investigating")

    for offset, stage in enumerate(stages):
        entry_date = base_date + timedelta(days=offset)
        timeline.append(
            {
                "timestamp": f"{entry_date.isoformat()}T08:00:00Z",
                "status": stage,
                "note": f"Incident now {stage}.",
            }
        )
    return timeline


def build_event_stream(
    tickets: list[dict[str, object]],
    incidents: list[dict[str, object]],
) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []

    for ticket in tickets:
        ticket_id = str(ticket.get("ticket_id", ""))
        customer_id = str(ticket.get("customer_id", ""))
        for item in ticket.get("timeline", []):
            if not isinstance(item, dict):
                continue
            events.append(
                {
                    "event_type": "ticket_update",
                    "entity_id": ticket_id,
                    "customer_id": customer_id,
                    "status": str(item.get("status", "unknown")),
                    "timestamp": str(item.get("timestamp", "")),
                    "message": str(item.get("note", "")),
                }
            )

    for incident in incidents:
        incident_id = str(incident.get("incident_id", ""))
        customer_id = str(incident.get("customer_id", ""))
        for item in incident.get("timeline", []):
            if not isinstance(item, dict):
                continue
            events.append(
                {
                    "event_type": "incident_update",
                    "entity_id": incident_id,
                    "customer_id": customer_id,
                    "status": str(item.get("status", "unknown")),
                    "timestamp": str(item.get("timestamp", "")),
                    "message": str(item.get("note", "")),
                }
            )

    events.sort(key=lambda row: row.get("timestamp", ""))
    return events


def generate_dataset(count: int) -> dict[str, object]:
    rng = random.Random(RNG_SEED)
    customers = [generate_customer(i, rng) for i in range(count)]
    stakeholders: list[dict[str, object]] = []
    tickets: list[dict[str, object]] = []
    incidents: list[dict[str, object]] = []

    for index, customer in enumerate(customers):
        customer_stakeholders = generate_stakeholders(customer, index, rng)
        customer_tickets = generate_tickets(customer, index, customer_stakeholders, rng)
        customer_incidents = generate_incidents(customer, index, rng)

        stakeholders.extend(customer_stakeholders)
        tickets.extend(customer_tickets)
        incidents.extend(customer_incidents)

    # Preserve deterministic Acme scenario as the first record for demos.
    customers[0] = {
        "id": "cust-acme",
        "name": "Acme Corp",
        "arr": 480000,
        "renewal_date": "2026-07-15",
        "health_score": 41,
        "risk_level": "high",
        "account_owner": "Sofia Patel",
    }

    stakeholders = [
        {
            "stakeholder_id": "stk-acme-001",
            "customer_id": "cust-acme",
            "name": "Jordan Lee",
            "role": "VP Engineering",
            "preference": "Executive summaries first",
            "sentiment": "skeptical",
            "is_primary": True,
        },
        {
            "stakeholder_id": "stk-acme-002",
            "customer_id": "cust-acme",
            "name": "Avery Chen",
            "role": "Director of IT",
            "preference": "Timeline and risk updates",
            "sentiment": "neutral",
            "is_primary": False,
        },
    ] + [row for row in stakeholders if row["customer_id"] != "cust-0001"]

    incidents = [
        {
            "incident_id": "inc-2026-0412",
            "customer_id": "cust-acme",
            "service": "search-api",
            "status": "monitoring",
            "summary": "Search API p95 latency exceeded 1.8s after deployment.",
            "updated_at": "2026-05-26T08:00:00Z",
            "timeline": [
                {
                    "timestamp": "2026-05-25T07:30:00Z",
                    "status": "investigating",
                    "note": "Latency alert triggered after deployment.",
                },
                {
                    "timestamp": "2026-05-25T09:00:00Z",
                    "status": "mitigated",
                    "note": "Rollback and cache warm-up completed.",
                },
                {
                    "timestamp": "2026-05-26T08:00:00Z",
                    "status": "monitoring",
                    "note": "Service stable under monitoring window.",
                },
            ],
            "recurrence_count": 0,
        }
    ] + [row for row in incidents if row["customer_id"] != "cust-0001"]

    tickets = [
        {
            "ticket_id": "tkt-acme-001",
            "customer_id": "cust-acme",
            "stakeholder_id": "stk-acme-001",
            "severity": "sev-1",
            "summary": "Customer reports repeated outages and renewal concern.",
            "status": "in_progress",
            "created_at": "2026-05-22",
            "timeline": [
                {
                    "timestamp": "2026-05-22T09:00:00Z",
                    "status": "open",
                    "note": "Ticket opened from support escalation.",
                },
                {
                    "timestamp": "2026-05-23T11:30:00Z",
                    "status": "in_progress",
                    "note": "Incident team engaged and mitigation underway.",
                },
            ],
        },
        {
            "ticket_id": "tkt-acme-002",
            "customer_id": "cust-acme",
            "stakeholder_id": "stk-acme-002",
            "severity": "sev-2",
            "summary": "Escalation path needs executive-ready update",
            "status": "pending_customer",
            "created_at": "2026-05-24",
            "timeline": [
                {
                    "timestamp": "2026-05-24T10:00:00Z",
                    "status": "open",
                    "note": "Ticket opened for renewal communication alignment.",
                },
                {
                    "timestamp": "2026-05-24T16:00:00Z",
                    "status": "pending_customer",
                    "note": "Awaiting confirmation on executive briefing draft.",
                },
            ],
        },
    ] + [row for row in tickets if row["customer_id"] != "cust-0001"]

    event_stream = build_event_stream(tickets, incidents)

    risk_distribution = dict(Counter(str(customer["risk_level"]) for customer in customers))

    return {
        "generator": {
            "seed": RNG_SEED,
            "count": count,
            "version": 2,
            "linked_entities": {
                "customers": len(customers),
                "stakeholders": len(stakeholders),
                "tickets": len(tickets),
                "incidents": len(incidents),
            },
            "risk_distribution": risk_distribution,
        },
        "customers": customers,
        "stakeholders": stakeholders,
        "tickets": tickets,
        "incidents": incidents,
        "event_stream": event_stream,
    }


def main() -> int:
    args = parse_args()
    if args.count < 1:
        raise ValueError("count must be >= 1")

    dataset = generate_dataset(args.count)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    print(f"Generated {args.count} customers")
    print(f"Saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
