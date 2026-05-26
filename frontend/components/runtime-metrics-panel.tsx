type MetricsMap = Record<string, number>;

type Props = {
  baseline: MetricsMap | null;
  iris: MetricsMap | null;
};

type MetricRow = {
  key: string;
  label: string;
  better: "lower" | "higher";
};

const CORE_ROWS: MetricRow[] = [
  { key: "runtime_latency_ms", label: "Runtime Latency (ms)", better: "lower" },
  { key: "prompt_tokens_observed", label: "Prompt Tokens", better: "lower" },
  { key: "memory_hits", label: "Memory Hits", better: "higher" },
  { key: "cache_hits", label: "Cache Hits", better: "higher" },
];

const SIGNAL_ROWS: MetricRow[] = [
  { key: "retrieval_signals", label: "Retrieval Signals", better: "lower" },
  { key: "tool_signals", label: "Tool Signals", better: "lower" },
];

function metricValue(source: MetricsMap | null, key: string): number | null {
  if (!source) {
    return null;
  }
  const value = source[key];
  if (typeof value !== "number" || Number.isNaN(value)) {
    return null;
  }
  return value;
}

function formatValue(value: number | null): string {
  if (value === null) {
    return "n/a";
  }
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}

function improvementText(baseline: number | null, iris: number | null, better: "lower" | "higher"): string {
  if (baseline === null || iris === null || baseline === 0) {
    return "n/a";
  }

  const ratio = better === "lower" ? (baseline - iris) / baseline : (iris - baseline) / baseline;
  const sign = ratio >= 0 ? "+" : "";
  return `${sign}${(ratio * 100).toFixed(1)}%`;
}

function barWidth(value: number | null, max: number): string {
  if (value === null || max <= 0) {
    return "0%";
  }
  return `${Math.max(6, (value / max) * 100).toFixed(1)}%`;
}

function MetricBarRow({ baseline, iris, row }: { baseline: MetricsMap | null; iris: MetricsMap | null; row: MetricRow }) {
  const baselineValue = metricValue(baseline, row.key);
  const irisValue = metricValue(iris, row.key);
  const localMax = Math.max(baselineValue ?? 0, irisValue ?? 0, 1);

  return (
    <article className="runtimeMetricCard">
      <h3>{row.label}</h3>
      <p>Baseline: {formatValue(baselineValue)}</p>
      <p>IRIS: {formatValue(irisValue)}</p>
      <p>Improvement: {improvementText(baselineValue, irisValue, row.better)}</p>
      <div className="runtimeMetricBars" aria-hidden="true">
        <div className="runtimeMetricBar runtimeMetricBarBaseline" style={{ width: barWidth(baselineValue, localMax) }} />
        <div className="runtimeMetricBar runtimeMetricBarIris" style={{ width: barWidth(irisValue, localMax) }} />
      </div>
    </article>
  );
}

export default function RuntimeMetricsPanel({ baseline, iris }: Props) {
  return (
    <section className="card trendPanel trendSpan2">
      <h2>Runtime Metrics</h2>
      <p>Live baseline-versus-IRIS runtime instrumentation from the latest request execution.</p>

      <div className="runtimeMetricGrid">
        {CORE_ROWS.map((row) => (
          <MetricBarRow key={row.key} baseline={baseline} iris={iris} row={row} />
        ))}
      </div>

      <div className="runtimeSignalGrid">
        {SIGNAL_ROWS.map((row) => (
          <MetricBarRow key={row.key} baseline={baseline} iris={iris} row={row} />
        ))}
      </div>

      <p className="trendLegend">Top bar = Baseline · Bottom bar = IRIS</p>
    </section>
  );
}
