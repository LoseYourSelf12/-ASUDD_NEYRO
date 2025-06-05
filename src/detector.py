# src/detector.py
import cv2
import onnxruntime as ort
import numpy as np
from logger import Logger

logger_obj = Logger()

class YOLOv8Detector:
    def __init__(self, model_path='models/yolov8n.onnx', providers=['CUDAExecutionProvider', 'CPUExecutionProvider']):
        self.model_path = model_path
        self.session = ort.InferenceSession(model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name
        logger_obj.log(f"Loaded ONNX model from {model_path}", "INFO")

    def preprocess(self, frame):
        img = cv2.resize(frame, (640, 640))
        img = img.transpose(2, 0, 1)  # CHW
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def postprocess(self, outputs, conf_threshold=0.3):
        detections = outputs[0]
        # Если выход имеет форму (1, N, 6), убираем батч-измерение.
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
        preprocessed = self.preprocess(frame)
        outputs = self.session.run(None, {self.input_name: preprocessed})
        boxes, scores, class_ids = self.postprocess(outputs)
        logger_obj.log(f"Detected {len(boxes)} objects. Class IDs: {class_ids} Scores: {scores}", "DEBUG")
        return boxes, scores, class_ids
