# =========================================================
# FILE:
# app/routers/generate.py
# =========================================================
import json  # Thêm thư viện json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.pipeline.prompt_service import PromptService
from app.pipeline.generation_service import GenerationService
from app.pipeline.face_service import FaceService
from app.pipeline.face_swap_service import FaceSwapService
from app.pipeline.photomaker_pipeline import (
    PhotoMakerPipeline
)

router = APIRouter(prefix="/generate", tags=["Generate"])

# Khởi tạo các service
prompt_service = PromptService()
gen_service = GenerationService()
face_service = FaceService()
face_swap_service = FaceSwapService()

pipeline = PhotoMakerPipeline()

FINAL_DIR = Path("outputs/final_results")
FINAL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("outputs/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/low/{file_id}")
async def generate_character(file_id: str):
    # 1. Tìm ảnh gốc
    original_files = list(Path("uploads/faces").glob(f"{file_id}.*"))
    if not original_files:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh gốc.")
    
    input_path = str(original_files[0])
    face_crop_path = Path(f"outputs/face_crops/{file_id}_face_crop.png")

    try:
        # Bước 1 & 2: Phân tích mặt và tạo Prompt
        face_info = face_service.process_face(input_path)
        prompt_data = prompt_service.generate_prompt(gender=face_info["gender"], age=face_info["age"])

        # Bước 3: Tạo ảnh trang phục (ảnh tạm)
        temp_gen_path = OUTPUT_DIR / f"{file_id}_temp.png"
        gen_result = gen_service.generate_costume(prompt_data, str(temp_gen_path))

        # Bước 4: Ghép mặt người dùng vào ảnh AI
        final_output_path = FINAL_DIR / f"{file_id}_final.png"
        
        swap_result = face_swap_service.swap_face(
            source_face_path=input_path,
            target_image_path=str(temp_gen_path),
            output_path=str(final_output_path)
        )

        # Bước 5: Chuẩn bị dữ liệu Response
        response_data = {
            "status": "success",
            "file_id": file_id,
            "analysis": {
                "detected_gender": face_info["gender"],
                "detected_age": face_info["age"],
                "age_group": prompt_data["age_group"]
            },
            "system_selection": {
                "rank_occupation": prompt_data["occupation"],
                "prompt_used": prompt_data["prompt"],
                "negative_prompt_used": prompt_data.get("negative_prompt")
            },
            "output": {
                "generated_file": str(final_output_path),
                "face_crop_used": str(face_crop_path) if face_crop_path.exists() else None
            },
            "next_steps": ["Face Swapping (Completed)", "Upscaling"]
        }

        # --- BƯỚC MỚI: LƯU JSON METADATA ---
        json_path = FINAL_DIR / f"{file_id}_final.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
        # -----------------------------------

        return response_data

    except Exception as e:
        # In lỗi chi tiết ra console để dễ debug
        print(f"Generation Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/medium/{file_id}")
async def generate_character(file_id: str):

    original_files = list(
        Path("uploads/faces").glob(f"{file_id}.*")
    )

    if not original_files:
        raise HTTPException(
            status_code=404,
            detail="Face file not found"
        )

    input_path = str(original_files[0])

    output_path = (
        f"outputs/generated/medium/{file_id}_final.png"
    )

    result = pipeline.run(
        input_path=input_path,
        output_path=output_path
    )

    return {
        "status": "success",
        "file_id": file_id,
        "result": result
    }