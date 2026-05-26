"use client";

import { useMemo, useState } from "react";

type RunResult = {
  summary: string;
  metrics: Record<string, number>;
};

type Props = {
  baseline: RunResult | null;
  iris: RunResult | null;
};

type Mode = "baseline" | "iris" | "comparison";

function metricValue(result: RunResult | null, key: string): number | null {
  if (!result) {
    return null;
  }
  const value = result.metrics?.[key];
  if (typeof value !== "number" || Number.isNaN(value)) {
    return null;
  }
  return value;
}

function formatMetric(value: number | null, digits = 0): string {
  if (value === null) {
    return "n/a";
  }
  return value.toFixed(digits);
}

function deltaPercent(
  baseline: number | null,
  iris: number | null,
  better: "lower" | "higher"
): string {
  if (baseline === null || iris === null || baseline === 0) {
    return "n/a";
  }
  const ratio = better === "lower" ? (baseline - iris) / baseline : (iris - baseline) / baseline;
  const sign = ratio >= 0 ? "+" : "";
  return `${sign}${(ratio * 100).toFixed(1)}%`;
}

function WorkflowModeCard({ title, result }: { title: string; result: RunResult | null }) {
  return (
    <article className="toggleModeCard">
      <h3>{title}</h3>
      <p>{result?.summary ?? "No workflow result available."}</p>
      <p>Latency: {formatMetric(metricValue(result, "latency_ms"), 0)} ms</p>
      <p>Prompt tokens: {formatMetric(metricValue(result, "prompt_tokens"), 0)}</p>
      <p>Retrieval calls: {formatMetric(metricValue(result, "retrieval_calls"), 0)}</p>
      <p>Tool calls: {formatMetric(metricValue(result, "tool_calls"), 0)}</p>
    </article>
  );
}

export default function BeforeAfterTogglePanel({ baseline, iris }: Props) {
  const [mode, setMode] = useState<Mode>("comparison");

  const deltas = useMemo(() => {
    const baselineLatency = metricValue(baseline, "latency_ms");
    const irisLatency = metricValue(iris, "latency_ms");
    const baselineTokens = metricValue(baseline, "prompt_tokens");
    const irisTokens = metricValue(iris, "prompt_tokens");
    const baselineRetrieval = metricValue(baseline, "retrieval_calls");
    const irisRetrieval = metricValue(iris, "retrieval_calls");
    const baselineTools = metricValue(baseline, "tool_calls");
    const irisTools = metricValue(iris, "tool_calls");

    return {
      latency: deltaPercent(baselineLatency, irisLatency, "lower"),
      tokens: deltaPercent(baselineTokens, irisTokens, "lower"),
      retrieval: deltaPercent(baselineRetrieval, irisRetrieval, "lower"),
      tools: deltaPercent(baselineTools, irisTools, "lower"),
    };
  }, [baseline, iris]);

  return (
    <section className="card trendPanel trendSpan2">
      <h2>Before vs After Toggle</h2>
      <p>
        Same request payload is executed in both workflows, then viewed in Baseline mode, IRIS mode, or side-by-side
        comparison.
      </p>

      <div className="toggleModeButtons" role="tablist" aria-label="Before after workflow mode">
        <button
          type="button"
          role="tab"
          aria-selected={mode === "baseline"}
          className={`toggleModeButton ${mode === "baseline" ? "isActive" : ""}`}
          onClick={() => setMode("baseline")}
        >
          Baseline Mode
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={mode === "iris"}
          className={`toggleModeButton ${mode === "iris" ? "isActive" : ""}`}
          onClick={() => setMode("iris")}
        >
          IRIS Mode
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={mode === "comparison"}
          className={`toggleModeButton ${mode === "comparison" ? "isActive" : ""}`}
          onClick={() => setMode("comparison")}
        >
          Side-by-Side
        </button>
      </div>

      {mode === "baseline" ? <WorkflowModeCard title="Baseline" result={baseline} /> : null}
      {mode === "iris" ? <WorkflowModeCard title="IRIS" result={iris} /> : null}
      {mode === "comparison" ? (
        <div className="toggleModeGrid">
          <WorkflowModeCard title="Baseline" result={baseline} />
          <WorkflowModeCard title="IRIS" result={iris} />
        </div>
      ) : null}

      <div className="toggleDeltaGrid">
        <article className="trendKpiCard">
          <h3>Latency Delta</h3>
          <p>{deltas.latency}</p>
        </article>
        <article className="trendKpiCard">
          <h3>Prompt Token Delta</h3>
          <p>{deltas.tokens}</p>
        </article>
        <article className="trendKpiCard">
          <h3>Retrieval Call Delta</h3>
          <p>{deltas.retrieval}</p>
        </article>
        <article className="trendKpiCard">
          <h3>Tool Call Delta</h3>
          <p>{deltas.tools}</p>
        </article>
      </div>
    </section>
  );
}
