# Модуль агрегатора данных
from logger import Logger
from config_models import Settings

logger_obj = Logger()

class DataAggregator:
    """Агрегация результатов детекции."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def aggregate_detections(self, boxes, scores, class_ids):
        """Подсчёт объектов заданного класса."""
        vehicle_class = self.settings.DETECTOR.vehicle_class_id
        vehicle_count = sum(1 for cid in class_ids if cid == vehicle_class)
        logger_obj.log(f"Aggregated vehicle count: {vehicle_count}", "DEBUG")
        return {"vehicle_count": vehicle_count}
