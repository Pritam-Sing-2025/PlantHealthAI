from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.predictor import predict_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Plant Health Checker Backend Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_bytes = await file.read()
    result = predict_image(file_bytes)
    return result
