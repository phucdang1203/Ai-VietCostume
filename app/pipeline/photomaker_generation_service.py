# app/pipeline/photomaker_generation_service.py

import torch
import os
from pathlib import Path
from diffusers.utils import load_image
from huggingface_hub import hf_hub_download

# Import pipeline chuyên dụng cho PhotoMaker
from photomaker import PhotoMakerStableDiffusionXLPipeline

class PhotoMakerGenerationService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        # 1. Đường dẫn Model
        # Kaggle: /kaggle/input/stable-diffusion-xl-base-1.0
        self.base_model = os.getenv("MODEL_PATH", "stabilityai/stable-diffusion-xl-base-1.0")
        
        # Đường dẫn tới file photomaker-v2.bin (Adapter)
        # Bạn có thể để trong Kaggle Dataset hoặc tải tự động từ HF
        self.photomaker_path = hf_hub_download(
            repo_id="TencentARC/PhotoMaker-V2", 
            filename="photomaker-v2.bin", 
            repo_type="model"
        )

        # 2. Khởi tạo Pipeline
        print(f"--- Loading PhotoMaker V2 with Base: {self.base_model} ---")
        self.pipe = PhotoMakerStableDiffusionXLPipeline.from_pretrained(
            self.base_model,
            torch_dtype=self.dtype,
            use_safetensors=True,
            variant="fp16"
        ).to(self.device)

        # 3. Load PhotoMaker Adapter
        self.pipe.load_photomaker_adapter(
            os.path.dirname(self.photomaker_path),
            subfolder="",
            weight_name=os.path.basename(self.photomaker_path),
            trigger_word="img"  # Rất quan trọng: từ khóa kích hoạt PhotoMaker
        )

        # 4. Tối ưu hóa cho T4 GPU (16GB VRAM)
        if self.device == "cuda":
            self.pipe.enable_model_cpu_offload() # Di chuyển các phần không dùng về RAM
            self.pipe.enable_vae_tiling()        # Xử lý ảnh kích thước lớn không tràn VRAM

    def generate(self, prompt_data: dict, input_image, output_path: str):
        """
        input_image: PIL Image từ FaceService
        """
        # PhotoMaker yêu cầu danh sách các ảnh khuôn mặt (ở đây ta dùng 1 ảnh)
        input_id_images = [input_image]
        
        # Lấy prompt và đảm bảo có từ khóa 'img' phía sau chủ thể
        # Ví dụ: "A photo of a man img, wearing Vietnamese costume..."
        raw_prompt = prompt_data.get("prompt", "")
        negative_prompt = prompt_data.get("negative_prompt", "asymmetry, worst quality, low quality, cartoon, anime")

        # Thiết lập Generator để kết quả ổn định
        generator = torch.Generator(device=self.device).manual_seed(42)

        print(f"--- Generating with prompt: {raw_prompt} ---")
        
        with torch.inference_mode():
            # Gọi pipeline với các tham số đặc thù của PhotoMaker
            result = self.pipe(
                prompt=raw_prompt,
                input_id_images=input_id_images,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=5.0, # PhotoMaker thường đẹp ở tầm 3.0 - 5.0
                generator=generator,
                start_merge_step=10 # Bước bắt đầu trộn ID
            )

        image = result.images[0]
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_file)

        return {
            "output_file": str(output_file),
            "mode": "PHOTOMAKER_V2_ACTIVE",
            "prompt_used": raw_prompt
        }