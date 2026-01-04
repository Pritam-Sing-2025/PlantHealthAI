import React, { useState } from "react";
import axios from "axios";
import ImageUpload from "../components/ImageUpload";
import PredictionResult from "../components/PredictionResult";
import Loader from "../components/Loader";

function Home() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = (file) => {
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handlePredict = async () => {
    if (!image) {
      alert("Upload an image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      // ✅ THIS IS THE IMPORTANT LINE
      setResult(res.data);
    } catch (err) {
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "40px" }}>
      <h1>🌱 Plant Health AI</h1>

      <ImageUpload onUpload={handleUpload} preview={preview} />

      <button onClick={handlePredict} style={{ marginTop: "20px" }}>
        Predict
      </button>

      {loading && <Loader />}

      {/* ✅ ONLY render when data exists */}
      {result && <PredictionResult data={result} />}
    </div>
  );
}

export default Home;
