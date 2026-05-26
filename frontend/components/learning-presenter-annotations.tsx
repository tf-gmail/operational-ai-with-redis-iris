"use client";

import { useMemo, useState } from "react";

type AnnotationSection = {
  id: string;
  topic: string;
  talkTrack: string;
  focusMetrics: string[];
};

type AnnotationTrack = {
  id: string;
  label: string;
  description: string;
  sections: AnnotationSection[];
};

type LearningPresenterAnnotationsProps = {
  title: string;
  defaultTrack: string;
  tracks: AnnotationTrack[];
  presenterHint: string;
};

export function LearningPresenterAnnotations({
  title,
  defaultTrack,
  tracks,
  presenterHint,
}: LearningPresenterAnnotationsProps) {
  const initialTrack = tracks.find((track) => track.id === defaultTrack)?.id ?? tracks[0]?.id ?? "";
  const [activeTrackId, setActiveTrackId] = useState<string>(initialTrack);

  const activeTrack = useMemo(() => {
    return tracks.find((track) => track.id === activeTrackId) ?? tracks[0];
  }, [tracks, activeTrackId]);

  return (
    <div className="learningAnnotationPanel">
      <header className="learningAnnotationHeader">
        <h3>{title}</h3>
        <p>{presenterHint}</p>
      </header>

      <div className="learningAnnotationTrackButtons" role="tablist" aria-label="Presenter annotation tracks">
        {tracks.map((track) => {
          const isActive = track.id === activeTrack?.id;
          return (
            <button
              key={track.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={`learningAnnotationTrackButton ${isActive ? "isActive" : ""}`}
              onClick={() => setActiveTrackId(track.id)}
            >
              {track.label}
            </button>
          );
        })}
      </div>

      {activeTrack ? (
        <>
          <p className="eventMeta">{activeTrack.description}</p>
          <div className="learningAnnotationGrid">
            {activeTrack.sections.map((section) => (
              <article key={section.id} className="learningInfoCard">
                <h4>{section.topic}</h4>
                <p>{section.talkTrack}</p>
                <div className="learningAnnotationMetrics">
                  {section.focusMetrics.map((metric) => (
                    <span key={`${section.id}-${metric}`}>{metric}</span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </>
      ) : (
        <p>No annotation track available.</p>
      )}
    </div>
  );
}
