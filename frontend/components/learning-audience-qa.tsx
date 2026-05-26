"use client";

import { useMemo, useState } from "react";

type LearningQaEntry = {
  id: string;
  category: string;
  question: string;
  answer: string;
  mappedComponents: string[];
};

type LearningAudienceQaProps = {
  questions: LearningQaEntry[];
  presenterHint: string;
};

const CATEGORY_ORDER = ["architecture", "performance", "reliability", "portability", "operations"];

export function LearningAudienceQa({ questions, presenterHint }: LearningAudienceQaProps) {
  const categories = useMemo(() => {
    const unique = Array.from(new Set(questions.map((q) => q.category)));
    return unique.sort((a, b) => {
      const indexA = CATEGORY_ORDER.indexOf(a);
      const indexB = CATEGORY_ORDER.indexOf(b);
      if (indexA === -1 && indexB === -1) return a.localeCompare(b);
      if (indexA === -1) return 1;
      if (indexB === -1) return -1;
      return indexA - indexB;
    });
  }, [questions]);

  const [activeCategory, setActiveCategory] = useState<string>(categories[0] ?? "");
  const [selectedQuestionId, setSelectedQuestionId] = useState<string>(questions[0]?.id ?? "");

  const filteredQuestions = useMemo(() => {
    return questions.filter((q) => (activeCategory ? q.category === activeCategory : true));
  }, [questions, activeCategory]);

  const selectedQuestion = useMemo(() => {
    return (
      filteredQuestions.find((q) => q.id === selectedQuestionId) ??
      filteredQuestions[0] ??
      questions[0]
    );
  }, [filteredQuestions, questions, selectedQuestionId]);

  return (
    <div className="learningQaPanel">
      <header className="learningQaHeader">
        <div>
          <h3>Audience Q and A Mode</h3>
          <p>{presenterHint}</p>
        </div>
      </header>

      <div className="learningQaCategories" role="tablist" aria-label="Question categories">
        {categories.map((category) => {
          const isActive = category === activeCategory;
          return (
            <button
              key={category}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={`learningQaCategoryButton ${isActive ? "isActive" : ""}`}
              onClick={() => {
                setActiveCategory(category);
                const firstInCategory = questions.find((q) => q.category === category);
                if (firstInCategory) {
                  setSelectedQuestionId(firstInCategory.id);
                }
              }}
            >
              {category}
            </button>
          );
        })}
      </div>

      <div className="learningQaContent">
        <aside className="learningQaQuestionList">
          {filteredQuestions.map((entry) => (
            <button
              key={entry.id}
              type="button"
              className={`learningQaQuestionButton ${entry.id === selectedQuestion?.id ? "isActive" : ""}`}
              onClick={() => setSelectedQuestionId(entry.id)}
            >
              {entry.question}
            </button>
          ))}
        </aside>

        <article className="learningQaAnswerCard" aria-live="polite">
          {selectedQuestion ? (
            <>
              <p className="learningQaPrompt">{selectedQuestion.question}</p>
              <p>{selectedQuestion.answer}</p>
              <div className="learningQaMappings">
                {selectedQuestion.mappedComponents.map((component) => (
                  <span key={component}>{component}</span>
                ))}
              </div>
            </>
          ) : (
            <p>No question selected.</p>
          )}
        </article>
      </div>
    </div>
  );
}
