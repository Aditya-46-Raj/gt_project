import React from "react";

function Report({ report }) {
  if (!report) {
    return null;
  }

  const { carbon_analysis, recommendations } = report;

  return (
    <div className="report-section">
      {/* Total Emissions Card */}
      <div className="report-card total-emissions">
        <h3>Total Emissions</h3>
        <p>
          {carbon_analysis.total_emissions.toFixed(2)} <span>kg CO₂e</span>
        </p>
      </div>

      {/* Materials Breakdown Card */}
      <div className="report-card">
        <h3>Materials Breakdown</h3>
        <ul>
          {carbon_analysis.materials.map((m, idx) => (
            <li key={idx}>
              <strong>{m.material}</strong>: {m.quantity} {m.unit} →
              <span> {m.emission.toFixed(2)} kg CO₂e</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Recommendations Card */}
      <div className="report-card">
        <h3>Recommendations</h3>
        {recommendations && recommendations.length > 0 ? (
          <ul>
            {recommendations.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>
        ) : (
          <p>No specific recommendations at this time.</p>
        )}
      </div>
    </div>
  );
}

export default Report;