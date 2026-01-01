from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .auth import router as auth_router
import os
import requests
import uvicorn

# 1. إنشاء جداول قاعدة البيانات تلقائياً
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️ تنبيه: تعذر تحديث جداول قاعدة البيانات: {e}")

# 2. تهيئة التطبيق
app = FastAPI(
    title="Neural Core Engine",
    description="نواة النظام التعليمي المتطور - BTEC NEXUS v2200",
    version="2.0.0"
)

# 3. إعدادات الـ CORS (السماح للواجهة بالاتصال)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. تسجيل الموجهات
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# 5. نقطة اتصال لوحة التحكم (Dashboard API) - المنفذ 10000
@app.get("/api/v1/status")
async def get_dashboard_status():
    return {
        "status": "ONLINE",
        "users": 1250,
        "activeProtocols": 8,
        "processing_power": "98.2 GHZ",
        "location": "Amman, Jordan",
        "timestamp": "2125.4.1"
    }

# 6. نقطة اتصال الذكاء الاصطناعي (Gemini)
API_KEY = "AIzaSyB4ptwXu2jdtg7NyyS43OZWBwNq2iA2K4s"

@app.post("/api/ask-gemini")
async def ask_gemini(data: dict):
    user_message = data.get("message")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": "فشل الاتصال بنواة Gemini", "details": str(e)}

# 7. نقطة فحص الصحة
@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# 8. تشغيل السيرفر على البورت 10000 (لحل مشكلة التصاريح)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=10000, reload=True)