import requests
import base64

BASE_URL = "https://your-live-api-url"

IMAGE_PATH = "sample_aadhaar.jpg"


# FILE TEST
files = {"file": open(IMAGE_PATH, "rb")}
response = requests.post(f"{BASE_URL}/predict/file", files=files)
print("FILE RESULT:", response.json())


# BYTE ARRAY TEST
with open(IMAGE_PATH, "rb") as f:
    byte_list = list(f.read())

payload = {"image_bytes": byte_list}
response = requests.post(f"{BASE_URL}/predict/bytes", json=payload)
print("BYTE RESULT:", response.json())


# BASE64 TEST
with open(IMAGE_PATH, "rb") as f:
    base64_string = base64.b64encode(f.read()).decode()

payload = {"image_base64": base64_string}
response = requests.post(f"{BASE_URL}/predict/base64", json=payload)
print("BASE64 RESULT:", response.json())
