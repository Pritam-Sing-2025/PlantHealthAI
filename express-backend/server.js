import express from "express";
import cors from "cors";
import multer from "multer";
import { spawn } from "child_process";

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: "uploads/" });

app.get("/", (req, res) => {
    res.send("PlantHealthAI Express Backend is Running");
  });

app.post("/predict", upload.single("file"), (req, res) => {
  if (!req.file) return res.status(400).json({ error: "No image uploaded" });

  const python = spawn("python3", [
    "../Python/predict_api.py",   // NEW FILE
    req.file.path
  ]);  

  python.stdout.on("data", (data) => {
    console.log("PYTHON RAW OUTPUT:", data.toString()); // <-- IMPORTANT

    try {
      const result = JSON.parse(data.toString());
      res.json(result);
    } catch (err) {
      console.log("JSON PARSE ERROR:", err);
      res.status(500).json({ 
        error: "Invalid JSON from Python",
        raw: data.toString()
      });
    }
});


  python.stderr.on("data", (data) => {
    console.log("Python error:", data.toString());
  });
});

const PORT = 8080;
app.listen(PORT, "0.0.0.0", () => {
    console.log(`Express backend running at http://localhost:${PORT}`);
  });
  

