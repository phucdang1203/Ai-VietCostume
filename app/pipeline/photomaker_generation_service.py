# =========================================================
# FILE:
# app/pipeline/photomaker_generation_service.py
#
# MỤC TIÊU:
# - Không load sai TencentARC/PhotoMaker-V2 như DiffusionPipeline trực tiếp
# - Dùng SDXL Base model chạy trước
# - Sẵn sàng nâng cấp sang PhotoMaker adapter sau
# - Chạy được local + Kaggle
# =========================================================

import torch
from pathlib import Path

# =========================================================
# TẠM THỜI:
# Dùng StableDiffusionXLPipeline base
# =========================================================
from diffusers import StableDiffusionXLPipeline

from app.core.model_registry import (
    ModelRegistry
)


class PhotoMakerGenerationService:
    def __init__(self):

        # =================================================
        # DEVICE
        # =================================================
        self.device = (
            ModelRegistry.get_device()
        )

        # =================================================
        # DTYPE
        # =================================================
        self.dtype = (
            torch.float16
            if self.device == "cuda"
            else torch.float32
        )

        # =================================================
        # BASE MODEL
        # KHÔNG dùng:
        # TencentARC/PhotoMaker-V2 trực tiếp
        # =================================================
        self.base_model = (
            ModelRegistry.get_base_model()
        )

        # =================================================
        # LOAD BASE SDXL PIPELINE
        # =================================================
        self.pipe = (
            StableDiffusionXLPipeline
            .from_pretrained(
                self.base_model,
                torch_dtype=self.dtype,
                use_safetensors=True
            )
        )

        # =================================================
        # MOVE DEVICE
        # =================================================
        self.pipe = self.pipe.to(
            self.device
        )

        # =================================================
        # MEMORY SAFE
        # =================================================
        try:
            self.pipe.enable_attention_slicing()
        except:
            pass

        # =================================================
        # OPTIONAL FUTURE:
        # Nếu sau này clone official PhotoMaker:
        #
        # self.pipe.load_photomaker_adapter(...)
        # =================================================

    def generate(
        self,
        prompt_data: dict,
        input_image,
        output_path: str
    ):

        # =================================================
        # NOTE:
        # Hiện tại input_image chưa được dùng trực tiếp
        # vì bản này là SDXL skeleton trước
        #
        # Giai đoạn sau:
        # input_image => PhotoMaker adapter
        # =================================================

        result = self.pipe(
            prompt=prompt_data[
                "prompt"
            ],

            negative_prompt=prompt_data.get(
                "negative_prompt",
                None
            ),

            num_inference_steps=30,

            guidance_scale=7.5
        )

        image = result.images[0]

        # =================================================
        # SAVE
        # =================================================
        output_file = Path(
            output_path
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        image.save(output_file)

        # =================================================
        # RESPONSE
        # =================================================
        return {
            "output_file": str(
                output_file
            ),

            "prompt": prompt_data[
                "prompt"
            ],

            "negative_prompt": prompt_data.get(
                "negative_prompt"
            ),

            "occupation": prompt_data[
                "occupation"
            ],

            "age_group": prompt_data.get(
                "age_group"
            ),

            "gender": prompt_data.get(
                "gender"
            ),

            # =================================================
            # Trạng thái rõ ràng:
            # Chưa phải full PhotoMaker identity injection
            # =================================================
            "mode": (
                "SDXL_BASE_ONLY"
            ),

            "next_upgrade": [
                "Install official PhotoMaker repo",
                "Load PhotoMaker adapter",
                "Inject face identity image"
            ]
        }