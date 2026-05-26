type TrendMetrics = {
  latency_ms_avg?: number;
  latency_ms_p95?: number;
  prompt_tokens_avg?: number;
};

type TrendEntry = {
  timestamp?: string;
  source?: string;
  report?: string;
  baseline?: TrendMetrics;
  iris?: TrendMetrics;
};

type Props = {
  entries: TrendEntry[];
};

function formatNumber(value: number | undefined, digits = 2): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "n/a";
  }
  return value.toFixed(digits);
}

function buildPolylinePoints(values: number[], width: number, height: number): string {
  if (values.length === 0) {
    return "";
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;

  return values
    .map((value, index) => {
      const x = values.length === 1 ? width / 2 : (index / (values.length - 1)) * width;
      const y = height - ((value - min) / span) * height;
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");
}

function metricSeries(entries: TrendEntry[], mode: "baseline" | "iris", metric: keyof TrendMetrics): number[] {
  return entries
    .map((entry) => entry[mode]?.[metric])
    .filter((value): value is number => typeof value === "number" && Number.isFinite(value));
}

function percentImprovement(baseline: number | undefined, iris: number | undefined): string {
  if (typeof baseline !== "number" || typeof iris !== "number" || baseline === 0) {
    return "n/a";
  }
  const delta = ((baseline - iris) / baseline) * 100;
  const sign = delta >= 0 ? "+" : "";
  return `${sign}${delta.toFixed(1)}%`;
}

export default function BenchmarkTrendPanel({ entries }: Props) {
  const last = entries[entries.length - 1];
  const baselineLatencySeries = metricSeries(entries, "baseline", "latency_ms_avg");
  const irisLatencySeries = metricSeries(entries, "iris", "latency_ms_avg");
  const baselineTokenSeries = metricSeries(entries, "baseline", "prompt_tokens_avg");
  const irisTokenSeries = metricSeries(entries, "iris", "prompt_tokens_avg");

  const width = 300;
  const height = 90;

  return (
    <section className="card trendPanel trendSpan2">
      <h2>Benchmark Trends</h2>
      <p>
        Snapshot count: {entries.length} · Latest source: {last?.source ?? "n/a"} · Latest report: {last?.report ?? "n/a"}
      </p>

      <div className="trendKpis">
        <article className="trendKpiCard">
          <h3>Latency Avg (ms)</h3>
          <p>Baseline: {formatNumber(last?.baseline?.latency_ms_avg)}</p>
          <p>IRIS: {formatNumber(last?.iris?.latency_ms_avg)}</p>
          <p>Improvement: {percentImprovement(last?.baseline?.latency_ms_avg, last?.iris?.latency_ms_avg)}</p>
        </article>
        <article className="trendKpiCard">
          <h3>P95 Latency (ms)</h3>
          <p>Baseline: {formatNumber(last?.baseline?.latency_ms_p95)}</p>
          <p>IRIS: {formatNumber(last?.iris?.latency_ms_p95)}</p>
          <p>Improvement: {percentImprovement(last?.baseline?.latency_ms_p95, last?.iris?.latency_ms_p95)}</p>
        </article>
        <article className="trendKpiCard">
          <h3>Prompt Tokens Avg</h3>
          <p>Baseline: {formatNumber(last?.baseline?.prompt_tokens_avg, 0)}</p>
          <p>IRIS: {formatNumber(last?.iris?.prompt_tokens_avg, 0)}</p>
          <p>Improvement: {percentImprovement(last?.baseline?.prompt_tokens_avg, last?.iris?.prompt_tokens_avg)}</p>
        </article>
      </div>

      <div className="trendCharts">
        <article className="trendChartCard">
          <h3>Latency Avg Trend</h3>
          <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Latency average trend chart">
            <polyline points={buildPolylinePoints(baselineLatencySeries, width, height)} className="trendLineBaseline" />
            <polyline points={buildPolylinePoints(irisLatencySeries, width, height)} className="trendLineIris" />
          </svg>
          <p className="trendLegend">Baseline (orange) · IRIS (teal)</p>
        </article>
        <article className="trendChartCard">
          <h3>Prompt Tokens Trend</h3>
          <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Prompt token trend chart">
            <polyline points={buildPolylinePoints(baselineTokenSeries, width, height)} className="trendLineBaseline" />
            <polyline points={buildPolylinePoints(irisTokenSeries, width, height)} className="trendLineIris" />
          </svg>
          <p className="trendLegend">Baseline (orange) · IRIS (teal)</p>
        </article>
      </div>
    </section>
  );
}
