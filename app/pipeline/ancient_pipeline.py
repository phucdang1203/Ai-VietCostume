from app.pipeline.face_service import FaceService
from app.pipeline.prompt_service import PromptService
from app.pipeline.generation_service import GenerationService
from app.pipeline.composition_service import CompositionService


class AncientPipeline:
    def __init__(self):
        self.face_service = FaceService()
        self.prompt_service = PromptService()
        self.generation_service = GenerationService()
        self.composition_service = CompositionService()

    def run(self, input_path: str, output_path: str):
        # Step 1: Face
        face_image = self.face_service.detect_and_crop_face(input_path)

        # Step 2: Prompt
        prompt = self.prompt_service.get_random_prompt()

        # Step 3: Generate
        generated_image = self.generation_service.generate_character(prompt)

        # Step 4: Compose
        final_image = self.composition_service.compose_face_on_body(
            face_image,
            generated_image
        )

        # Step 5: Save
        final_image.save(output_path)

        return {
            "prompt": prompt,
            "output": output_path
        }