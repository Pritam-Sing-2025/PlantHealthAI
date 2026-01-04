import React from "react";

function PredictionResult({ data }) {
  // Map backend response to UI fields
  const label = data.class;
  const probability = (data.confidence * 100).toFixed(2);
  const status = data.health_status;
  const damage = data.damage_percent;
  const seriousness = data.seriousness;

  return (
    <div style={styles.card}>
      <h2>Prediction Result</h2>

      <p><strong>Disease:</strong> {label}</p>
      <p><strong>Confidence:</strong> {probability}%</p>
      <p><strong>Status:</strong> {status}</p>

      {status === "Diseased" && (
        <>
          <p><strong>Damage:</strong> {damage}%</p>
          <p><strong>Seriousness:</strong> {seriousness}</p>
        </>
      )}
    </div>
  );
}

const styles = {
  card: {
    marginTop: "20px",
    padding: "20px",
    width: "380px",
    margin: "auto",
    border: "1px solid #ccc",
    borderRadius: "10px",
    background: "#fff",
    textAlign: "left",
  },
};

export default PredictionResult;
