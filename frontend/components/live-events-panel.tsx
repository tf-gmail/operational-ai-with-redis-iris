"use client";

import { useEffect, useMemo, useRef, useState } from "react";

type LiveEvent = {
  event_id?: string;
  event_type: string;
  status: string;
  customer?: string;
  message?: string | null;
  source?: string;
  timestamp?: string;
};

type Props = {
  apiBase: string;
};

type ReplayStep = {
  label: string;
  event_type: string;
  status: string;
  message: string;
  delay_ms: number;
};

type ReplayTemplate = {
  id: string;
  name: string;
  customer: string;
  description: string;
  steps: ReplayStep[];
};

type ReplayRunState = {
  run_id: string;
  template_id: string;
  template_name: string;
  status: string;
  customer: string;
  step_count: number;
  last_step_index: number;
};

function isTerminalRunStatus(status: string): boolean {
  return status === "completed" || status === "cancelled" || status === "error";
}

function toWebSocketUrl(apiBase: string): string {
  if (apiBase.startsWith("https://")) {
    return apiBase.replace("https://", "wss://") + "/ws/events";
  }
  return apiBase.replace("http://", "ws://") + "/ws/events";
}

export default function LiveEventsPanel({ apiBase }: Props) {
  const wsUrl = useMemo(() => toWebSocketUrl(apiBase), [apiBase]);
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState<LiveEvent[]>([]);
  const [templates, setTemplates] = useState<ReplayTemplate[]>([]);
  const [injecting, setInjecting] = useState(false);
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [isStartingRun, setIsStartingRun] = useState(false);
  const [isCancellingRun, setIsCancellingRun] = useState(false);
  const [activeRunId, setActiveRunId] = useState<string | null>(null);
  const [activeStepIndex, setActiveStepIndex] = useState(-1);
  const [activeRunState, setActiveRunState] = useState<ReplayRunState | null>(null);
  const [replayStatus, setReplayStatus] = useState<string>("idle");
  const pollTimerRef = useRef<number | null>(null);

  const selectedTemplate = useMemo(
    () => templates.find((template) => template.id === selectedTemplateId) ?? null,
    [selectedTemplateId, templates]
  );

  useEffect(() => {
    let cancelled = false;

    const loadTemplates = async () => {
      try {
        const response = await fetch(`${apiBase}/api/replay/templates`, { cache: "no-store" });
        if (!response.ok) {
          return;
        }
        const payload = (await response.json()) as { templates?: ReplayTemplate[] };
        const loaded = payload.templates ?? [];
        if (!cancelled) {
          setTemplates(loaded);
          setSelectedTemplateId((current) => current || loaded[0]?.id || "");
        }
      } catch {
        // Keep panel usable even if template discovery is temporarily unavailable.
      }
    };

    loadTemplates();

    return () => {
      cancelled = true;
    };
  }, [apiBase]);

  useEffect(() => {
    let closed = false;
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      if (!closed) {
        setConnected(true);
      }
    };

    socket.onclose = () => {
      if (!closed) {
        setConnected(false);
      }
    };

    socket.onerror = () => {
      if (!closed) {
        setConnected(false);
      }
    };

    socket.onmessage = (message) => {
      try {
        const parsed = JSON.parse(message.data) as LiveEvent;
        setEvents((prev) => [parsed, ...prev].slice(0, 20));
      } catch {
        // Ignore non-JSON messages.
      }
    };

    return () => {
      closed = true;
      socket.close();
    };
  }, [wsUrl]);

  const injectEvent = async (payload: { event_type: string; status: string; customer: string; message: string }) => {
    setInjecting(true);
    try {
      await fetch(`${apiBase}/api/events/inject`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    } finally {
      setInjecting(false);
    }
  };

  const injectSampleEvent = async () => {
    await injectEvent({
      event_type: "incident_update",
      status: "mitigated",
      customer: "Acme Corp",
      message: "Search API p95 recovered after mitigation rollout."
    });
  };

  const clearPollTimer = () => {
    if (pollTimerRef.current !== null) {
      window.clearTimeout(pollTimerRef.current);
      pollTimerRef.current = null;
    }
  };

  const resetTimeline = () => {
    clearPollTimer();
    setActiveRunId(null);
    setActiveRunState(null);
    setActiveStepIndex(-1);
    setReplayStatus("idle");
  };

  const runTimelineStep = async (stepIndex: number) => {
    if (!selectedTemplate || stepIndex < 0 || stepIndex >= selectedTemplate.steps.length) {
      return;
    }

    const step = selectedTemplate.steps[stepIndex];
    setActiveStepIndex(stepIndex);
    setReplayStatus(`step ${stepIndex + 1}/${selectedTemplate.steps.length}: ${step.label}`);

    try {
      const response = await fetch(`${apiBase}/api/replay/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_id: selectedTemplate.id,
          mode: "step",
          step_index: stepIndex
        })
      });
      if (!response.ok) {
        setReplayStatus("step execution failed");
      }
    } catch {
      setReplayStatus("step execution unavailable");
    }
  };

  const handleNextStep = async () => {
    if (!selectedTemplate) {
      return;
    }

    const nextStepIndex = activeStepIndex + 1;
    if (nextStepIndex >= selectedTemplate.steps.length) {
      setReplayStatus("completed");
      return;
    }

    await runTimelineStep(nextStepIndex);
  };

  useEffect(() => {
    if (!activeRunId) {
      return;
    }

    let cancelled = false;
    let inFlight = false;

    const pollStatus = async () => {
      if (cancelled || inFlight) {
        return;
      }
      inFlight = true;

      try {
        const response = await fetch(`${apiBase}/api/replay/runs/${activeRunId}`, { cache: "no-store" });
        if (!response.ok) {
          setReplayStatus("run status unavailable");
          return;
        }

        const payload = (await response.json()) as
          | { status: "ok"; run: ReplayRunState }
          | { status: string; details?: string };
        if (!("run" in payload)) {
          setReplayStatus(("details" in payload ? payload.details : undefined) ?? payload.status);
          setActiveRunId(null);
          setActiveRunState(null);
          return;
        }

        const run = payload.run;
        setActiveRunState(run);
        setActiveStepIndex(run.last_step_index);

        const completedSteps = Math.max(run.last_step_index + 1, 0);
        setReplayStatus(`run ${run.status} (${completedSteps}/${run.step_count})`);

        if (isTerminalRunStatus(run.status)) {
          setActiveRunId(null);
        }
      } catch {
        setReplayStatus("run status poll failed");
      } finally {
        inFlight = false;
      }
    };

    const schedulePoll = () => {
      if (cancelled) {
        return;
      }
      pollTimerRef.current = window.setTimeout(async () => {
        await pollStatus();
        schedulePoll();
      }, 1000);
    };

    void pollStatus();
    schedulePoll();

    return () => {
      cancelled = true;
      clearPollTimer();
    };
  }, [activeRunId, apiBase]);

  useEffect(() => {
    resetTimeline();
  }, [selectedTemplateId]);

  useEffect(() => {
    return () => {
      clearPollTimer();
    };
  }, []);

  const startReplayRun = async () => {
    if (!selectedTemplate) {
      return;
    }

    setIsStartingRun(true);
    setReplayStatus("starting replay run");
    setActiveRunState(null);
    setActiveStepIndex(-1);

    try {
      const response = await fetch(`${apiBase}/api/replay/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_id: selectedTemplate.id,
          mode: "full",
          speed_multiplier: 10
        })
      });
      if (!response.ok) {
        setReplayStatus("full replay start failed");
        return;
      }
      const payload = (await response.json()) as
        | { status: "accepted"; run: ReplayRunState }
        | { status: string; details?: string };
      if (!("run" in payload)) {
        setReplayStatus(("details" in payload ? payload.details : undefined) ?? payload.status);
        return;
      }

      const run = payload.run;
      setActiveRunState(run);
      setActiveRunId(run.run_id);
      setReplayStatus(`run ${run.status} (0/${run.step_count})`);
    } catch {
      setReplayStatus("full replay unavailable");
    } finally {
      setIsStartingRun(false);
    }
  };

  const cancelReplayRun = async () => {
    if (!activeRunId) {
      return;
    }

    setIsCancellingRun(true);
    try {
      const response = await fetch(`${apiBase}/api/replay/runs/${activeRunId}/cancel`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      if (!response.ok) {
        setReplayStatus("cancel request failed");
        return;
      }
      const payload = (await response.json()) as { status?: string; details?: string };
      setReplayStatus(payload.details ?? payload.status ?? "cancellation requested");
    } catch {
      setReplayStatus("cancel request unavailable");
    } finally {
      setIsCancellingRun(false);
    }
  };

  const runInProgress = activeRunId !== null;

  return (
    <section className="card">
      <h2>Live Events</h2>
      <p>WebSocket: {connected ? "connected" : "disconnected"}</p>
      <button className="injectButton" onClick={injectSampleEvent} disabled={injecting}>
        {injecting ? "Injecting..." : "Inject Sample Event"}
      </button>
      <div className="replayControls">
        <h3>Replay Controls</h3>
        <label className="replayLabel" htmlFor="template-select">
          Template
        </label>
        <select
          id="template-select"
          className="replaySelect"
          value={selectedTemplateId}
          onChange={(event) => setSelectedTemplateId(event.target.value)}
          disabled={runInProgress || templates.length === 0}
        >
          {templates.map((template) => (
            <option key={template.id} value={template.id}>
              {template.name}
            </option>
          ))}
        </select>
        <p className="eventMeta">
          {selectedTemplate?.description ?? "Loading replay templates from backend..."}
        </p>
        <p className="eventMeta">Replay status: {replayStatus}</p>
        <p className="eventMeta">Active run: {activeRunState?.run_id ?? "none"}</p>
        <div className="replayButtons">
          <button
            className="injectButton"
            onClick={startReplayRun}
            disabled={injecting || !selectedTemplate || runInProgress || isStartingRun}
          >
            {isStartingRun ? "Starting..." : "Play"}
          </button>
          <button
            className="injectButton"
            onClick={handleNextStep}
            disabled={injecting || !selectedTemplate || runInProgress}
          >
            Next Step
          </button>
          <button
            className="injectButton"
            onClick={cancelReplayRun}
            disabled={injecting || !runInProgress || isCancellingRun}
          >
            {isCancellingRun ? "Cancelling..." : "Cancel Run"}
          </button>
          <button className="injectButton" onClick={resetTimeline} disabled={injecting || runInProgress}>
            Reset
          </button>
        </div>
        <div className="timelineList">
          {(selectedTemplate?.steps ?? []).map((step, index) => {
            const status =
              index < activeStepIndex ? "done" : index === activeStepIndex ? "active" : "pending";
            const templateId = selectedTemplate?.id ?? "template";

            return (
              <article key={`${templateId}-${step.label}`} className={`timelineItem timeline-${status}`}>
                <p>
                  <strong>{index + 1}. {step.label}</strong>
                </p>
                <p>{step.message}</p>
                <p className="eventMeta">{step.event_type} · {step.status}</p>
              </article>
            );
          })}
        </div>
      </div>
      <div className="eventsList">
        {events.length === 0 ? <p>No events received yet.</p> : null}
        {events.map((event, index) => (
          <article key={`${event.event_id ?? event.timestamp ?? "evt"}-${index}`} className="eventItem">
            <p>
              <strong>{event.event_type}</strong> · {event.status}
            </p>
            <p>{event.message ?? "No message"}</p>
            <p className="eventMeta">
              {(event.customer ?? "unknown customer") + " | " + (event.timestamp ?? "no timestamp")}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
