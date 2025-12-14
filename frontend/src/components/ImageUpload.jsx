import React from "react";

export default function ImageUpload({ setImage, setPreview }) {
  const handleFile = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  return (
    <div className="upload-box">
      <h2>
        Is your green buddy dying?
        Try Almighty to identify the cause and get extensive disease and care info in a snap.
      </h2>
      <label className="upload-label">Upload Leaf Image</label>
      <input type="file" accept="image/*" onChange={handleFile} />
    </div>
  );
}
