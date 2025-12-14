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
      alert("Please select an image!");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post("http://localhost:8080/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Response:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("Backend Error:", err);
      alert("Error connecting to backend.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">🌱 PlantHealthAI</h1>

      <ImageUpload onUpload={handleUpload} preview={preview} />

      <button className="predict-btn" onClick={handlePredict}>
        Predict Disease
      </button>

      {loading && <Loader />}
      {result && <PredictionResult data={result} />}
    </div>
  );
}

export default Home;
