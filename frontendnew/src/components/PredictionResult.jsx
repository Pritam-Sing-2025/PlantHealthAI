import React from "react";

function PredictionResult({ data }) {
  return (
    <div className="result-card">
      <h2>Prediction Result</h2>

      <p><strong>Label:</strong> {data.label}</p>
      <p><strong>Probability:</strong> {data.probability}%</p>
      <p><strong>Status:</strong> {data.status}</p>

      {data.status === "Diseased" && (
        <>
          <p><strong>Damage:</strong> {data.damage}%</p>
          <p><strong>Seriousness:</strong> {data.seriousness}</p>
        </>
      )}
    </div>
  );
}

export default PredictionResult;
