import Link from "next/link";
import LearningArchitectureDiagram, {
  type LearningArchitectureEdge,
  type LearningArchitectureNode,
  type LearningFlowStep,
} from "../../components/learning-architecture-diagram";

type LearningArchitecturePayload = {
  status?: string;
  nodes?: LearningArchitectureNode[];
  edges?: LearningArchitectureEdge[];
};

type LearningFlowPayload = {
  status?: string;
  mode?: "baseline" | "iris";
  summary?: string;
  steps?: LearningFlowStep[];
};

type LearningContextPacketPayload = {
  status?: string;
  packet?: {
    customer?: {
      name?: string;
      arr?: number;
      renewal_date?: string;
      risk_level?: string;
      health_score?: number;
    };
    structured_facts?: string[];
    memory_hits?: string[];
    semantic_matches?: Array<{ incident_id?: string; similarity?: number; summary?: string }>;
    live_events?: Array<{ event_type?: string; status?: string; message?: string }>;
    prompt_estimate?: {
      baseline_prompt_tokens?: number;
      iris_prompt_tokens?: number;
      savings_tokens?: number;
      savings_pct?: number;
    };
  };
};

type LearningMetricsEducationPayload = {
  status?: string;
  metrics?: {
    baseline?: {
      latency_ms_avg?: number;
      latency_ms_p95?: number;
      prompt_tokens_avg?: number;
      memory_hits?: number;
      cache_hits?: number;
    };
    iris?: {
      latency_ms_avg?: number;
      latency_ms_p95?: number;
      prompt_tokens_avg?: number;
      memory_hits?: number;
      cache_hits?: number;
    };
    education?: Array<{ title?: string; explanation?: string }>;
  };
};

async function loadArchitecture(apiBase: string): Promise<LearningArchitecturePayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/architecture`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }

    return (await response.json()) as LearningArchitecturePayload;
  } catch {
    return null;
  }
}

async function loadFlow(apiBase: string, mode: "baseline" | "iris"): Promise<LearningFlowPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/flow/${mode}`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningFlowPayload;
  } catch {
    return null;
  }
}

async function loadContextPacket(apiBase: string): Promise<LearningContextPacketPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/context-packet`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningContextPacketPayload;
  } catch {
    return null;
  }
}

async function loadMetricsEducation(apiBase: string): Promise<LearningMetricsEducationPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/metrics-education`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningMetricsEducationPayload;
  } catch {
    return null;
  }
}

