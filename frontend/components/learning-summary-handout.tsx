"use client";

type LearningSummarySection = {
  id: string;
  heading: string;
  points: string[];
};

type LearningSummaryHandoutProps = {
  title: string;
  audience: string;
  generatedFor: string;
  sections: LearningSummarySection[];
  takeaways: string[];
  exportPayload: Record<string, unknown>;
  exportFilename: string;
};

export function LearningSummaryHandout({
  title,
  audience,
  generatedFor,
  sections,
  takeaways,
  exportPayload,
  exportFilename,
}: LearningSummaryHandoutProps) {
  const downloadHandout = () => {
    const serialized = JSON.stringify(exportPayload, null, 2);
    const blob = new Blob([serialized], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = exportFilename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="learningHandoutPanel">
      <header className="learningHandoutHeader">
        <div>
          <h3>{title}</h3>
          <p>
            Audience: {audience} | Purpose: {generatedFor}
          </p>
        </div>
        <button type="button" className="injectButton" onClick={downloadHandout}>
          Download JSON Handout
        </button>
      </header>

      <div className="learningHandoutGrid">
        {sections.map((section) => (
          <article key={section.id} className="learningInfoCard">
            <h4>{section.heading}</h4>
            <ul>
              {section.points.map((point) => (
                <li key={`${section.id}-${point}`}>{point}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <article className="learningInfoCard learningInfoCardWide">
        <h4>Stakeholder Takeaways</h4>
        <ul>
          {takeaways.map((takeaway) => (
            <li key={takeaway}>{takeaway}</li>
          ))}
        </ul>
      </article>
    </div>
  );
}
