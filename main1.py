from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastai.learner import load_learner
from fastai.vision.core import PILImage
import pathlib
import io
import base64

# Fix PosixPath error (model trained on Linux)
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

app = FastAPI(title="Aadhaar Card Detection API")

# Load model once
learn = load_learner("aadhaar_classifier.pkl")


# -----------------------------
# Request models
# -----------------------------
class ImageBytes(BaseModel):
    image_bytes: list


class ImageBase64(BaseModel):
    image_base64: str


# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "Aadhaar Card Detection API is running"}


# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "OK"}


# -----------------------------
# Predict using uploaded file
# -----------------------------
@app.post("/predict/file")
async def predict_file(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img = PILImage.create(io.BytesIO(image_bytes))

        pred_class, pred_idx, probs = learn.predict(img)

        return {
            "status": "success",
            "prediction": str(pred_class),
            "is_aadhaar_card": str(pred_class).lower() == "aadhaar",
            "confidence": float(probs[pred_idx])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# -----------------------------
# Predict using byte array
# -----------------------------
@app.post("/predict/bytes")
async def predict_bytes(data: ImageBytes):
    try:
        image_bytes = bytes(data.image_bytes)
        img = PILImage.create(io.BytesIO(image_bytes))

        pred_class, pred_idx, probs = learn.predict(img)

        return {
            "status": "success",
            "prediction": str(pred_class),
            "is_aadhaar_card": str(pred_class).lower() == "aadhaar",
            "confidence": float(probs[pred_idx])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# -----------------------------
# Predict using Base64 string
# -----------------------------
@app.post("/predict/base64")
async def predict_base64(data: ImageBase64):
    try:
        image_bytes = base64.b64decode(data.image_base64)
        img = PILImage.create(io.BytesIO(image_bytes))

        pred_class, pred_idx, probs = learn.predict(img)

        return {
            "status": "success",
            "prediction": str(pred_class),
            "is_aadhaar_card": str(pred_class).lower() == "aadhaar",
            "confidence": float(probs[pred_idx])
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }