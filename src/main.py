# Главный модуль запуска детектора
import asyncio
import cv2
import time
from detector import YOLOv8Detector
from aggregator import DataAggregator
from config_manager import ConfigManager
from skneyro_protocol import SkNeuroProtocol
from communicator import send_post, start_communicator
from logger import Logger

logger_obj = Logger()

async def detection_loop(detector, aggregator, config: ConfigManager, server_url):
    """Асинхронный цикл детекции и отправки результатов."""
    cap = cv2.VideoCapture(config.settings.detector.video_source)
    fps_count = 0
    start_time = time.time()
    process_interval = config.settings.pti.interval

    while True:
        frame_start = time.time()
        ret, frame = cap.read()
        if not ret:
            logger_obj.log("Frame capture failed", "ERROR")
            await asyncio.sleep(1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        boxes, scores, class_ids = await asyncio.to_thread(detector.detect, frame)
        agg_data = aggregator.aggregate_detections(boxes, scores, class_ids)
        await send_post(server_url, agg_data)

        fps_count += 1
        elapsed = time.time() - start_time
        if elapsed >= 1.0:
            logger_obj.log(f"FPS: {fps_count / elapsed:.2f}", "INFO")
            fps_count = 0
            start_time = time.time()

        await asyncio.sleep(max(0, process_interval - (time.time() - frame_start)))

async def main():
    """Точка входа приложения."""
    config = ConfigManager()
    detector = YOLOv8Detector(model_path=config.settings.detector.model_path)
    aggregator = DataAggregator(config.settings)
    protocol = SkNeuroProtocol(config.settings)

    server_url = config.settings.ndc.adr_1
    communicator_task = asyncio.create_task(start_communicator(protocol))
    detection_task = asyncio.create_task(detection_loop(detector, aggregator, config, server_url))

    try:
        while True:
            status_msg = protocol.get_status_message()
            logger_obj.log(f"Status: {status_msg}", "INFO")
            await asyncio.sleep(30)
    finally:
        communicator_task.cancel()
        detection_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
