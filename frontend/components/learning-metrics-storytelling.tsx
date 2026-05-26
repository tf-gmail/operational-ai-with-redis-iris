"use client";

import { useEffect, useMemo, useState } from "react";

type StoryChapter = {
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
};

type StoryPacing = {
  defaultStepMs?: number;
  recommendedAudience?: string;
  presentationHint?: string;
};

type LearningMetricsStorytellingProps = {
  chapters: StoryChapter[];
  pacing?: StoryPacing;
};

function clamp(index: number, count: number) {
  if (count <= 0) {
    return 0;
  }
  return Math.max(0, Math.min(index, count - 1));
}

export default function LearningMetricsStorytelling({ chapters, pacing }: LearningMetricsStorytellingProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const total = chapters.length;
  const stepMs = Math.max(1200, pacing?.defaultStepMs ?? 3500);
  const boundedIndex = clamp(activeIndex, total);
  const active = chapters[boundedIndex];

  useEffect(() => {
    if (!isPlaying || total <= 1) {
      return;
    }

    if (boundedIndex >= total - 1) {
      setIsPlaying(false);
      return;
    }

    const handle = window.setTimeout(() => {
      setActiveIndex((prev) => clamp(prev + 1, total));
    }, stepMs);

    return () => window.clearTimeout(handle);
  }, [isPlaying, boundedIndex, total, stepMs]);

  const storyProgress = useMemo(() => {
    if (!total) {
      return "0/0";
    }
    return `${boundedIndex + 1}/${total}`;
  }, [boundedIndex, total]);

  if (!total) {
    return (
      <article className="learningStoryPanel">
        <h3>Narrated Metrics Storytelling</h3>
        <p className="eventMeta">No storytelling chapters available yet.</p>
      </article>
    );
  }

  return (
    <article className="learningStoryPanel">
      <div className="learningStoryHeader">
        <h3>Narrated Metrics Storytelling</h3>
        <p className="eventMeta">
          Chapter {storyProgress} | Pace {Math.round(stepMs / 100) / 10}s | Audience {pacing?.recommendedAudience ?? "mixed"}
        </p>
      </div>

      <div className="learningPlaybackButtons">
        <button className="learningModeButton" type="button" onClick={() => setIsPlaying((prev) => !prev)}>
          {isPlaying ? "Pause Story" : "Play Story"}
        </button>
        <button
          className="learningModeButton"
          type="button"
          disabled={boundedIndex <= 0}
          onClick={() => {
            setIsPlaying(false);
            setActiveIndex((prev) => clamp(prev - 1, total));
          }}
        >
          Previous Chapter
        </button>
        <button
          className="learningModeButton"
          type="button"
          disabled={boundedIndex >= total - 1}
          onClick={() => {
            setIsPlaying(false);
            setActiveIndex((prev) => clamp(prev + 1, total));
          }}
        >
          Next Chapter
        </button>
        <button
          className="learningModeButton"
          type="button"
          onClick={() => {
            setIsPlaying(false);
            setActiveIndex(0);
          }}
        >
          Reset Story
        </button>
      </div>

      <div className="learningStoryBody">
        <h4>{active?.title ?? "Story Chapter"}</h4>
        <p>{active?.narrative ?? "Narrative details unavailable."}</p>
        <p>
          <strong>Focus Metric:</strong> {active?.focusMetric ?? "-"}
        </p>
        <p>
          <strong>KPI:</strong> {active?.kpi?.label ?? "-"} = {active?.kpi?.value ?? "-"} {active?.kpi?.unit ?? ""}
        </p>
        <p>
          <strong>Talk Track:</strong> {active?.talkTrack ?? "-"}
        </p>
      </div>

      {pacing?.presentationHint ? <p className="eventMeta">Hint: {pacing.presentationHint}</p> : null}
    </article>
  );
}
