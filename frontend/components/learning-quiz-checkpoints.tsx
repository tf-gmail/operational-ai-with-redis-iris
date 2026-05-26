"use client";

import { useMemo, useState } from "react";

type QuizCheckpoint = {
  id: string;
  chapter: string;
  prompt: string;
  options: string[];
  correctOptionIndex: number;
  explanation: string;
  relatedComponents: string[];
};

type LearningQuizCheckpointsProps = {
  title: string;
  defaultCheckpointId: string;
  checkpoints: QuizCheckpoint[];
  presenterHint: string;
};

export function LearningQuizCheckpoints({
  title,
  defaultCheckpointId,
  checkpoints,
  presenterHint,
}: LearningQuizCheckpointsProps) {
  const initialCheckpointId = checkpoints.find((item) => item.id === defaultCheckpointId)?.id ?? checkpoints[0]?.id ?? "";
  const [activeCheckpointId, setActiveCheckpointId] = useState<string>(initialCheckpointId);
  const [selectedOptionIndex, setSelectedOptionIndex] = useState<number | null>(null);
  const [isRevealed, setIsRevealed] = useState<boolean>(false);

  const activeCheckpoint = useMemo(() => {
    return checkpoints.find((item) => item.id === activeCheckpointId) ?? checkpoints[0];
  }, [checkpoints, activeCheckpointId]);

  function chooseCheckpoint(id: string) {
    setActiveCheckpointId(id);
    setSelectedOptionIndex(null);
    setIsRevealed(false);
  }

  function revealAnswer() {
    if (selectedOptionIndex === null) {
      return;
    }
    setIsRevealed(true);
  }

  return (
    <div className="learningQuizPanel">
      <header className="learningQuizHeader">
        <h3>{title}</h3>
        <p>{presenterHint}</p>
      </header>

      <div className="learningQuizChips" role="tablist" aria-label="Quiz checkpoints">
        {checkpoints.map((checkpoint) => {
          const isActive = checkpoint.id === activeCheckpoint?.id;
          return (
            <button
              key={checkpoint.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={`learningQuizChip ${isActive ? "isActive" : ""}`}
              onClick={() => chooseCheckpoint(checkpoint.id)}
            >
              {checkpoint.chapter}
            </button>
          );
        })}
      </div>

      {activeCheckpoint ? (
        <article className="learningInfoCard learningInfoCardWide">
          <p className="eventMeta">Checkpoint: {activeCheckpoint.chapter}</p>
          <h4>{activeCheckpoint.prompt}</h4>
          <div className="learningQuizOptions" role="radiogroup" aria-label="Quiz answer options">
            {activeCheckpoint.options.map((option, index) => {
              const isSelected = selectedOptionIndex === index;
              const isCorrect = activeCheckpoint.correctOptionIndex === index;
              const isWrongSelection = isRevealed && isSelected && !isCorrect;
              const isCorrectReveal = isRevealed && isCorrect;
              return (
                <button
                  key={`${activeCheckpoint.id}-${option}`}
                  type="button"
                  role="radio"
                  aria-checked={isSelected}
                  className={`learningQuizOption ${isSelected ? "isSelected" : ""} ${isWrongSelection ? "isWrong" : ""} ${isCorrectReveal ? "isCorrect" : ""}`}
                  onClick={() => {
                    if (!isRevealed) {
                      setSelectedOptionIndex(index);
                    }
                  }}
                  disabled={isRevealed}
                >
                  {option}
                </button>
              );
            })}
          </div>
          <div className="learningQuizActions">
            <button
              type="button"
              className="injectButton"
              onClick={revealAnswer}
              disabled={selectedOptionIndex === null || isRevealed}
            >
              Reveal Answer
            </button>
            <button
              type="button"
              className="injectButton"
              onClick={() => {
                setSelectedOptionIndex(null);
                setIsRevealed(false);
              }}
            >
              Reset
            </button>
          </div>

          {isRevealed ? (
            <div className="learningQuizExplanation">
              <p>
                <strong>Explanation:</strong> {activeCheckpoint.explanation}
              </p>
              <div className="learningQuizComponents">
                {activeCheckpoint.relatedComponents.map((component) => (
                  <span key={`${activeCheckpoint.id}-${component}`}>{component}</span>
                ))}
              </div>
            </div>
          ) : null}
        </article>
      ) : (
        <p>No quiz checkpoints available.</p>
      )}
    </div>
  );
}
