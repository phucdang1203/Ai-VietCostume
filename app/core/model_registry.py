import os


class ModelRegistry:
    TEXT2IMG_MODEL = os.getenv(
        "TEXT2IMG_MODEL"
        # ,"nota-ai/bk-sdm-tiny"
        ,"runwayml/stable-diffusion-v1-5"
    )

    FACE_MODEL = os.getenv(
        "FACE_MODEL",
        "buffalo_l"
    )

    UPSCALER_MODEL = os.getenv(
        "UPSCALER_MODEL",
        "GFPGAN"
    )

    DEVICE = os.getenv(
        "DEVICE",
        "cpu"
    )

    @classmethod
    def get_text2img_model(cls):
        return cls.TEXT2IMG_MODEL

    @classmethod
    def get_face_model(cls):
        return cls.FACE_MODEL

    @classmethod
    def get_upscaler_model(cls):
        return cls.UPSCALER_MODEL

    @classmethod
    def get_device(cls):
        return cls.DEVICE



    # Model PhotoMaker-V2
    @staticmethod
    def get_base_model():
        return os.getenv(
            "MODEL_ID",
            "SG161222/RealVisXL_V4.0"
        )

    @staticmethod
    def get_photomaker_model():
        return os.getenv(
            "PHOTOMAKER_MODEL_ID",
            "TencentARC/PhotoMaker-V2"
        )

    @staticmethod
    def get_device():
        return os.getenv("DEVICE", "cuda")