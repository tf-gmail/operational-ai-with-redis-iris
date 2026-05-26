"use client";

import { useMemo, useState } from "react";

type FallbackScenario = {
  id: string;
  label: string;
  trigger: string;
  script: string[];
  recommendedPanel: string;
};

type LearningFallbackScriptsProps = {
  title: string;
  defaultScenarioId: string;
  scenarios: FallbackScenario[];
  presenterHint: string;
};

export function LearningFallbackScripts({
  title,
  defaultScenarioId,
  scenarios,
  presenterHint,
}: LearningFallbackScriptsProps) {
  const initialScenarioId = scenarios.find((item) => item.id === defaultScenarioId)?.id ?? scenarios[0]?.id ?? "";
  const [activeScenarioId, setActiveScenarioId] = useState<string>(initialScenarioId);

  const activeScenario = useMemo(() => {
    return scenarios.find((item) => item.id === activeScenarioId) ?? scenarios[0];
  }, [scenarios, activeScenarioId]);

  return (
    <div className="learningFallbackPanel">
      <header className="learningFallbackHeader">
        <h3>{title}</h3>
        <p>{presenterHint}</p>
      </header>

      <div className="learningFallbackButtons" role="tablist" aria-label="Fallback scenarios">
        {scenarios.map((scenario) => {
          const isActive = scenario.id === activeScenario?.id;
          return (
            <button
              key={scenario.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={`learningFallbackButton ${isActive ? "isActive" : ""}`}
              onClick={() => setActiveScenarioId(scenario.id)}
            >
              {scenario.label}
            </button>
          );
        })}
      </div>

      {activeScenario ? (
        <article className="learningInfoCard learningInfoCardWide">
          <h4>Trigger</h4>
          <p>{activeScenario.trigger}</p>
          <h4>Narration Script</h4>
          <ol>
            {activeScenario.script.map((line) => (
              <li key={`${activeScenario.id}-${line}`}>{line}</li>
            ))}
          </ol>
          <p className="eventMeta">Recommended next panel: {activeScenario.recommendedPanel}</p>
        </article>
      ) : (
        <p>No fallback scenario available.</p>
      )}
    </div>
  );
}
