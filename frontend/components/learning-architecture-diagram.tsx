"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  type Edge,
  type Node,
  type NodeMouseHandler,
} from "reactflow";
import "reactflow/dist/style.css";

export type LearningArchitectureNode = {
  id: string;
  label: string;
  category: "user" | "frontend" | "orchestrator" | "agent" | "redis" | "llm" | "metrics";
  shortDescription: string;
  responsibilities: string[];
  beforeIRIS?: string[];
  afterIRIS?: string[];
  demoValue: string[];
};

export type LearningArchitectureEdge = {
  id: string;
  source: string;
  target: string;
  kind: string;
};

export type LearningFlowStep = {
  id: string;
  title: string;
  description: string;
  activeNodes: string[];
  activeEdges: string[];
};

type LearningMode = "baseline" | "iris" | "comparison";

type LearningArchitectureDiagramProps = {
  nodes: LearningArchitectureNode[];
  edges: LearningArchitectureEdge[];
  baselineSteps: LearningFlowStep[];
  irisSteps: LearningFlowStep[];
  baselineSummary: string;
  irisSummary: string;
  apiBase: string;
};

type LearningComponentDetail = {
  id: string;
  label: string;
  role: string;
  whatItDoes: string[];
  whatItDoesNotDo: string[];
  whyRedisMatters: string[];
  beforeValue: string[];
  afterValue: string[];
  demoTalkTrack: string[];
};

type GuidedDemoStep = {
  title: string;
  instruction: string;
  mode?: LearningMode;
  stepIndex?: number;
  focusNodeId?: string;
};

const GUIDED_DEMO_STEPS: GuidedDemoStep[] = [
  {
    title: "Step 1: Submit customer outage request",
    instruction: "Run a customer outage prompt from the main demo so the audience has clear problem context.",
    mode: "comparison",
    stepIndex: 0,
    focusNodeId: "user",
  },
  {
    title: "Step 2: Watch baseline context assembly",
    instruction: "Switch to baseline and show how orchestration runs without shared operational context.",
    mode: "baseline",
    stepIndex: 1,
    focusNodeId: "langgraph",
  },
  {
    title: "Step 3: Switch to IRIS",
    instruction: "Move to IRIS mode to contrast shared retrieval and context assembly behavior.",
    mode: "iris",
    stepIndex: 1,
    focusNodeId: "context_retriever",
  },
  {
    title: "Step 4: Observe memory retrieval",
    instruction: "Highlight agent memory and explain how prior customer commitments are recalled automatically.",
    mode: "iris",
    stepIndex: 1,
    focusNodeId: "redis_agent_memory",
  },
  {
    title: "Step 5: Replay live incident event",
    instruction: "Use the Live Events replay controls, then return here to show how context and response evolve.",
  },
  {
    title: "Step 6: Observe updated response",
    instruction: "End in comparison view and emphasize updated metrics and response quality after IRIS enrichment.",
    mode: "comparison",
    stepIndex: 3,
    focusNodeId: "metrics_collector",
  },
];

const NODE_POSITIONS: Record<string, { x: number; y: number }> = {
  user: { x: 0, y: 180 },
  frontend: { x: 220, y: 180 },
  backend_api: { x: 450, y: 180 },
  langgraph: { x: 700, y: 180 },
  context_retriever: { x: 960, y: 40 },
  support_agent: { x: 960, y: 180 },
  incident_agent: { x: 960, y: 280 },
  account_agent: { x: 960, y: 380 },
  billing_agent: { x: 960, y: 480 },
  escalation_agent: { x: 1220, y: 280 },
  redis_json: { x: 1220, y: 20 },
  redis_search: { x: 1220, y: 100 },
  redis_vector_search: { x: 1220, y: 180 },
  redis_agent_memory: { x: 1220, y: 360 },
  redis_streams: { x: 1220, y: 440 },
  semantic_cache: { x: 1220, y: 520 },
  llm: { x: 1470, y: 280 },
  metrics_collector: { x: 1710, y: 280 },
};

const CATEGORY_COLORS: Record<LearningArchitectureNode["category"], string> = {
  user: "#f59f45",
  frontend: "#5fbff9",
  orchestrator: "#67d687",
  agent: "#ff7d8f",
  redis: "#29c4b7",
  llm: "#f7d154",
  metrics: "#9d89ff",
};

const EDGE_COLORS: Record<string, string> = {
  request: "#5fbff9",
  orchestration: "#67d687",
  context: "#29c4b7",
  lookup: "#29c4b7",
  memory: "#ff7d8f",
  events: "#f59f45",
  cache: "#f7d154",
  agent: "#ff7d8f",
  generation: "#f7d154",
  metrics: "#9d89ff",
  display: "#5fbff9",
};

function buildNodeStyle(node: LearningArchitectureNode, isSelected: boolean): CSSProperties {
  const color = CATEGORY_COLORS[node.category];
  return {
    width: 190,
    borderRadius: 14,
    border: `1px solid ${isSelected ? color : `${color}55`}`,
    background: isSelected ? `${color}22` : "rgba(7, 16, 19, 0.95)",
    color: "#e7f2f6",
    boxShadow: isSelected ? `0 0 0 1px ${color}55, 0 12px 30px rgba(0, 0, 0, 0.22)` : "0 10px 24px rgba(0, 0, 0, 0.18)",
    fontSize: 13,
    padding: 10,
  };
}

function collectActiveIds(steps: LearningFlowStep[]) {
  const nodeIds = new Set<string>();
  const edgeIds = new Set<string>();

  for (const step of steps) {
    for (const nodeId of step.activeNodes) {
      nodeIds.add(nodeId);
    }
    for (const edgeId of step.activeEdges) {
      edgeIds.add(edgeId);
    }
  }

  return { nodeIds, edgeIds };
}

function getComparisonRole(id: string, baselineIds: Set<string>, irisIds: Set<string>) {
  if (baselineIds.has(id) && irisIds.has(id)) {
    return "shared";
  }
  if (baselineIds.has(id)) {
    return "baseline-only";
  }
  if (irisIds.has(id)) {
    return "iris-only";
  }
  return "inactive";
}

function clampStepIndex(index: number, count: number) {
  if (count <= 0) {
    return 0;
  }
  return Math.max(0, Math.min(index, count - 1));
}

