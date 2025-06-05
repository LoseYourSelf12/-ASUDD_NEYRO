# src/aggregator.py
from logger import Logger

logger_obj = Logger()

class DataAggregator:
    def __init__(self, config):
        self.config = config

    def aggregate_detections(self, boxes, scores, class_ids):
        # Простой пример: считаем количество автомобилей (предположим, class_id == 2 означает автомобиль)
        vehicle_count = sum(1 for cid in class_ids if cid == 2)
        logger_obj.log(f"Aggregated vehicle count: {vehicle_count}", "DEBUG")
        return {"vehicle_count": vehicle_count}
