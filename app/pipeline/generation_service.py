# =========================================================
# FILE:
# app/pipeline/generation_service.py
# =========================================================

import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
from PIL import Image

class GenerationService:
    def __init__(self):
        self.device = "cpu" # Hoặc "cuda" nếu có GPU
        # model_id = "runwayml/stable-diffusion-v1-5" # Hoặc model từ ModelRegistry
        model_id = "nota-ai/bk-sdm-tiny" # Hoặc model từ ModelRegistry
        
        # Load pipeline cơ bản
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float32,
            safety_checker=None
        ).to(self.device)
        
        # Thay vì import class lỗi, ta dùng method load_ip_adapter (nếu diffusers đã update)
        # Nếu chưa cần dùng IP-Adapter ngay, bạn có thể comment phần này để chạy test trước
        # self.pipe.load_ip_adapter("huggingface/ip-adapter-faceid", subfolder="models", weight_name="ip-adapter-faceid_sd15.bin")

    def generate_costume(self, prompt_data: dict, output_path: str, face_image_path: str = None):
        # Tạo ảnh từ Prompt (Text-to-Image)
        image = self.pipe(
            prompt=prompt_data["prompt"],
            negative_prompt=prompt_data["negative_prompt"],
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]
        
        image.save(output_path)
        return {"output_file": output_path, "occupation": prompt_data["occupation"]}
 