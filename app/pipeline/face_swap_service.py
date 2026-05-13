#app/pipeline/face_swap_service.py

import cv2
import insightface
from insightface.app import FaceAnalysis
import numpy as np
from PIL import Image

class FaceSwapService:
    def __init__(self):
        # Khởi tạo FaceAnalysis để tìm mặt trong ảnh target
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        # Tải model swap mặt (inswapper_128.onnx)
        # Bạn cần tải file này từ internet hoặc hệ thống sẽ tự tải nếu cấu hình đúng
        # Sửa lại dòng nạp model trong __init__
        self.swapper = insightface.model_zoo.get_model(
            'app/models/inswapper_128.onnx', 
            download=False # Tắt tự động tải để tránh lỗi server chậm
        )

    def swap_face(self, source_face_path: str, target_image_path: str, output_path: str):
        # 1. Đọc ảnh
        img_source = cv2.imread(source_face_path)
        img_target = cv2.imread(target_image_path)

        # 2. Tìm mặt trong ảnh nguồn và ảnh đích
        face_source = self.app.get(img_source)[0] # Lấy mặt đầu tiên tìm thấy
        faces_target = self.app.get(img_target)

        if not faces_target:
            return None

        # 3. Thực hiện swap (thay thế tất cả mặt tìm thấy trong ảnh AI bằng mặt nguồn)
        result_img = img_target.copy()
        for face in faces_target:
            result_img = self.swapper.get(result_img, face, face_source, paste_back=True)

        # 4. Lưu kết quả
        cv2.imwrite(output_path, result_img)
        return output_path