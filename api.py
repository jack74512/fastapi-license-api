from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
from datetime import datetime, timedelta

# 🔹 تهيئة Firestore
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"
db = firestore.Client()

app = FastAPI()

# 🔹 API للتحقق من مفتاح التفعيل
@app.post("/verify-license/")
async def verify_license(license_key: str, uuid: str):
    try:
        doc_ref = db.collection("activation_keys").document(license_key)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="License key not found")

        license_data = doc.to_dict()
        stored_uuid = license_data.get("uuid")
        activated_at = license_data.get("activated_at")

        # 🔹 التحقق مما إذا كان المفتاح مستخدمًا بالفعل على جهاز آخر
        if stored_uuid and stored_uuid != uuid:
            raise HTTPException(status_code=403, detail="License key already in use on another device")

        # 🔹 حساب تاريخ انتهاء الصلاحية
        if activated_at:
            expiration_date = activated_at + timedelta(days=30)
            if datetime.utcnow() > expiration_date:
                raise HTTPException(status_code=403, detail="License key has expired")

        # 🔹 تحديث UUID إذا كان المفتاح جديدًا
        if not stored_uuid:
            doc_ref.update({"uuid": uuid, "activated_at": datetime.utcnow()})
        
        return {"success": True, "message": "License is valid"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
