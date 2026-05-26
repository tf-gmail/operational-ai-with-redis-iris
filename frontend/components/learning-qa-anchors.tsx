"use client";

type LearningQaAnchor = {
  id: string;
  question: string;
  answerSummary: string;
  sectionId: string;
  targetLabel: string;
};

type LearningQaAnchorsProps = {
  title: string;
  anchors: LearningQaAnchor[];
  presenterHint: string;
};

export function LearningQaAnchors({ title, anchors, presenterHint }: LearningQaAnchorsProps) {
  return (
    <div className="learningAnchorPanel">
      <header className="learningAnchorHeader">
        <h3>{title}</h3>
        <p>{presenterHint}</p>
      </header>

      <div className="learningAnchorGrid">
        {anchors.map((anchor) => (
          <article key={anchor.id} className="learningInfoCard">
            <p className="learningQaPrompt">{anchor.question}</p>
            <p>{anchor.answerSummary}</p>
            <a href={`#${anchor.sectionId}`} className="injectButton learningAnchorLink">
              Jump to {anchor.targetLabel}
            </a>
          </article>
        ))}
      </div>
    </div>
  );
}