export default async function LearningModePage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const [architecture, baselineFlow, irisFlow, contextPacket, metricsEducation] = await Promise.all([
    loadArchitecture(apiBase),
    loadFlow(apiBase, "baseline"),
    loadFlow(apiBase, "iris"),
    loadContextPacket(apiBase),
    loadMetricsEducation(apiBase),
  ]);
  const nodes = architecture?.nodes ?? [];
  const edges = architecture?.edges ?? [];
  const baselineSteps = baselineFlow?.steps ?? [];
  const irisSteps = irisFlow?.steps ?? [];
  const baselineSummary = baselineFlow?.summary ?? "Baseline mode highlights fragmented retrieval and repeated context assembly.";
  const irisSummary = irisFlow?.summary ?? "IRIS mode highlights shared operational context and compact prompt assembly.";
  const packet = contextPacket?.packet;
  const packetFacts = packet?.structured_facts ?? [];
  const packetMemoryHits = packet?.memory_hits ?? [];
  const packetMatches = packet?.semantic_matches ?? [];
  const packetEvents = packet?.live_events ?? [];
  const promptEstimate = packet?.prompt_estimate;
  const metrics = metricsEducation?.metrics;
  const baselineMetrics = metrics?.baseline;
  const irisMetrics = metrics?.iris;
  const educationPoints = metrics?.education ?? [];

  return (
    <main className="page">
      <section className="card trendSpan2">
        <h1>Learning Mode</h1>
        <p>
          Interactive architecture explorer for understanding how baseline and IRIS flows differ.
        </p>
        <p>
          EPIC 9 Task 9.3 now adds Baseline, IRIS, and Comparison toggles so the architecture view clearly contrasts
          fragmented and shared-context paths.
        </p>
        <p>
          <Link href="/" className="injectButton">
            Back to Main Demo
          </Link>
        </p>
      </section>

      <section className="card trendSpan2">
        <h2>Architecture Overview</h2>
        <p>
          Planned flow: User -&gt; Frontend -&gt; Backend API -&gt; LangGraph -&gt; Agents -&gt; Redis IRIS Context Layer -&gt; LLM.
        </p>
        <LearningArchitectureDiagram
          nodes={nodes}
          edges={edges}
          baselineSteps={baselineSteps}
          irisSteps={irisSteps}
          baselineSummary={baselineSummary}
          irisSummary={irisSummary}
          apiBase={apiBase}
        />
      </section>

      <section className="card">
        <h2>Before IRIS</h2>
        <p>Fragmented retrieval, duplicated context assembly, weaker memory continuity.</p>
      </section>

      <section className="card">
        <h2>With Redis IRIS</h2>
        <p>Shared operational context, compact context packets, memory and cache-aware flows.</p>
      </section>

      <section className="card">
        <h2>Upcoming Tasks</h2>
        <ul>
          <li>Task 9.9: MAF portability mapping panel</li>
          <li>Task 9.10: Presenter auto-tour mode</li>
          <li>Task 9.11: Baseline-vs-IRIS context diff narrative</li>
        </ul>
      </section>

      <section className="card trendSpan2">
        <h2>Context Packet Viewer (EPIC 9 · Task 9.6)</h2>
        <p>Shows what IRIS sends into the LLM before response generation.</p>

        <div className="learningInfoGrid">
          <article className="learningInfoCard">
            <h3>Customer Snapshot</h3>
            <p><strong>Name:</strong> {packet?.customer?.name ?? "-"}</p>
            <p><strong>ARR:</strong> {packet?.customer?.arr ?? "-"}</p>
            <p><strong>Renewal:</strong> {packet?.customer?.renewal_date ?? "-"}</p>
            <p><strong>Risk:</strong> {packet?.customer?.risk_level ?? "-"}</p>
            <p><strong>Health:</strong> {packet?.customer?.health_score ?? "-"}</p>
          </article>

          <article className="learningInfoCard">
            <h3>Structured Facts</h3>
            <ul>
              {packetFacts.map((fact) => (
                <li key={fact}>{fact}</li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard">
            <h3>Memory Hits</h3>
            <ul>
              {packetMemoryHits.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard">
            <h3>Semantic Matches</h3>
            <ul>
              {packetMatches.map((match) => (
                <li key={`${match.incident_id}-${match.summary}`}>
                  {match.incident_id ?? "incident"} ({match.similarity ?? "-"}): {match.summary ?? "-"}
                </li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard">
            <h3>Live Events</h3>
            <ul>
              {packetEvents.map((event) => (
                <li key={`${event.event_type}-${event.message}`}>
                  {event.event_type ?? "event"} / {event.status ?? "-"}: {event.message ?? "-"}
                </li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard">
            <h3>Prompt Estimate</h3>
            <p><strong>Baseline Tokens:</strong> {promptEstimate?.baseline_prompt_tokens ?? "-"}</p>
            <p><strong>IRIS Tokens:</strong> {promptEstimate?.iris_prompt_tokens ?? "-"}</p>
            <p><strong>Savings:</strong> {promptEstimate?.savings_tokens ?? "-"}</p>
            <p><strong>Savings %:</strong> {promptEstimate?.savings_pct ?? "-"}</p>
          </article>
        </div>
      </section>

      <section className="card trendSpan2">
        <h2>Metrics Education Panel (EPIC 9 · Task 9.7)</h2>
        <p>Plain-language explanation of why IRIS improves both cost and speed.</p>

        <div className="learningInfoGrid">
          <article className="learningInfoCard">
            <h3>Baseline Snapshot</h3>
            <p><strong>Latency Avg (ms):</strong> {baselineMetrics?.latency_ms_avg ?? "-"}</p>
            <p><strong>Latency P95 (ms):</strong> {baselineMetrics?.latency_ms_p95 ?? "-"}</p>
            <p><strong>Prompt Tokens:</strong> {baselineMetrics?.prompt_tokens_avg ?? "-"}</p>
            <p><strong>Memory Hits:</strong> {baselineMetrics?.memory_hits ?? "-"}</p>
            <p><strong>Cache Hits:</strong> {baselineMetrics?.cache_hits ?? "-"}</p>
          </article>

          <article className="learningInfoCard">
            <h3>IRIS Snapshot</h3>
            <p><strong>Latency Avg (ms):</strong> {irisMetrics?.latency_ms_avg ?? "-"}</p>
            <p><strong>Latency P95 (ms):</strong> {irisMetrics?.latency_ms_p95 ?? "-"}</p>
            <p><strong>Prompt Tokens:</strong> {irisMetrics?.prompt_tokens_avg ?? "-"}</p>
            <p><strong>Memory Hits:</strong> {irisMetrics?.memory_hits ?? "-"}</p>
            <p><strong>Cache Hits:</strong> {irisMetrics?.cache_hits ?? "-"}</p>
          </article>

          <article className="learningInfoCard learningInfoCardWide">
            <h3>Why These Metrics Matter</h3>
            <ul>
              {educationPoints.map((point) => (
                <li key={point.title}>
                  <strong>{point.title ?? "Insight"}:</strong> {point.explanation ?? "-"}
                </li>
              ))}
            </ul>
          </article>
        </div>
      </section>
    </main>
  );
}