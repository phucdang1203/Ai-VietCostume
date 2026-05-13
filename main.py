from fastapi import FastAPI
from app.routers.generate import router as generate_router
# 1. Import router từ file face.py
from app.routers.face import router as face_router 
from app.routers.instantid_generate import router as instantid_generate 

from dotenv import load_dotenv
import os

app = FastAPI(title="Ancient Vietnam AI Server")

app.include_router(generate_router)
app.include_router(face_router)
app.include_router(instantid_generate)

@app.get("/health")
def health():
    return {"status": "ok"}

load_dotenv() # Dòng này sẽ đọc file .env và nạp vào hệ thống