import Link from "next/link";
import LearningArchitectureDiagram, {
  type LearningArchitectureEdge,
  type LearningArchitectureNode,
  type LearningFlowStep,
} from "../../components/learning-architecture-diagram";
import { LearningAudienceQa } from "../../components/learning-audience-qa";
import { LearningFallbackScripts } from "../../components/learning-fallback-scripts";
import LearningMetricsStorytelling from "../../components/learning-metrics-storytelling";
import { LearningPresenterAnnotations } from "../../components/learning-presenter-annotations";
import { LearningQaAnchors } from "../../components/learning-qa-anchors";
import { LearningQuizCheckpoints } from "../../components/learning-quiz-checkpoints";
import { LearningSummaryHandout } from "../../components/learning-summary-handout";

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

type LearningMafPortabilityPayload = {
  status?: string;
  mapping?: Array<{
    currentComponent?: string;
    mafEquivalent?: string;
    portabilityNotes?: string;
    effort?: string;
  }>;
  migrationPlan?: string[];
  teachingSummary?: string;
};

type LearningContextDiffPayload = {
  status?: string;
  baseline?: {
    title?: string;
    summary?: string;
    packet?: {
      customer?: { name?: string; risk_level?: string; renewal_date?: string };
      facts?: string[];
      memory?: string[];
      events?: string[];
      prompt_shape?: string;
    };
  };
  iris?: {
    title?: string;
    summary?: string;
    packet?: {
      customer?: { name?: string; risk_level?: string; renewal_date?: string };
      facts?: string[];
      memory?: string[];
      events?: string[];
      prompt_shape?: string;
    };
  };
  narrative?: string[];
  delta?: {
    prompt_tokens?: {
      baseline?: number;
      iris?: number;
      change_pct?: number;
    };
    retrieval_calls?: {
      baseline?: string;
      iris?: string;
    };
    memory_continuity?: {
      baseline?: string;
      iris?: string;
    };
  };
};

type LearningMetricsStorytellingPayload = {
  status?: string;
  chapters?: Array<{
    id?: string;
    title?: string;
    narrative?: string;
    focusMetric?: string;
    kpi?: {
      label?: string;
      value?: number | string;
      unit?: string;
    };
    talkTrack?: string;
  }>;
  pacing?: {
    defaultStepMs?: number;
    recommendedAudience?: string;
    presentationHint?: string;
  };
};

type LearningAudienceQaPayload = {
  status?: string;
  questions?: Array<{
    id?: string;
    category?: string;
    question?: string;
    answer?: string;
    mappedComponents?: string[];
  }>;
  presenterHint?: string;
};

type LearningSummaryHandoutPayload = {
  status?: string;
  title?: string;
  audience?: string;
  generatedFor?: string;
  sections?: Array<{
    id?: string;
    heading?: string;
    points?: string[];
  }>;
  takeaways?: string[];
  exportMeta?: {
    format?: string;
    filename?: string;
    version?: string;
  };
};

type LearningPresenterAnnotationsPayload = {
  status?: string;
  title?: string;
  defaultTrack?: string;
  tracks?: Array<{
    id?: string;
    label?: string;
    description?: string;
    sections?: Array<{
      id?: string;
      topic?: string;
      talkTrack?: string;
      focusMetrics?: string[];
    }>;
  }>;
  presenterHint?: string;
};

type LearningFallbackScriptsPayload = {
  status?: string;
  title?: string;
  defaultScenarioId?: string;
  scenarios?: Array<{
    id?: string;
    label?: string;
    trigger?: string;
    script?: string[];
    recommendedPanel?: string;
  }>;
  presenterHint?: string;
};

type LearningQuizCheckpointsPayload = {
  status?: string;
  title?: string;
  defaultCheckpointId?: string;
  checkpoints?: Array<{
    id?: string;
    chapter?: string;
    prompt?: string;
    options?: string[];
    correctOptionIndex?: number;
    explanation?: string;
    relatedComponents?: string[];
  }>;
  presenterHint?: string;
};

type LearningQaAnchorsPayload = {
  status?: string;
  title?: string;
  anchors?: Array<{
    id?: string;
    question?: string;
    answerSummary?: string;
    sectionId?: string;
    targetLabel?: string;
  }>;
  presenterHint?: string;
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

async function loadMafPortability(apiBase: string): Promise<LearningMafPortabilityPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/maf-portability`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningMafPortabilityPayload;
  } catch {
    return null;
  }
}

async function loadContextDiff(apiBase: string): Promise<LearningContextDiffPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/context-diff`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningContextDiffPayload;
  } catch {
    return null;
  }
}

async function loadMetricsStorytelling(apiBase: string): Promise<LearningMetricsStorytellingPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/metrics-storytelling`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningMetricsStorytellingPayload;
  } catch {
    return null;
  }
}

async function loadAudienceQa(apiBase: string): Promise<LearningAudienceQaPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/audience-qa`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningAudienceQaPayload;
  } catch {
    return null;
  }
}

async function loadSummaryHandout(apiBase: string): Promise<LearningSummaryHandoutPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/summary-handout`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningSummaryHandoutPayload;
  } catch {
    return null;
  }
}

async function loadPresenterAnnotations(apiBase: string): Promise<LearningPresenterAnnotationsPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/presenter-annotations`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningPresenterAnnotationsPayload;
  } catch {
    return null;
  }
}

async function loadFallbackScripts(apiBase: string): Promise<LearningFallbackScriptsPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/fallback-scripts`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningFallbackScriptsPayload;
  } catch {
    return null;
  }
}

async function loadQuizCheckpoints(apiBase: string): Promise<LearningQuizCheckpointsPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/quiz-checkpoints`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningQuizCheckpointsPayload;
  } catch {
    return null;
  }
}

async function loadQaAnchors(apiBase: string): Promise<LearningQaAnchorsPayload | null> {
  try {
    const response = await fetch(`${apiBase}/api/learning/qa-anchors`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as LearningQaAnchorsPayload;
  } catch {
    return null;
  }
}

export default async function LearningModePage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  const [architecture, baselineFlow, irisFlow, contextPacket, metricsEducation, mafPortability, contextDiff, metricsStorytelling, audienceQa, summaryHandout, presenterAnnotations, fallbackScripts, quizCheckpoints, qaAnchors] = await Promise.all([
    loadArchitecture(apiBase),
    loadFlow(apiBase, "baseline"),
    loadFlow(apiBase, "iris"),
    loadContextPacket(apiBase),
    loadMetricsEducation(apiBase),
    loadMafPortability(apiBase),
    loadContextDiff(apiBase),
    loadMetricsStorytelling(apiBase),
    loadAudienceQa(apiBase),
    loadSummaryHandout(apiBase),
    loadPresenterAnnotations(apiBase),
    loadFallbackScripts(apiBase),
    loadQuizCheckpoints(apiBase),
    loadQaAnchors(apiBase),
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
  const portabilityMapping = mafPortability?.mapping ?? [];
  const portabilityPlan = mafPortability?.migrationPlan ?? [];
  const portabilitySummary = mafPortability?.teachingSummary ?? "";
  const diffBaseline = contextDiff?.baseline;
  const diffIris = contextDiff?.iris;
  const diffNarrative = contextDiff?.narrative ?? [];
  const diffDelta = contextDiff?.delta;
  const storyChapters = metricsStorytelling?.chapters ?? [];
  const storyPacing = metricsStorytelling?.pacing;
  const qaQuestions = (audienceQa?.questions ?? [])
    .filter((q) => q.id && q.category && q.question && q.answer)
    .map((q) => ({
      id: q.id as string,
      category: q.category as string,
      question: q.question as string,
      answer: q.answer as string,
      mappedComponents: q.mappedComponents ?? [],
    }));
  const qaPresenterHint = audienceQa?.presenterHint ?? "Use category filters to answer audience questions quickly.";
  const handoutSections = (summaryHandout?.sections ?? [])
    .filter((section) => section.id && section.heading)
    .map((section) => ({
      id: section.id as string,
      heading: section.heading as string,
      points: section.points ?? [],
    }));
  const handoutTakeaways = summaryHandout?.takeaways ?? [];
  const handoutTitle = summaryHandout?.title ?? "Operational AI Learning Summary";
  const handoutAudience = summaryHandout?.audience ?? "Stakeholders";
  const handoutGeneratedFor = summaryHandout?.generatedFor ?? "Follow-up";
  const handoutFilename = summaryHandout?.exportMeta?.filename ?? "learning-summary-handout.json";
  const annotationTracks = (presenterAnnotations?.tracks ?? [])
    .filter((track) => track.id && track.label)
    .map((track) => ({
      id: track.id as string,
      label: track.label as string,
      description: track.description ?? "",
      sections: (track.sections ?? [])
        .filter((section) => section.id && section.topic && section.talkTrack)
        .map((section) => ({
          id: section.id as string,
          topic: section.topic as string,
          talkTrack: section.talkTrack as string,
          focusMetrics: section.focusMetrics ?? [],
        })),
    }));
  const annotationTitle = presenterAnnotations?.title ?? "Presenter Annotation Mode";
  const annotationDefaultTrack = presenterAnnotations?.defaultTrack ?? "executive";
  const annotationHint = presenterAnnotations?.presenterHint ?? "Switch tracks based on audience depth.";
  const fallbackTitle = fallbackScripts?.title ?? "Guided Fallback Script Cards";
  const fallbackDefaultScenarioId = fallbackScripts?.defaultScenarioId ?? "";
  const fallbackScenarios = (fallbackScripts?.scenarios ?? [])
    .filter((scenario) => scenario.id && scenario.label && scenario.trigger)
    .map((scenario) => ({
      id: scenario.id as string,
      label: scenario.label as string,
      trigger: scenario.trigger as string,
      script: scenario.script ?? [],
      recommendedPanel: scenario.recommendedPanel ?? "Architecture Overview",
    }));
  const fallbackHint = fallbackScripts?.presenterHint ?? "Use fallback cards to keep the narrative stable when live dependencies fail.";
  const quizTitle = quizCheckpoints?.title ?? "Architecture Quiz Checkpoints";
  const quizDefaultCheckpointId = quizCheckpoints?.defaultCheckpointId ?? "";
  const quizItems = (quizCheckpoints?.checkpoints ?? [])
    .filter((item) => item.id && item.chapter && item.prompt)
    .map((item) => ({
      id: item.id as string,
      chapter: item.chapter as string,
      prompt: item.prompt as string,
      options: item.options ?? [],
      correctOptionIndex: item.correctOptionIndex ?? 0,
      explanation: item.explanation ?? "",
      relatedComponents: item.relatedComponents ?? [],
    }));
  const quizHint = quizCheckpoints?.presenterHint ?? "Use quiz checkpoints to reinforce architecture concepts between demo chapters.";
  const qaAnchorTitle = qaAnchors?.title ?? "Live Q and A Answer Anchors";
  const qaAnchorItems = (qaAnchors?.anchors ?? [])
    .filter((item) => item.id && item.question && item.sectionId)
    .map((item) => ({
      id: item.id as string,
      question: item.question as string,
      answerSummary: item.answerSummary ?? "",
      sectionId: item.sectionId as string,
      targetLabel: item.targetLabel ?? "Learning Section",
    }));
  const qaAnchorHint = qaAnchors?.presenterHint ?? "Use these links to jump to the strongest answer panel during live Q and A.";

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

      <section id="architecture-overview" className="card trendSpan2">
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
          <li>Task 9.13+: Additional Learning Mode refinements</li>
        </ul>
      </section>

      <section className="card trendSpan2" id="live-qa-answer-anchors">
        <h2>Live Q and A Answer Anchors (EPIC 9 · Task 9.12)</h2>
        <p>Fast presenter jump links for the most common audience interruptions.</p>
        <LearningQaAnchors title={qaAnchorTitle} anchors={qaAnchorItems} presenterHint={qaAnchorHint} />
      </section>

      <section id="metrics-storytelling-mode" className="card trendSpan2">
        <h2>Metrics Storytelling Mode (EPIC 9 · Enhancement)</h2>
        <p>Narrated chapter playback for executive demo pacing and KPI-focused talk track delivery.</p>
        <LearningMetricsStorytelling chapters={storyChapters} pacing={storyPacing} />
      </section>

      <section className="card trendSpan2">
        <h2>Audience Q and A Mode (EPIC 9 · Enhancement)</h2>
        <p>Pre-mapped architecture answers to common audience questions during live walkthroughs.</p>
        <LearningAudienceQa questions={qaQuestions} presenterHint={qaPresenterHint} />
      </section>

      <section className="card trendSpan2">
        <h2>Exportable Learning Summary Handout (EPIC 9 · Enhancement)</h2>
        <p>Stakeholder-ready summary of architecture outcomes with downloadable handout payload.</p>
        <LearningSummaryHandout
          title={handoutTitle}
          audience={handoutAudience}
          generatedFor={handoutGeneratedFor}
          sections={handoutSections}
          takeaways={handoutTakeaways}
          exportPayload={summaryHandout ?? { status: "unavailable" }}
          exportFilename={handoutFilename}
        />
      </section>

      <section className="card trendSpan2">
        <h2>Presenter Annotation Mode (EPIC 9 · Enhancement)</h2>
        <p>Switch between executive and technical talk tracks with topic-level speaking prompts.</p>
        <LearningPresenterAnnotations
          title={annotationTitle}
          defaultTrack={annotationDefaultTrack}
          tracks={annotationTracks}
          presenterHint={annotationHint}
        />
      </section>

      <section id="guided-fallback-script-cards" className="card trendSpan2">
        <h2>Guided Fallback Script Cards (EPIC 9 · Enhancement)</h2>
        <p>Narrator-ready fallback scripts for offline or degraded live-demo dependencies.</p>
        <LearningFallbackScripts
          title={fallbackTitle}
          defaultScenarioId={fallbackDefaultScenarioId}
          scenarios={fallbackScenarios}
          presenterHint={fallbackHint}
        />
      </section>

      <section className="card trendSpan2">
        <h2>Architecture Quiz Checkpoints (EPIC 9 · Enhancement)</h2>
        <p>Audience engagement checkpoints between chapters with immediate explanation and component mapping.</p>
        <LearningQuizCheckpoints
          title={quizTitle}
          defaultCheckpointId={quizDefaultCheckpointId}
          checkpoints={quizItems}
          presenterHint={quizHint}
        />
      </section>

      <section id="context-diff-narrative" className="card trendSpan2">
        <h2>Context Diff Narrative (EPIC 9 · Task 9.11)</h2>
        <p>Side-by-side baseline versus IRIS context packets for presenter storytelling.</p>

        <div className="learningInfoGrid">
          <article className="learningInfoCard">
            <h3>{diffBaseline?.title ?? "Baseline Context"}</h3>
            <p>{diffBaseline?.summary ?? "Local, repeated context assembly across agents."}</p>
            <p><strong>Prompt Shape:</strong> {diffBaseline?.packet?.prompt_shape ?? "-"}</p>
            <p><strong>Customer:</strong> {diffBaseline?.packet?.customer?.name ?? "-"}</p>
            <p><strong>Risk:</strong> {diffBaseline?.packet?.customer?.risk_level ?? "-"}</p>
            <ul>
              {(diffBaseline?.packet?.facts ?? []).map((item) => (
                <li key={`baseline-fact-${item}`}>{item}</li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard">
            <h3>{diffIris?.title ?? "IRIS Context"}</h3>
            <p>{diffIris?.summary ?? "Shared, compact context packet before agent reasoning."}</p>
            <p><strong>Prompt Shape:</strong> {diffIris?.packet?.prompt_shape ?? "-"}</p>
            <p><strong>Customer:</strong> {diffIris?.packet?.customer?.name ?? "-"}</p>
            <p><strong>Risk:</strong> {diffIris?.packet?.customer?.risk_level ?? "-"}</p>
            <ul>
              {(diffIris?.packet?.facts ?? []).map((item) => (
                <li key={`iris-fact-${item}`}>{item}</li>
              ))}
            </ul>
          </article>

          <article className="learningInfoCard learningInfoCardWide">
            <h3>Narrative Deltas</h3>
            <p>
              <strong>Prompt Tokens:</strong> {diffDelta?.prompt_tokens?.baseline ?? "-"} -&gt; {diffDelta?.prompt_tokens?.iris ?? "-"} ({diffDelta?.prompt_tokens?.change_pct ?? "-"}%)
            </p>
            <p>
              <strong>Retrieval Calls:</strong> {diffDelta?.retrieval_calls?.baseline ?? "-"} -&gt; {diffDelta?.retrieval_calls?.iris ?? "-"}
            </p>
            <p>
              <strong>Memory Continuity:</strong> {diffDelta?.memory_continuity?.baseline ?? "-"} -&gt; {diffDelta?.memory_continuity?.iris ?? "-"}
            </p>
            <ul>
              {diffNarrative.map((item) => (
                <li key={`narrative-${item}`}>{item}</li>
              ))}
            </ul>
          </article>
        </div>
      </section>

      <section id="context-packet-viewer" className="card trendSpan2">
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

      <section className="card trendSpan2">
        <h2>MAF Portability Mapping (EPIC 9 · Task 9.9)</h2>
        <p>Shows how this architecture ports to Microsoft Agent Framework without losing Redis IRIS operational context.</p>
        {portabilitySummary ? <p className="eventMeta">{portabilitySummary}</p> : null}

        <div className="learningInfoCard learningInfoCardWide">
          <h3>Component Mapping</h3>
          <div className="learningMappingTableWrap">
            <table className="learningMappingTable">
              <thead>
                <tr>
                  <th>Current Component</th>
                  <th>MAF Equivalent</th>
                  <th>Portability Notes</th>
                  <th>Effort</th>
                </tr>
              </thead>
              <tbody>
                {portabilityMapping.map((item) => (
                  <tr key={`${item.currentComponent}-${item.mafEquivalent}`}>
                    <td>{item.currentComponent ?? "-"}</td>
                    <td>{item.mafEquivalent ?? "-"}</td>
                    <td>{item.portabilityNotes ?? "-"}</td>
                    <td>{item.effort ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="learningInfoCard learningInfoCardWide">
          <h3>Migration Sequence</h3>
          <ol>
            {portabilityPlan.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
      </section>
    </main>
  );
}