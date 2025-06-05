# Модуль работы с моделью YOLO
import cv2
import onnxruntime as ort
import numpy as np
from logger import Logger

logger_obj = Logger()

class YOLOv8Detector:
    """Класс обёртки над ONNX-моделью YOLOv8."""

    def __init__(self, model_path='models/yolov8n.onnx', providers=None):
        """Инициализация с выбором доступных провайдеров."""
        self.model_path = model_path
        if providers is None:
            providers = [
                'TensorrtExecutionProvider',
                'CUDAExecutionProvider',
                'CPUExecutionProvider'
            ]
        try:
            self.session = ort.InferenceSession(model_path, providers=providers)
            self.input_name = self.session.get_inputs()[0].name
            logger_obj.log(f"Loaded ONNX model from {model_path}", "INFO")
            logger_obj.log(f"Execution providers: {self.session.get_providers()}", "DEBUG")
        except Exception as e:
            logger_obj.log(f"Failed to load model {model_path}: {e}", "ERROR")
            raise

    def preprocess(self, frame):
        """Подготовка кадра к подаче в модель."""
        img = cv2.resize(frame, (640, 640))
        img = img.transpose(2, 0, 1)  # CHW
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def postprocess(self, outputs, conf_threshold=0.3):
        """Постобработка выходов модели."""
        detections = outputs[0]
        if len(detections.shape) == 3:
            detections = detections[0]
        boxes = []
        scores = []
        class_ids = []
        for detection in detections:
            score = detection[4]
            if score > conf_threshold:
                boxes.append(detection[:4])
                scores.append(score)
                class_ids.append(int(detection[5]))
        return boxes, scores, class_ids

    def detect(self, frame):
        """Выполняет детекцию на одном кадре."""
        preprocessed = self.preprocess(frame)
        outputs = self.session.run(None, {self.input_name: preprocessed})
        boxes, scores, class_ids = self.postprocess(outputs)
        logger_obj.log(
            f"Detected {len(boxes)} objects. Class IDs: {class_ids} Scores: {scores}",
            "DEBUG",
        )
        return boxes, scores, class_ids
