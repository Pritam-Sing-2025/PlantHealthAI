// import React, { useState } from "react";
// import ImageUpload from "../components/ImageUpload";
// import Loader from "../components/Loader";
// import PredictionResult from "../components/PredictionResult";
// import logo from '../plantLogo.png';

// export default function Home() {
//   const [image, setImage] = useState(null);
//   const [preview, setPreview] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [predictions, setPredictions] = useState(null);

//   const handlePredict = () => {
//     if (!image) return alert("Bro upload an image first!");

//     setLoading(true);

//     setTimeout(() => {
//       setPredictions({
//         disease: "Sample Prediction",
//         confidence: "92%",
//         solution: "Provide proper treatment."
//       });
//       setLoading(false);
//     }, 1500);
//   };

//   return (
//     <>
//     <h3 className="message">Let's take care of <s>ur</s> our plants.</h3> 
//     <div className="page home-container">
//       {/* <h1 className="page-title">Plant Disease Detection</h1> */}
//       {/* <br/>  */}
//       <img src={logo} className="logoImg" alt="logoImg" />

//       <div className="card">
//         <ImageUpload setImage={setImage} setPreview={setPreview} preview={preview} />

//         {preview && (
//           <img src={preview} alt="preview" className="preview-center" />
//         )}

//         <button className="primary-btn predict-btn" onClick={handlePredict}>
//           Predict Disease
//         </button>

//         {loading && <Loader />}
//         {predictions && <PredictionResult data={predictions} />}
//       </div>
//       <div className="demo"></div>
//     </div>
//     </>
//   );
// }




const formData = new FormData();
formData.append("file", image);

const res = await axios.post("http://localhost:6000/predict", formData, {
  headers: { "Content-Type": "multipart/form-data" }
});

setResult(res.data);
