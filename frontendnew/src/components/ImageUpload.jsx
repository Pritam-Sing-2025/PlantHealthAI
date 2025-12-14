import React from "react";

function ImageUpload({ onUpload, preview }) {
  return (
    <div className="upload-box">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => onUpload(e.target.files[0])}
      />

      {preview && (
        <img src={preview} alt="Preview" className="preview-img" />
      )}
    </div>
  );
}

export default ImageUpload;
