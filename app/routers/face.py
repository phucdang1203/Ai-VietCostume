# app/routers/face.py

"""
Face Upload Router
------------------
Chức năng:
1. User upload ảnh khuôn mặt
2. Lưu file vào uploads/
3. Gọi FaceService xử lý:
    - Load image
    - Face Detection
    - Face Crop
    - Face Embedding
4. Trả về metadata để debug/test pipeline

Endpoint:
POST /face/upload
"""

from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.pipeline.face_service import FaceService


router = APIRouter(
    prefix="/face",
    tags=["Face"]
)

# =========================
# CONFIG
# =========================
UPLOAD_DIR = Path("uploads/faces")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

FACE_CROP_DIR = Path("outputs/face_crops")
FACE_CROP_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# INIT SERVICE
# =========================
face_service = FaceService(
    # face_model_name="buffalo_l",
    # providers=["CPUExecutionProvider"]  # đổi sang CUDAExecutionProvider nếu có GPU
)


# =========================
# VALIDATION
# =========================
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def validate_image_extension(filename: str):
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Chỉ hỗ trợ file ảnh: jpg, jpeg, png, webp"
        )


# =========================
# API
# =========================
@router.post("/upload")
async def upload_face(
    file: UploadFile = File(...)
):
    """
    Upload face image + detect + embedding
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Tên file không hợp lệ."
        )

    validate_image_extension(file.filename)

    # Unique filename
    file_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix.lower()

    input_path = UPLOAD_DIR / f"{file_id}{ext}"

    # Save upload
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi lưu file: {str(e)}"
        )

    # Process face
    try:
        result = face_service.process_face(
            str(input_path)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi xử lý face: {str(e)}"
        )

    # Save cropped face for debug
    crop_output_path = FACE_CROP_DIR / f"{file_id}_face_crop.png"

    face_service.save_face_crop(
        result["face_crop"],
        str(crop_output_path)
    )

    # Convert numpy embedding shape
    embedding_dim = (
        len(result["embedding"])
        if result["embedding"] is not None
        else 0
    )

    return {
        "message": "Face uploaded and processed successfully",
        "file_id": file_id,
        "original_file": str(input_path),
        "face_crop_file": str(crop_output_path),

        # Face metadata
        "bbox": result["bbox"],
        "landmarks": (
            result["landmarks"].tolist()
            if result["landmarks"] is not None
            else None
        ),
        "embedding_dimension": embedding_dim,

        # Pipeline readiness
        "next_steps": [
            "Random Ancient Occupation Prompt",
            "Stable Diffusion Generation",
            "Face Preservation / Swap",
            "Composition / Blending",
            "Upscale"
        ]
    }