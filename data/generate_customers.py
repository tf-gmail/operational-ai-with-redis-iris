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
CUSTOMER_INDUSTRIES = [
    "SaaS",
    "FinTech",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Logistics",
]
CUSTOMER_REGIONS = ["north_america", "emea", "apac", "latam"]
CONTRACT_BILLING_MODELS = ["annual_prepaid", "annual_net_30", "monthly"]
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
COMMUNICATION_CHANNELS = ["email", "slack", "teams", "phone"]
COMMUNICATION_CADENCES = ["daily", "twice-weekly", "weekly", "incident-only"]
TIMEZONES = ["America/Los_Angeles", "America/New_York", "Europe/Berlin", "Asia/Singapore"]
COMMUNICATION_STYLES = ["concise", "executive", "technical", "collaborative"]
SEVERITIES = ["sev-1", "sev-2", "sev-3"]
SERVICES = ["search-api", "billing-api", "identity-api", "events-api", "sync-worker"]
DEPLOYMENT_TRACKS = ["weekly-release", "hotfix", "infra-rollout", "schema-migration"]
IMPACT_SCOPES = ["single_customer", "regional_cluster", "shared_control_plane"]
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
TICKET_ORIGINS = ["customer_report", "incident_followup", "executive_escalation"]
TREND_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
USAGE_ANOMALIES = ["declining_adoption", "weekend_dropoff", "integration_failure_spike", "burst_usage"]
MEMORY_PROMISES = [
    "Provide executive escalation within 2 hours for sev-1 recurrences",
    "Share weekly reliability summary with incident owners",
    "Deliver customer-ready RCA within 48 hours",
    "Route renewal-risk incidents to account leadership immediately",
]
MEMORY_FRUSTRATIONS = [
    "Repeated incident updates without clear owner",
    "Escalation summaries arrive too late for leadership briefings",
    "Integration issues resurface near renewal milestones",
    "Stakeholder updates are too technical for executive audiences",
]
MEMORY_PREFERENCES = [
    "Executive summaries first",
    "Timeline and risk updates",
    "Action items with owners",
    "Technical deep dive appendix",
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


def _build_usage_profile(arr: int, risk_level: str, health_score: int, rng: random.Random) -> dict[str, object]:
    seats_provisioned = max(20, min(2200, int(arr / 2800) + rng.randint(0, 24)))

    if risk_level == "high":
        start_ratio = rng.uniform(0.42, 0.68)
        drift_min, drift_max = -0.08, -0.015
    elif risk_level == "medium":
        start_ratio = rng.uniform(0.50, 0.78)
        drift_min, drift_max = -0.04, 0.02
    else:
        start_ratio = rng.uniform(0.62, 0.90)
        drift_min, drift_max = -0.01, 0.05

    current_ratio = min(0.95, max(0.22, start_ratio + (health_score - 60) * 0.0015))

    monthly_active: list[dict[str, object]] = []
    prior_active = None
    decline_streak = 0

    for month in TREND_MONTHS:
        drift = rng.uniform(drift_min, drift_max)
        jitter = rng.uniform(-0.01, 0.01)
        current_ratio = min(0.95, max(0.16, current_ratio + drift + jitter))

        active_seats = int(seats_provisioned * current_ratio)
        if prior_active is None:
            delta_pct = 0.0
        else:
            delta_pct = round(((active_seats - prior_active) / max(prior_active, 1)) * 100, 2)
            decline_streak = decline_streak + 1 if active_seats < prior_active else 0

        monthly_active.append(
            {
                "month": month,
                "active_seats": active_seats,
                "delta_pct": delta_pct,
            }
        )
        prior_active = active_seats

    active_seats = int(monthly_active[-1]["active_seats"])
    adoption_rate = round((active_seats / max(seats_provisioned, 1)) * 100, 1)

    anomalies: list[str] = []
    if decline_streak >= 2 or (risk_level == "high" and adoption_rate < 55):
        anomalies.append("declining_adoption")
    if risk_level != "low" and rng.random() > 0.72:
        anomalies.append("integration_failure_spike")
    if risk_level == "low" and rng.random() > 0.78:
        anomalies.append("burst_usage")
    if rng.random() > 0.84:
        anomalies.append("weekend_dropoff")

    # Keep anomalies stable and deduplicated.
    deduped = []
    for anomaly in anomalies:
        if anomaly in USAGE_ANOMALIES and anomaly not in deduped:
            deduped.append(anomaly)

    return {
        "seats_provisioned": seats_provisioned,
        "active_seats": active_seats,
        "adoption_rate_pct": adoption_rate,
        "monthly_active_trend": monthly_active,
        "anomalies": deduped,
    }


def _build_memory_profile(index: int, risk_level: str, health_score: int, rng: random.Random) -> dict[str, object]:
    escalation_count = 1 + (1 if risk_level != "low" else 0) + (1 if health_score <= 45 else 0)
    has_open_commitment = risk_level == "high" or health_score <= 50 or rng.random() > 0.72

    preference = MEMORY_PREFERENCES[index % len(MEMORY_PREFERENCES)]
    promise = MEMORY_PROMISES[(index + (1 if has_open_commitment else 0)) % len(MEMORY_PROMISES)]
    frustration = MEMORY_FRUSTRATIONS[(index + (2 if risk_level == "high" else 0)) % len(MEMORY_FRUSTRATIONS)]

    memory_events = [
        {
            "timestamp": "2026-03-12T10:30:00Z",
            "type": "escalation",
            "summary": "Customer escalation triggered after reliability concern.",
        },
        {
            "timestamp": "2026-04-09T15:00:00Z",
            "type": "commitment",
            "summary": promise,
        },
        {
            "timestamp": "2026-05-04T09:45:00Z",
            "type": "preference",
            "summary": f"Preference confirmed: {preference}.",
        },
    ]

    if risk_level != "low":
        memory_events.append(
            {
                "timestamp": "2026-05-18T11:20:00Z",
                "type": "frustration",
                "summary": frustration,
            }
        )

    memory_events.sort(key=lambda item: item["timestamp"])

    return {
        "escalation_count": escalation_count,
        "open_commitment": has_open_commitment,
        "promise": promise,
        "frustration": frustration,
        "preference": preference,
        "memory_timeline": memory_events,
    }


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

    usage_profile = _build_usage_profile(arr, risk_level, health_score, rng)
    memory_profile = _build_memory_profile(index, risk_level, health_score, rng)
    account_tier = "enterprise" if arr >= 1_000_000 else "mid_market" if arr >= 300_000 else "growth"
    region = CUSTOMER_REGIONS[(index + rng.randint(0, len(CUSTOMER_REGIONS) - 1)) % len(CUSTOMER_REGIONS)]
    industry = CUSTOMER_INDUSTRIES[(index + rng.randint(0, len(CUSTOMER_INDUSTRIES) - 1)) % len(CUSTOMER_INDUSTRIES)]
    term_months = 36 if arr >= 1_200_000 else 24 if arr >= 500_000 else 12
    contract = {
        "contract_id": f"ctr-{index + 1:04d}",
        "term_months": term_months,
        "billing_model": CONTRACT_BILLING_MODELS[(index + term_months // 12) % len(CONTRACT_BILLING_MODELS)],
        "next_invoice_date": (renewal_date - timedelta(days=30)).isoformat(),
        "auto_renew": risk_level != "high",
        "sla_tier": "platinum" if arr >= 1_000_000 else "gold" if arr >= 350_000 else "silver",
    }

    return {
        "id": f"cust-{index + 1:04d}",
        "name": name,
        "arr": arr,
        "renewal_date": renewal_date.isoformat(),
        "health_score": health_score,
        "risk_level": risk_level,
        "industry": industry,
        "region": region,
        "account_tier": account_tier,
        "contract": contract,
        "account_owner": ACCOUNT_OWNERS[index % len(ACCOUNT_OWNERS)],
        "usage": usage_profile,
        "memory_profile": memory_profile,
    }


def _stakeholder_name(index: int) -> str:
    first = STAKEHOLDER_FIRST_NAMES[index % len(STAKEHOLDER_FIRST_NAMES)]
    last = STAKEHOLDER_LAST_NAMES[(index // len(STAKEHOLDER_FIRST_NAMES)) % len(STAKEHOLDER_LAST_NAMES)]
    return f"{first} {last}"


def _sentiment_for_customer(customer: dict[str, object], index: int, local_idx: int, rng: random.Random) -> str:
    risk = str(customer.get("risk_level", "medium"))
    health = int(customer.get("health_score", 60))

    if risk == "high" or health <= 45:
        weighted = ["skeptical", "neutral", "neutral", "champion"]
    elif risk == "low" and health >= 75:
        weighted = ["champion", "champion", "neutral", "skeptical"]
    else:
        weighted = ["neutral", "neutral", "champion", "skeptical"]

    return weighted[(index + local_idx + rng.randint(0, 2)) % len(weighted)]


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
                "sentiment": _sentiment_for_customer(customer, index, local_idx, rng),
                "preferred_channel": COMMUNICATION_CHANNELS[global_idx % len(COMMUNICATION_CHANNELS)],
                "update_cadence": COMMUNICATION_CADENCES[(global_idx + local_idx) % len(COMMUNICATION_CADENCES)],
                "communication_style": COMMUNICATION_STYLES[(global_idx + index) % len(COMMUNICATION_STYLES)],
                "timezone": TIMEZONES[(global_idx + local_idx) % len(TIMEZONES)],
                "response_sla_hours": 4 + ((global_idx + local_idx) % 4) * 2,
                "is_primary": local_idx == 0,
            }
        )
    return stakeholders


def generate_tickets(
    customer: dict[str, object],
    index: int,
    stakeholders: list[dict[str, object]],
    incidents: list[dict[str, object]],
    rng: random.Random,
) -> list[dict[str, object]]:
    ticket_count = 1 + (1 if rng.random() > 0.45 else 0)
    if rng.random() > 0.82:
        ticket_count += 1

    tickets: list[dict[str, object]] = []
    incident_ids = [str(incident.get("incident_id", "")) for incident in incidents if incident.get("incident_id")]

    for local_idx in range(ticket_count):
        created_at = date(2026, 1, 1) + timedelta(days=rng.randint(0, 145))
        owner = stakeholders[local_idx % len(stakeholders)]
        timeline = _build_ticket_timeline(created_at.isoformat(), rng)
        ticket_id = f"tkt-{index + 1:04d}-{local_idx + 1}"

        if local_idx > 0 and str(tickets[-1].get("severity", "")) == "sev-1":
            origin = "executive_escalation"
        elif incident_ids and (local_idx == 0 or rng.random() > 0.65):
            origin = "incident_followup"
        else:
            origin = TICKET_ORIGINS[0]

        related_incident_id = incident_ids[(index + local_idx) % len(incident_ids)] if incident_ids and origin != "customer_report" else None
        escalates_ticket_id = str(tickets[-1]["ticket_id"]) if local_idx > 0 and origin == "executive_escalation" else None

        tickets.append(
            {
                "ticket_id": ticket_id,
                "customer_id": customer["id"],
                "stakeholder_id": owner["stakeholder_id"],
                "severity": SEVERITIES[(index + local_idx) % len(SEVERITIES)],
                "summary": TICKET_SUMMARIES[(index + local_idx) % len(TICKET_SUMMARIES)],
                "origin": origin,
                "related_incident_id": related_incident_id,
                "escalates_ticket_id": escalates_ticket_id,
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
        risk_level = str(customer.get("risk_level", "medium"))
        customer_arr = int(customer.get("arr", 0))
        impact_multiplier = 0.62 if risk_level == "high" else 0.44 if risk_level == "medium" else 0.28
        affected_revenue = int(customer_arr * impact_multiplier)
        affected_seats = max(12, int(affected_revenue / 5400))

        deployment_track = DEPLOYMENT_TRACKS[(index + local_idx) % len(DEPLOYMENT_TRACKS)]
        was_deployment_triggered = (index + local_idx) % 2 == 0 or risk_level == "high"
        root_cause = (
            "deployment_failure" if was_deployment_triggered else "service_regression"
        )

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
                "impact_scope": IMPACT_SCOPES[(index + local_idx) % len(IMPACT_SCOPES)],
                "customer_impact": {
                    "affected_seats": affected_seats,
                    "affected_revenue_usd": affected_revenue,
                    "downtime_minutes": 35 + ((index + local_idx) % 7) * 9,
                    "renewal_risk_delta": 5 + ((index + local_idx) % 4) * 3,
                },
                "deployment_context": {
                    "deployment_id": f"dep-{index + 1:04d}-{local_idx + 1}",
                    "track": deployment_track,
                    "triggered_by_deployment": was_deployment_triggered,
                    "root_cause": root_cause,
                },
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
    customers: list[dict[str, object]],
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

    # Add deterministic support-note events linked to primary tickets.
    for ticket in tickets:
        customer_id = str(ticket.get("customer_id", ""))
        ticket_id = str(ticket.get("ticket_id", ""))
        status = str(ticket.get("status", "open"))
        events.append(
            {
                "event_type": "support_note",
                "entity_id": ticket_id,
                "customer_id": customer_id,
                "status": status,
                "timestamp": f"{str(ticket.get('created_at', '2026-01-01'))}T17:30:00Z",
                "message": "Support playbook updated with next escalation owner and ETA.",
            }
        )

    # Emit customer-message and deployment events for replay diversity.
    for customer in customers:
        customer_id = str(customer.get("id", ""))
        customer_name = str(customer.get("name", "Customer"))
        risk = str(customer.get("risk_level", "medium"))

        events.append(
            {
                "event_type": "customer_message",
                "entity_id": customer_id,
                "customer_id": customer_id,
                "status": "received",
                "timestamp": "2026-05-20T10:15:00Z",
                "message": f"{customer_name} requests an update on service reliability and renewal impact.",
            }
        )

        deploy_status = "degraded" if risk == "high" else "stable"
        events.append(
            {
                "event_type": "deployment_event",
                "entity_id": f"deploy-{customer_id}",
                "customer_id": customer_id,
                "status": deploy_status,
                "timestamp": "2026-05-20T11:00:00Z",
                "message": "Deployment completed; post-deploy telemetry captured for operational review.",
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
        customer_incidents = generate_incidents(customer, index, rng)
        customer_tickets = generate_tickets(customer, index, customer_stakeholders, customer_incidents, rng)

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
        "industry": "SaaS",
        "region": "north_america",
        "account_tier": "mid_market",
        "contract": {
            "contract_id": "ctr-acme",
            "term_months": 24,
            "billing_model": "annual_net_30",
            "next_invoice_date": "2026-06-15",
            "auto_renew": False,
            "sla_tier": "gold",
        },
        "account_owner": "Sofia Patel",
        "usage": {
            "seats_provisioned": 176,
            "active_seats": 82,
            "adoption_rate_pct": 46.6,
            "monthly_active_trend": [
                {"month": "2026-01", "active_seats": 124, "delta_pct": 0.0},
                {"month": "2026-02", "active_seats": 118, "delta_pct": -4.84},
                {"month": "2026-03", "active_seats": 109, "delta_pct": -7.63},
                {"month": "2026-04", "active_seats": 98, "delta_pct": -10.09},
                {"month": "2026-05", "active_seats": 90, "delta_pct": -8.16},
                {"month": "2026-06", "active_seats": 82, "delta_pct": -8.89},
            ],
            "anomalies": ["declining_adoption", "integration_failure_spike"],
        },
        "memory_profile": {
            "escalation_count": 3,
            "open_commitment": True,
            "promise": "Provide executive escalation within 2 hours for sev-1 recurrences",
            "frustration": "Escalation summaries arrive too late for leadership briefings",
            "preference": "Executive summaries first",
            "memory_timeline": [
                {
                    "timestamp": "2026-03-12T10:30:00Z",
                    "type": "escalation",
                    "summary": "Customer escalation triggered after reliability concern.",
                },
                {
                    "timestamp": "2026-04-09T15:00:00Z",
                    "type": "commitment",
                    "summary": "Provide executive escalation within 2 hours for sev-1 recurrences",
                },
                {
                    "timestamp": "2026-05-04T09:45:00Z",
                    "type": "preference",
                    "summary": "Preference confirmed: Executive summaries first.",
                },
                {
                    "timestamp": "2026-05-18T11:20:00Z",
                    "type": "frustration",
                    "summary": "Escalation summaries arrive too late for leadership briefings",
                },
            ],
        },
    }

    stakeholders = [
        {
            "stakeholder_id": "stk-acme-001",
            "customer_id": "cust-acme",
            "name": "Jordan Lee",
            "role": "VP Engineering",
            "preference": "Executive summaries first",
            "sentiment": "skeptical",
            "preferred_channel": "slack",
            "update_cadence": "daily",
            "communication_style": "executive",
            "timezone": "America/Los_Angeles",
            "response_sla_hours": 4,
            "is_primary": True,
        },
        {
            "stakeholder_id": "stk-acme-002",
            "customer_id": "cust-acme",
            "name": "Avery Chen",
            "role": "Director of IT",
            "preference": "Timeline and risk updates",
            "sentiment": "neutral",
            "preferred_channel": "email",
            "update_cadence": "twice-weekly",
            "communication_style": "technical",
            "timezone": "America/New_York",
            "response_sla_hours": 6,
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
            "impact_scope": "shared_control_plane",
            "customer_impact": {
                "affected_seats": 118,
                "affected_revenue_usd": 302000,
                "downtime_minutes": 96,
                "renewal_risk_delta": 12,
            },
            "deployment_context": {
                "deployment_id": "dep-acme-0412",
                "track": "hotfix",
                "triggered_by_deployment": True,
                "root_cause": "deployment_failure",
            },
        }
    ] + [row for row in incidents if row["customer_id"] != "cust-0001"]

    tickets = [
        {
            "ticket_id": "tkt-acme-001",
            "customer_id": "cust-acme",
            "stakeholder_id": "stk-acme-001",
            "severity": "sev-1",
            "summary": "Customer reports repeated outages and renewal concern.",
            "origin": "incident_followup",
            "related_incident_id": "inc-2026-0412",
            "escalates_ticket_id": None,
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
            "origin": "executive_escalation",
            "related_incident_id": "inc-2026-0412",
            "escalates_ticket_id": "tkt-acme-001",
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

    event_stream = build_event_stream(customers, tickets, incidents)

    risk_distribution = dict(Counter(str(customer["risk_level"]) for customer in customers))
    region_distribution = dict(Counter(str(customer["region"]) for customer in customers))
    tier_distribution = dict(Counter(str(customer["account_tier"]) for customer in customers))

    return {
        "generator": {
            "seed": RNG_SEED,
            "count": count,
            "version": 9,
            "linked_entities": {
                "customers": len(customers),
                "stakeholders": len(stakeholders),
                "tickets": len(tickets),
                "incidents": len(incidents),
            },
            "risk_distribution": risk_distribution,
            "customer_distribution": {
                "by_region": region_distribution,
                "by_account_tier": tier_distribution,
            },
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
