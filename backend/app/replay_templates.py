from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReplayStep:
    label: str
    event_type: str
    status: str
    message: str
    delay_ms: int


@dataclass(frozen=True)
class ReplayTemplate:
    id: str
    name: str
    customer: str
    description: str
    steps: tuple[ReplayStep, ...]


_REPLAY_TEMPLATES: tuple[ReplayTemplate, ...] = (
    ReplayTemplate(
        id="degradation-recovery",
        name="Latency Degradation -> Recovery",
        customer="Acme Corp",
        description="Simulates escalation, mitigation, and recovery confirmation.",
        steps=(
            ReplayStep(
                label="Detect Degradation",
                event_type="incident_update",
                status="investigating",
                message="Search API p95 exceeded 1.8s after deploy.",
                delay_ms=1000,
            ),
            ReplayStep(
                label="Escalate Customer",
                event_type="customer_escalation",
                status="open",
                message="Customer requested executive update within 30 minutes.",
                delay_ms=1200,
            ),
            ReplayStep(
                label="Mitigation Applied",
                event_type="incident_update",
                status="mitigated",
                message="Rollback and cache warm-up completed.",
                delay_ms=1200,
            ),
            ReplayStep(
                label="Recovery Confirmed",
                event_type="incident_update",
                status="resolved",
                message="Latency normalized and customer informed.",
                delay_ms=1000,
            ),
        ),
    ),
    ReplayTemplate(
        id="renewal-risk",
        name="Renewal Risk Escalation",
        customer="Acme Corp",
        description="Simulates ticket growth, stakeholder sentiment decline, and executive review.",
        steps=(
            ReplayStep(
                label="Ticket Spike",
                event_type="support_ticket",
                status="open",
                message="Two new high-priority tickets opened in one hour.",
                delay_ms=1100,
            ),
            ReplayStep(
                label="Sentiment Alert",
                event_type="stakeholder_signal",
                status="negative",
                message="VP Engineering sentiment changed to skeptical.",
                delay_ms=1200,
            ),
            ReplayStep(
                label="Renewal Risk Increase",
                event_type="account_risk",
                status="high",
                message="Renewal confidence dropped due to reliability concerns.",
                delay_ms=1300,
            ),
            ReplayStep(
                label="Executive Action Plan",
                event_type="executive_update",
                status="prepared",
                message="Executive briefing with owners and ETA drafted.",
                delay_ms=900,
            ),
        ),
    ),
    ReplayTemplate(
        id="deployment-regression",
        name="Deployment Regression Timeline",
        customer="Acme Corp",
        description="Simulates deployment issue lifecycle from detection to monitor mode.",
        steps=(
            ReplayStep(
                label="Deploy Completed",
                event_type="deployment_event",
                status="completed",
                message="search-api v2.14 deployed to production.",
                delay_ms=900,
            ),
            ReplayStep(
                label="Error Rate Alert",
                event_type="incident_update",
                status="investigating",
                message="5xx error rate crossed 4% threshold.",
                delay_ms=1000,
            ),
            ReplayStep(
                label="Rollback Executed",
                event_type="deployment_event",
                status="rollback",
                message="Rollback initiated to previous stable release.",
                delay_ms=1200,
            ),
            ReplayStep(
                label="Monitoring Stable",
                event_type="incident_update",
                status="monitoring",
                message="Post-rollback telemetry stable for 20 minutes.",
                delay_ms=1000,
            ),
        ),
    ),
)


def list_replay_templates() -> list[dict[str, Any]]:
    return [
        {
            "id": template.id,
            "name": template.name,
            "customer": template.customer,
            "description": template.description,
            "steps": [asdict(step) for step in template.steps],
        }
        for template in _REPLAY_TEMPLATES
    ]


def get_replay_template(template_id: str) -> ReplayTemplate | None:
    for template in _REPLAY_TEMPLATES:
        if template.id == template_id:
            return template
    return None
