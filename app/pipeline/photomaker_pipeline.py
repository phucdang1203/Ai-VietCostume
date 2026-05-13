# app/pipeline/photomaker_pipeline.py

class PhotoMakerPipeline:
    def __init__(self):
        from app.pipeline.face_service import FaceService
        from app.pipeline.prompt_service import PromptService
        from app.pipeline.photomaker_generation_service import PhotoMakerGenerationService
        
        self.face_service = FaceService()
        self.prompt_service = PromptService()
        self.generation_service = PhotoMakerGenerationService()

    def run(self, input_path, output_path):
        # 1. Trích xuất khuôn mặt và thông tin
        face_data = self.face_service.process_face(input_path)

        # 2. Tạo prompt dựa trên giới tính/tuổi
        prompt_data = self.prompt_service.generate_prompt(
            gender=face_data["gender"],
            age=face_data["age"]
        )

        # 3. CHỈNH SỬA QUAN TRỌNG: 
        # PhotoMaker V2 cần từ khóa 'img' trong prompt để biết chèn mặt vào đâu.
        # Giả sử prompt từ PromptService là: "A Vietnamese man wearing..."
        # Ta cần đổi thành: "A Vietnamese man img wearing..."
        
        original_prompt = prompt_data["prompt"]
        # Cách đơn giản: chèn 'img' sau man/woman
        target_words = ["man", "woman", "person", "boy", "girl"]
        modified_prompt = original_prompt
        for word in target_words:
            if word in original_prompt.lower():
                modified_prompt = original_prompt.lower().replace(word, f"{word} img")
                break
        
        if "img" not in modified_prompt:
            modified_prompt += " img" # Backup nếu không tìm thấy từ khóa
            
        prompt_data["prompt"] = modified_prompt

        # 4. Gọi service tạo ảnh với PIL Image đã cắt từ FaceService
        return self.generation_service.generate(
            prompt_data=prompt_data,
            input_image=face_data["face_pil"], # Truyền trực tiếp PIL Image
            output_path=output_path
        )