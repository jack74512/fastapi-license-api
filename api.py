import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
from fastapi import FastAPI

app = FastAPI()

# 🔹 قراءة `service-account.json` من متغير بيئي في `Railway`
service_account_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# 🔹 إنشاء `Firestore Client`
db = firestore.Client(credentials=credentials)

@app.get("/")
def home():
    return {"message": "FastAPI is running on Railway!"}

@app.post("/verify-license/")
def verify_license(license_key: str, uuid: str):
    # 🔹 البحث عن المفتاح في Firestore
    doc_ref = db.collection("activation_keys").document(license_key)
    doc = doc_ref.get()

    if not doc.exists:
        return {"detail": "❌ License key not found"}

    license_data = doc.to_dict()

    # 🔹 التحقق من الـ UUID
    if license_data.get("uuid") and license_data["uuid"] != uuid:
        return {"detail": "❌ This key is already used on another device"}

    # 🔹 تحديث UUID عند أول استخدام
    if not license_data.get("uuid"):
        doc_ref.update({"uuid": uuid})

    return {"message": "✅ License key is valid!"}
