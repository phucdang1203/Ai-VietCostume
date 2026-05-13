# app/pipeline/photomaker_pipeline.py

from app.pipeline.face_service import FaceService
from app.pipeline.prompt_service import PromptService
from app.pipeline.photomaker_generation_service import (
    PhotoMakerGenerationService
)


class PhotoMakerPipeline:
    def __init__(self):
        self.face_service = FaceService()
        self.prompt_service = PromptService()
        self.generation_service = (
            PhotoMakerGenerationService()
        )

    def run(self, input_path, output_path):

        face_data = self.face_service.process_face(
            input_path
        )

        prompt_data = (
            self.prompt_service.generate_prompt(
                gender=face_data["gender"],
                age=face_data["age"]
            )
        )

        return self.generation_service.generate(
            prompt_data=prompt_data,
            input_image=face_data["face_pil"],
            output_path=output_path
        )