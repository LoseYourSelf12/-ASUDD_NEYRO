# src/main.py
import cv2
import threading
import time
from detector import YOLOv8Detector
from aggregator import DataAggregator
from config_manager import ConfigManager
from skneyro_protocol import SkNeuroProtocol
from communicator import send_post, start_communicator
from logger import Logger

logger_obj = Logger()

def detection_loop(detector, aggregator, config, server_url):
    # Используем видеофайл (путь к видео, см. предыдущие изменения)
    cap = cv2.VideoCapture("video/test_vid.mp4")
    
    fps_count = 0
    start_time = time.time()
    
    # Если требуется обработка в реальном времени, можно убрать sleep или установить короткий интервал.
    process_interval = config.config.get("PTI", {}).get("interval", 15)
    
    while True:
        frame_start = time.time()
        ret, frame = cap.read()
        if not ret:
            logger_obj.log("Frame capture failed", "ERROR")
            time.sleep(1)
            # Если видео закончено, начинаем сначала:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        boxes, scores, class_ids = detector.detect(frame)
        agg_data = aggregator.aggregate_detections(boxes, scores, class_ids)
        send_post(server_url, agg_data)
        
        fps_count += 1
        elapsed = time.time() - start_time
        if elapsed >= 1.0:
            logger_obj.log(f"FPS: {fps_count / elapsed:.2f}", "INFO")
            fps_count = 0
            start_time = time.time()

def main():
    config = ConfigManager()
    detector = YOLOv8Detector(model_path='models/yolov8n.onnx')
    aggregator = DataAggregator(config.config)
    protocol = SkNeuroProtocol(config.config)

    # Запускаем цикл детекции в отдельном потоке
    server_url = config.config.get("NDC", {}).get("adr_1", "http://192.168.2.100:8000")
    detection_thread = threading.Thread(target=detection_loop, args=(detector, aggregator, config, server_url), daemon=True)
    detection_thread.start()

    # Запускаем FastAPI сервер для приёма команд в отдельном потоке
    communicator_thread = threading.Thread(target=start_communicator, args=(protocol,), daemon=True)
    communicator_thread.start()

    # Основной цикл – периодически выводим статус детектора
    while True:
        status_msg = protocol.get_status_message()
        logger_obj.log(f"Status: {status_msg}", "INFO")
        time.sleep(30)

if __name__ == "__main__":
    main()
