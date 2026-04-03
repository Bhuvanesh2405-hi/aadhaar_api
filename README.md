---
title: Aadhaar Card Detection API
emoji: 🪪
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Aadhaar Card Detection API

## Install dependencies
pip install -r requirements.txt

## Run API
uvicorn main:app --reload

## API Docs
http://127.0.0.1:8000/docs

## Request format
{
  "image_bytes": [255,216,255,...]
}

## Response
{
  "prediction": "AADHAAR_CARD",
  "is_aadhaar_card": true,
  "confidence": 0.97
}