export default function LearningArchitectureDiagram({
  nodes,
  edges,
  baselineSteps,
  irisSteps,
  baselineSummary,
  irisSummary,
  apiBase,
}: LearningArchitectureDiagramProps) {
  const [mode, setMode] = useState<LearningMode>("comparison");
  const [isPlaying, setIsPlaying] = useState(false);
  const [stepIndexByMode, setStepIndexByMode] = useState<Record<LearningMode, number>>({
    baseline: 0,
    iris: 0,
    comparison: 0,
  });
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(nodes[0]?.id ?? null);
  const [componentDetail, setComponentDetail] = useState<LearningComponentDetail | null>(null);
  const [componentDetailLoading, setComponentDetailLoading] = useState(false);
  const [guidedOverlayOpen, setGuidedOverlayOpen] = useState(false);
  const [guidedStepIndex, setGuidedStepIndex] = useState(0);

  const baselineActive = useMemo(() => collectActiveIds(baselineSteps), [baselineSteps]);
  const irisActive = useMemo(() => collectActiveIds(irisSteps), [irisSteps]);

  const baselineStepCount = baselineSteps.length;
  const irisStepCount = irisSteps.length;
  const comparisonStepCount = Math.max(baselineStepCount, irisStepCount);
  const currentStepCount =
    mode === "baseline" ? baselineStepCount : mode === "iris" ? irisStepCount : comparisonStepCount;
  const currentStepIndex = clampStepIndex(stepIndexByMode[mode] ?? 0, currentStepCount);

  const activeBaselineStep = baselineSteps[clampStepIndex(stepIndexByMode.baseline, baselineStepCount)] ?? null;
  const activeIrisStep = irisSteps[clampStepIndex(stepIndexByMode.iris, irisStepCount)] ?? null;
  const activeComparisonBaselineStep = baselineSteps[clampStepIndex(stepIndexByMode.comparison, baselineStepCount)] ?? null;
  const activeComparisonIrisStep = irisSteps[clampStepIndex(stepIndexByMode.comparison, irisStepCount)] ?? null;

  const activeNodeSets = useMemo(() => {
    if (mode === "baseline") {
      return {
        baseline: new Set(activeBaselineStep?.activeNodes ?? []),
        iris: new Set<string>(),
      };
    }
    if (mode === "iris") {
      return {
        baseline: new Set<string>(),
        iris: new Set(activeIrisStep?.activeNodes ?? []),
      };
    }
    return {
      baseline: new Set(activeComparisonBaselineStep?.activeNodes ?? []),
      iris: new Set(activeComparisonIrisStep?.activeNodes ?? []),
    };
  }, [
    mode,
    activeBaselineStep,
    activeIrisStep,
    activeComparisonBaselineStep,
    activeComparisonIrisStep,
  ]);

  const activeEdgeSets = useMemo(() => {
    if (mode === "baseline") {
      return {
        baseline: new Set(activeBaselineStep?.activeEdges ?? []),
        iris: new Set<string>(),
      };
    }
    if (mode === "iris") {
      return {
        baseline: new Set<string>(),
        iris: new Set(activeIrisStep?.activeEdges ?? []),
      };
    }
    return {
      baseline: new Set(activeComparisonBaselineStep?.activeEdges ?? []),
      iris: new Set(activeComparisonIrisStep?.activeEdges ?? []),
    };
  }, [
    mode,
    activeBaselineStep,
    activeIrisStep,
    activeComparisonBaselineStep,
    activeComparisonIrisStep,
  ]);

  const currentStepTitle =
    mode === "baseline"
      ? activeBaselineStep?.title
      : mode === "iris"
        ? activeIrisStep?.title
        : `Comparison Step ${currentStepIndex + 1}`;

  const currentStepDescription =
    mode === "baseline"
      ? activeBaselineStep?.description
      : mode === "iris"
        ? activeIrisStep?.description
        : [activeComparisonBaselineStep?.description, activeComparisonIrisStep?.description]
            .filter(Boolean)
            .join(" | ");

  const modeSummary =
    mode === "baseline"
      ? baselineSummary
      : mode === "iris"
        ? irisSummary
        : "Comparison mode overlays baseline-only and IRIS-only paths to show where shared context changes the architecture.";

  const guidedStep = GUIDED_DEMO_STEPS[guidedStepIndex] ?? GUIDED_DEMO_STEPS[0];

  useEffect(() => {
    setIsPlaying(false);
  }, [mode]);

  useEffect(() => {
    if (!selectedNodeId) {
      setComponentDetail(null);
      return;
    }

    let cancelled = false;
    setComponentDetailLoading(true);

    const loadComponentDetail = async () => {
      try {
        const response = await fetch(`${apiBase}/api/learning/component/${selectedNodeId}`, { cache: "no-store" });
        if (!response.ok) {
          if (!cancelled) {
            setComponentDetail(null);
          }
          return;
        }

        const payload = (await response.json()) as
          | { status: "ok"; component: LearningComponentDetail }
          | { status: string; details?: string };
        if (cancelled) {
          return;
        }

        if ("component" in payload) {
          setComponentDetail(payload.component);
          return;
        }

        setComponentDetail(null);
      } catch {
        if (!cancelled) {
          setComponentDetail(null);
        }
      } finally {
        if (!cancelled) {
          setComponentDetailLoading(false);
        }
      }
    };

    void loadComponentDetail();

    return () => {
      cancelled = true;
    };
  }, [apiBase, selectedNodeId]);

  useEffect(() => {
    if (!isPlaying || currentStepCount <= 1) {
      return;
    }

    const handle = window.setInterval(() => {
      setStepIndexByMode((prev) => {
        const current = clampStepIndex(prev[mode] ?? 0, currentStepCount);
        if (current >= currentStepCount - 1) {
          window.clearInterval(handle);
          setIsPlaying(false);
          return prev;
        }
        return {
          ...prev,
          [mode]: current + 1,
        };
      });
    }, 1300);

    return () => window.clearInterval(handle);
  }, [isPlaying, mode, currentStepCount]);

  const goToPreviousStep = () => {
    setStepIndexByMode((prev) => ({
      ...prev,
      [mode]: clampStepIndex((prev[mode] ?? 0) - 1, currentStepCount),
    }));
  };

  const goToNextStep = () => {
    setStepIndexByMode((prev) => ({
      ...prev,
      [mode]: clampStepIndex((prev[mode] ?? 0) + 1, currentStepCount),
    }));
  };

  const resetSteps = () => {
    setIsPlaying(false);
    setStepIndexByMode((prev) => ({
      ...prev,
      [mode]: 0,
    }));
  };

  const getStepCountForMode = (targetMode: LearningMode) => {
    if (targetMode === "baseline") {
      return baselineStepCount;
    }
    if (targetMode === "iris") {
      return irisStepCount;
    }
    return comparisonStepCount;
  };

  const applyGuidedStep = (index: number) => {
    const step = GUIDED_DEMO_STEPS[index];
    if (!step) {
      return;
    }

    setIsPlaying(false);

    const targetMode = step.mode ?? mode;
    if (step.mode) {
      setMode(step.mode);
    }

    if (typeof step.stepIndex === "number") {
      const targetCount = getStepCountForMode(targetMode);
      setStepIndexByMode((prev) => ({
        ...prev,
        [targetMode]: clampStepIndex(step.stepIndex ?? 0, targetCount),
      }));
    }

    if (step.focusNodeId && nodes.some((node) => node.id === step.focusNodeId)) {
      setSelectedNodeId(step.focusNodeId);
    }
  };

  const startGuidedDemo = () => {
    setGuidedOverlayOpen(true);
    setGuidedStepIndex(0);
    applyGuidedStep(0);
  };

  const goToGuidedStep = (nextIndex: number) => {
    const boundedIndex = clampStepIndex(nextIndex, GUIDED_DEMO_STEPS.length);
    setGuidedStepIndex(boundedIndex);
    applyGuidedStep(boundedIndex);
  };

  useEffect(() => {
    if (!nodes.length) {
      setSelectedNodeId(null);
      return;
    }

    if (!selectedNodeId || !nodes.some((node) => node.id === selectedNodeId)) {
      setSelectedNodeId(nodes[0].id);
    }
  }, [nodes, selectedNodeId]);

  const selectedNode = nodes.find((node) => node.id === selectedNodeId) ?? null;

  const flowNodes = useMemo<Node[]>(
    () =>
      nodes.map((node) => {
        const baseStyle = buildNodeStyle(node, node.id === selectedNodeId);
        let style = baseStyle;

        if (mode === "baseline") {
          const isActive = activeNodeSets.baseline.has(node.id);
          style = {
            ...baseStyle,
            opacity: isActive ? 1 : 0.24,
            background: isActive ? "rgba(245, 159, 69, 0.2)" : "rgba(7, 16, 19, 0.65)",
            border: `1px solid ${isActive ? "#f59f45" : "rgba(95, 191, 249, 0.12)"}`,
          };
        } else if (mode === "iris") {
          const isActive = activeNodeSets.iris.has(node.id);
          style = {
            ...baseStyle,
            opacity: isActive ? 1 : 0.24,
            background: isActive ? "rgba(41, 196, 183, 0.2)" : "rgba(7, 16, 19, 0.65)",
            border: `1px solid ${isActive ? "#29c4b7" : "rgba(95, 191, 249, 0.12)"}`,
          };
        } else {
          const role = getComparisonRole(node.id, activeNodeSets.baseline, activeNodeSets.iris);
          if (role === "baseline-only") {
            style = {
              ...baseStyle,
              background: "rgba(245, 159, 69, 0.2)",
              border: "1px solid #f59f45",
            };
          } else if (role === "iris-only") {
            style = {
              ...baseStyle,
              background: "rgba(41, 196, 183, 0.2)",
              border: "1px solid #29c4b7",
            };
          } else if (role === "shared") {
            style = {
              ...baseStyle,
              background: "rgba(95, 191, 249, 0.2)",
              border: "1px solid #5fbff9",
            };
          } else {
            style = {
              ...baseStyle,
              opacity: 0.24,
            };
          }
        }

        return {
          id: node.id,
          position: NODE_POSITIONS[node.id] ?? { x: 0, y: 0 },
          data: {
            label: `${node.label}\n${node.category.replace("_", " ")}`,
          },
          draggable: false,
          selectable: true,
          style,
        };
      }),
    [nodes, selectedNodeId, mode, activeNodeSets.baseline, activeNodeSets.iris],
  );

  const flowEdges = useMemo<Edge[]>(
    () =>
      edges.map((edge) => {
        const isBaseline = activeEdgeSets.baseline.has(edge.id);
        const isIris = activeEdgeSets.iris.has(edge.id);

        let stroke = EDGE_COLORS[edge.kind] ?? "#5fbff9";
        let strokeWidth = 2.1;
        let opacity = 0.95;

        if (mode === "baseline") {
          stroke = isBaseline ? "#f59f45" : "rgba(95, 191, 249, 0.2)";
          strokeWidth = isBaseline ? 2.4 : 1.2;
          opacity = isBaseline ? 1 : 0.3;
        } else if (mode === "iris") {
          stroke = isIris ? "#29c4b7" : "rgba(95, 191, 249, 0.2)";
          strokeWidth = isIris ? 2.4 : 1.2;
          opacity = isIris ? 1 : 0.3;
        } else {
          const role = getComparisonRole(edge.id, activeEdgeSets.baseline, activeEdgeSets.iris);
          if (role === "baseline-only") {
            stroke = "#f59f45";
            strokeWidth = 2.5;
          } else if (role === "iris-only") {
            stroke = "#29c4b7";
            strokeWidth = 2.5;
          } else if (role === "shared") {
            stroke = "#5fbff9";
            strokeWidth = 2.2;
          } else {
            stroke = "rgba(95, 191, 249, 0.2)";
            strokeWidth = 1.2;
            opacity = 0.3;
          }
        }

        return {
          id: edge.id,
          source: edge.source,
          target: edge.target,
          label: edge.kind,
          animated:
            (mode === "baseline" && isBaseline) ||
            (mode === "iris" && isIris) ||
            (mode === "comparison" && (isBaseline || isIris)),
          style: {
            stroke,
            strokeWidth,
            opacity,
          },
          labelStyle: {
            fill: "#d2e5ec",
            fontSize: 11,
            fontWeight: 600,
          },
          labelBgStyle: {
            fill: "rgba(7, 16, 19, 0.88)",
            fillOpacity: 0.95,
          },
        };
      }),
    [edges, mode, activeEdgeSets.baseline, activeEdgeSets.iris],
  );

  const handleNodeClick = useMemo<NodeMouseHandler>(
    () => (_, node) => {
      setSelectedNodeId(node.id);
    },
    [],
  );

  if (!nodes.length) {
    return (
      <section className="learningDiagramShell">
        <article className="learningInspectorCard">
          <h3>Architecture data unavailable</h3>
          <p>The Learning Mode architecture endpoint did not return any nodes yet.</p>
        </article>
      </section>
    );
  }

  return (
    <section className="learningDiagramShell">
      <article className="learningModeToolbar">
        <div className="learningModeButtons" role="tablist" aria-label="Learning mode toggle">
          <button
            className={`learningModeButton ${mode === "baseline" ? "is-active" : ""}`}
            onClick={() => setMode("baseline")}
            type="button"
          >
            Baseline
          </button>
          <button
            className={`learningModeButton ${mode === "iris" ? "is-active" : ""}`}
            onClick={() => setMode("iris")}
            type="button"
          >
            IRIS
          </button>
          <button
            className={`learningModeButton ${mode === "comparison" ? "is-active" : ""}`}
            onClick={() => setMode("comparison")}
            type="button"
          >
            Comparison
          </button>
        </div>
        <p className="eventMeta">{modeSummary}</p>
        <p className="learningLegend">
          <span className="legendDot legendBaseline">Baseline-only path</span>
          <span className="legendDot legendIris">IRIS-only path</span>
          <span className="legendDot legendShared">Shared path</span>
        </p>
        <div className="learningPlaybackBar">
          <div className="learningPlaybackButtons">
            <button className="learningModeButton" type="button" onClick={() => setIsPlaying((prev) => !prev)}>
              {isPlaying ? "Pause" : "Play"}
            </button>
            <button
              className="learningModeButton"
              type="button"
              onClick={goToPreviousStep}
              disabled={currentStepIndex <= 0}
            >
              Previous
            </button>
            <button
              className="learningModeButton"
              type="button"
              onClick={goToNextStep}
              disabled={currentStepIndex >= Math.max(currentStepCount - 1, 0)}
            >
              Next
            </button>
            <button className="learningModeButton" type="button" onClick={resetSteps}>
              Reset
            </button>
            <button
              className={`learningModeButton ${guidedOverlayOpen ? "is-active" : ""}`}
              type="button"
              onClick={() => {
                if (guidedOverlayOpen) {
                  setGuidedOverlayOpen(false);
                  return;
                }
                startGuidedDemo();
              }}
            >
              {guidedOverlayOpen ? "Hide Guided Demo" : "Guided Demo"}
            </button>
          </div>
          <p className="eventMeta">
            Step {currentStepCount ? currentStepIndex + 1 : 0}/{currentStepCount}: {currentStepTitle ?? "No flow step loaded"}
          </p>
          <p className="eventMeta">{currentStepDescription ?? "Flow details unavailable for this mode."}</p>
        </div>
        {guidedOverlayOpen ? (
          <div className="learningGuidedOverlay">
            <p className="learningInspectorEyebrow">EPIC 9 · Task 9.8 Guided Demo</p>
            <h4>{guidedStep.title}</h4>
            <p>{guidedStep.instruction}</p>
            <p className="eventMeta">
              Guided step {guidedStepIndex + 1}/{GUIDED_DEMO_STEPS.length}
            </p>
            <div className="learningPlaybackButtons">
              <button
                className="learningModeButton"
                type="button"
                onClick={() => goToGuidedStep(guidedStepIndex - 1)}
                disabled={guidedStepIndex <= 0}
              >
                Previous Guided Step
              </button>
              <button
                className="learningModeButton"
                type="button"
                onClick={() => goToGuidedStep(guidedStepIndex + 1)}
                disabled={guidedStepIndex >= GUIDED_DEMO_STEPS.length - 1}
              >
                Next Guided Step
              </button>
              <button className="learningModeButton" type="button" onClick={() => startGuidedDemo()}>
                Restart Guided Demo
              </button>
            </div>
          </div>
        ) : null}
      </article>

      <div className="learningDiagramCanvas">
        <ReactFlow
          nodes={flowNodes}
          edges={flowEdges}
          onNodeClick={handleNodeClick}
          fitView
          minZoom={0.45}
          maxZoom={1.4}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable
          proOptions={{ hideAttribution: true }}
        >
          <MiniMap
            pannable
            zoomable
            nodeColor={(node) => {
              const selected = nodes.find((item) => item.id === node.id);
              return selected ? CATEGORY_COLORS[selected.category] : "#5fbff9";
            }}
            maskColor="rgba(7, 16, 19, 0.72)"
          />
          <Controls showInteractive={false} />
          <Background color="rgba(95, 191, 249, 0.18)" gap={18} />
        </ReactFlow>
      </div>

      <aside className="learningInspectorCard">
        <p className="learningInspectorEyebrow">EPIC 9 · Task 9.2 / 9.3 / 9.4 / 9.5 / 9.8</p>
        <h3>{componentDetail?.label ?? selectedNode?.label ?? "Component Inspector"}</h3>
        <p>{componentDetail?.role ?? selectedNode?.shortDescription ?? "Select a node to inspect its role in the architecture."}</p>
        {componentDetailLoading ? <p className="eventMeta">Loading component details...</p> : null}

        <div className="learningInspectorSection">
          <h4>Mode Lens</h4>
          {mode === "baseline" ? (
            <p>{selectedNode?.beforeIRIS?.[0] ?? "Baseline view emphasizes fragmented retrieval and repeated context assembly."}</p>
          ) : null}
          {mode === "iris" ? (
            <p>{selectedNode?.afterIRIS?.[0] ?? "IRIS view emphasizes shared operational context and compact retrieval."}</p>
          ) : null}
          {mode === "comparison" ? (
            <p>
              {(selectedNode?.beforeIRIS?.[0] ?? "Baseline: fragmented and local context") +
                " | " +
                (selectedNode?.afterIRIS?.[0] ?? "IRIS: shared operational context")}
            </p>
          ) : null}
        </div>

        <div className="learningInspectorSection">
          <h4>Responsibilities</h4>
          <ul>
            {(componentDetail?.whatItDoes?.length ? componentDetail.whatItDoes : selectedNode?.responsibilities ?? []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="learningInspectorSection">
          <h4>What It Does Not Do</h4>
          <ul>
            {(componentDetail?.whatItDoesNotDo?.length ? componentDetail.whatItDoesNotDo : ["Details not available for this component yet."]).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        {componentDetail?.whyRedisMatters?.length ? (
          <div className="learningInspectorSection">
            <h4>Why Redis Matters</h4>
            <ul>
              {componentDetail.whyRedisMatters.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        <div className="learningInspectorSection">
          <h4>Before IRIS</h4>
          <ul>
            {(componentDetail?.beforeValue?.length ? componentDetail.beforeValue : selectedNode?.beforeIRIS?.length ? selectedNode.beforeIRIS : ["No explicit baseline note recorded for this component."]).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="learningInspectorSection">
          <h4>After IRIS</h4>
          <ul>
            {(componentDetail?.afterValue?.length ? componentDetail.afterValue : selectedNode?.afterIRIS?.length ? selectedNode.afterIRIS : ["This component participates in the shared operational-state path."]).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="learningInspectorSection">
          <h4>Demo Talk Track</h4>
          <ul>
            {(componentDetail?.demoTalkTrack?.length ? componentDetail.demoTalkTrack : selectedNode?.demoValue ?? []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </aside>
    </section>
  );
}