# app/pipeline/face_service.py
from deepface import DeepFace
from PIL import Image
import numpy as np
from pathlib import Path

class FaceService:
    def __init__(self):
        self.detector_backend = 'retinaface' # Giữ nguyên bộ quét xịn nhất

    def process_face(self, input_path: str):
        try:
            # 1. Phân tích đa chỉ số: Giới tính và Tuổi
            # Việc gộp chung vào 1 lần gọi analyze giúp tiết kiệm thời gian xử lý CPU
            results = DeepFace.analyze(
                img_path = input_path, 
                actions = ['gender', 'age'], # Thêm 'age' vào đây
                enforce_detection = True,
                detector_backend = self.detector_backend
            )
            
            face_data = results[0]
            
            # 2. Xử lý Giới tính
            raw_gender = face_data['dominant_gender']
            gender = "woman" if raw_gender == 'Woman' else "man"

            # 3. Xử lý Độ tuổi
            age = int(face_data['age']) # DeepFace trả về số thực, ta ép kiểu về số nguyên

            # 4. Tính toán Tọa độ BBox (Bounding Box)
            region = face_data['region']
            bbox = [
                int(region['x']), 
                int(region['y']), 
                int(region['x'] + region['w']), 
                int(region['y'] + region['h'])
            ]

            # 5. Xử lý Hình ảnh (Giữ nguyên logic cắt mặt của bạn)
            original_image = Image.open(input_path).convert("RGB")
            face_crop = self._crop_face(original_image, bbox)

            # Trả về đầy đủ tất cả thông tin, không làm mất dữ liệu cũ
            return {
                "original_image": original_image,
                "face_crop": face_crop,
                "gender": gender,
                "age": age,          # Thông tin mới bổ sung
                "bbox": bbox,
                "embedding": None,   # Có thể bổ sung DeepFace.represent nếu cần sau này
                "landmarks": None
            }
            
        except Exception as e:
            raise ValueError(f"Không thể xử lý khuôn mặt: {str(e)}")

    def _crop_face(self, image: Image.Image, bbox, padding_ratio: float = 0.2):
        # Logic cắt mặt có lề để ảnh trông tự nhiên hơn
        width, height = image.size
        x1, y1, x2, y2 = bbox
        fw, fh = x2 - x1, y2 - y1
        px, py = int(fw * padding_ratio), int(fh * padding_ratio)
        return image.crop((
            max(0, x1 - px),
            max(0, y1 - py),
            min(width, x2 + px),
            min(height, y2 + py)
        ))

    # Bổ sung hàm này vì Router của bạn đang gọi nó
    def save_face_crop(self, face_crop: Image.Image, output_path: str):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        face_crop.save(output_path)

# from pathlib import Path
# from typing import Dict, Any, Optional
# import numpy as np
# from PIL import Image
# import mediapipe as mp
# # Thêm dòng này để kiểm tra xem solutions có tồn tại không
# # try:
# #     from mediapipe.python.solutions import face_detection as mp_face_detection
# #     from mediapipe.python.solutions import face_mesh as mp_face_mesh
# # except ImportError:
# #     import mediapipe.solutions.face_detection as mp_face_detection
# #     import mediapipe.solutions.face_mesh as mp_face_mesh

# class FaceService:
#     """
#     FaceService dùng MediaPipe - Không cần C++ Build Tools
#     Ưu điểm: Cài đặt cực nhanh, chạy ổn định trên CPU.
#     Nhược điểm: Embedding không tương thích hoàn toàn với IP-Adapter (InsightFace).
#     """

#     def __init__(self):
#         # self.face_model_name = face_model_name
#         # Khởi tạo giải pháp nhận diện khuôn mặt của MediaPipe
#         self.mp_face_detection = mp.solutions.face_detection
#         self.mp_face_mesh = mp.solutions.face_mesh
        
#         self.face_detector = self.mp_face_detection.FaceDetection(
#             model_selection=1, # 0 cho mặt gần (<2m), 1 cho mặt xa (<5m)
#             min_detection_confidence=0.5
#         )

#     # =========================
#     # PUBLIC MAIN ENTRY
#     # =========================
#     def process_face(self, input_path: str) -> Dict[str, Any]:
#         original_image = self._load_image(input_path)
        
#         # Chuyển sang RGB cho MediaPipe
#         image_np = np.array(original_image)
        
#         results = self.face_detector.process(image_np)

#         if not results.detections:
#             raise ValueError("Không tìm thấy khuôn mặt trong ảnh.")

#         # Chọn khuôn mặt có độ tin cậy cao nhất hoặc lớn nhất
#         primary_detection = max(results.detections, key=lambda x: x.score[0])
        
#         # Tính toán BBox
#         h, w, _ = image_np.shape
#         bbox_data = primary_detection.location_data.relative_bounding_box
#         x1 = int(bbox_data.xmin * w)
#         y1 = int(bbox_data.ymin * h)
#         x2 = int((bbox_data.xmin + bbox_data.width) * w)
#         y2 = int((bbox_data.ymin + bbox_data.height) * h)
#         bbox = [x1, y1, x2, y2]

#         face_crop = self._crop_face(original_image, bbox)

#         # Lưu ý: MediaPipe không có sẵn Face Embedding 512-d như InsightFace
#         # Chúng ta sẽ trả về mảng rỗng hoặc dùng logic khác sau này
#         return {
#             "original_image": original_image,
#             "face_crop": face_crop,
#             "bbox": bbox,
#             "embedding": np.zeros((512,)), # Dummy embedding
#             "landmarks": None, # Có thể lấy từ Face Mesh nếu cần
#         }

#     def _load_image(self, input_path: str) -> Image.Image:
#         path = Path(input_path)
#         if not path.exists():
#             raise FileNotFoundError(f"Không tìm thấy file: {input_path}")
#         return Image.open(path).convert("RGB")

#     def _crop_face(self, image: Image.Image, bbox, padding_ratio: float = 0.25) -> Image.Image:
#         width, height = image.size
#         x1, y1, x2, y2 = bbox
        
#         face_w, face_h = x2 - x1, y2 - y1
#         pad_x, pad_y = int(face_w * padding_ratio), int(face_h * padding_ratio)

#         crop_x1 = max(0, x1 - pad_x)
#         crop_y1 = max(0, y1 - pad_y)
#         crop_x2 = min(width, x2 + pad_x)
#         crop_y2 = min(height, y2 + pad_y)

#         return image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

#     def save_face_crop(self, face_crop: Image.Image, output_path: str):
#         Path(output_path).parent.mkdir(parents=True, exist_ok=True)
#         face_crop.save(output_path)