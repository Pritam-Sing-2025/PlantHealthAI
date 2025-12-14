import React from "react";

export default function HowItWorks() {
  return (
    <div className="page">
      <h1 className="page-title">How It Works</h1>

      <ol className="steps">
        <li>Upload a clear image of the plant leaf.</li>
        <li>The AI model processes the image.</li>
        <li>You receive predicted disease & confidence level.</li>
        <li>The app suggests possible solutions.</li>
      </ol>
    </div>
  );
}
