import BenchmarkTrendPanel from "../components/benchmark-trend-panel";
import LiveEventsPanel from "../components/live-events-panel";
import Link from "next/link";

export default async function HomePage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  let trendEntries: Array<{
    timestamp?: string;
    source?: string;
    report?: string;
    baseline?: {
      latency_ms_avg?: number;
      latency_ms_p95?: number;
      prompt_tokens_avg?: number;
    };
    iris?: {
      latency_ms_avg?: number;
      latency_ms_p95?: number;
      prompt_tokens_avg?: number;
    };
  }> = [];
  let health = "unavailable";
  let baseline: null | {
    summary: string;
    metrics: Record<string, number>;
  } = null;
  let iris: null | {
    summary: string;
    metrics: Record<string, number>;
  } = null;

  try {
    const response = await fetch(`${apiBase}/health`, { cache: "no-store" });
    if (response.ok) {
      const payload = (await response.json()) as { status?: string };
      health = payload.status ?? "ok";
    }
  } catch {
    health = "unavailable";
  }

  try {
    const payload = {
      customer: "Acme Corp",
      message: "Our production system is down again and we are considering canceling our renewal."
    };

    const [baselineResponse, irisResponse] = await Promise.all([
      fetch(`${apiBase}/api/run/baseline`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        cache: "no-store"
      }),
      fetch(`${apiBase}/api/run/iris`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        cache: "no-store"
      })
    ]);

    if (baselineResponse.ok) {
      baseline = (await baselineResponse.json()) as {
        summary: string;
        metrics: Record<string, number>;
      };
    }

    if (irisResponse.ok) {
      iris = (await irisResponse.json()) as {
        summary: string;
        metrics: Record<string, number>;
      };
    }
  } catch {
    baseline = null;
    iris = null;
  }

  try {
    const response = await fetch(`${apiBase}/api/benchmarks/trends?limit=60`, { cache: "no-store" });
    if (response.ok) {
      const payload = (await response.json()) as {
        entries?: typeof trendEntries;
      };
      trendEntries = payload.entries ?? [];
    }
  } catch {
    trendEntries = [];
  }

  return (
    <main className="page">
      <section className="card">
        <h1>Operational AI with Redis IRIS</h1>
        <p>Foundation milestone completed. Dashboard implementation starts next.</p>
        <p>
          <Link href="/learning" className="injectButton">
            Open Learning Mode
          </Link>
        </p>
      </section>
      <section className="card">
        <h2>Service Status</h2>
        <p>Backend health: {health}</p>
      </section>
      <section className="card">
        <h2>Next Steps</h2>
        <ul>
          <li>Replace stub endpoints with live LangGraph + IRIS flows</li>
          <li>Wire Redis-backed context retrieval and memory storage</li>
          <li>Upgrade this screen to the 3-column operations dashboard</li>
        </ul>
      </section>
      <section className="card">
        <h2>Baseline</h2>
        <p>{baseline?.summary ?? "No baseline result yet (backend unavailable)."}</p>
        <p>Latency: {baseline?.metrics?.latency_ms ?? "n/a"} ms</p>
        <p>Prompt tokens: {baseline?.metrics?.prompt_tokens ?? "n/a"}</p>
        <p>Retrieval calls: {baseline?.metrics?.retrieval_calls ?? "n/a"}</p>
      </section>
      <section className="card">
        <h2>IRIS</h2>
        <p>{iris?.summary ?? "No IRIS result yet (backend unavailable)."}</p>
        <p>Latency: {iris?.metrics?.latency_ms ?? "n/a"} ms</p>
        <p>Prompt tokens: {iris?.metrics?.prompt_tokens ?? "n/a"}</p>
        <p>Retrieval calls: {iris?.metrics?.retrieval_calls ?? "n/a"}</p>
      </section>
      <BenchmarkTrendPanel entries={trendEntries} />
      <LiveEventsPanel apiBase={apiBase} />
    </main>
  );
}
