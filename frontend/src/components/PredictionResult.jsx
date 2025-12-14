import React from "react";

export default function PredictionResult({ data }) {
  return (
    <div className="result-box">
      <h2>Prediction Result</h2>
      <p><strong>Disease:</strong> {data.disease}</p>
      <p><strong>Confidence:</strong> {data.confidence}</p>
      <p><strong>Solution:</strong> {data.solution}</p>
    </div>
  );
}
