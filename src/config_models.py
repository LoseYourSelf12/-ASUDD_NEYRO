# Описание моделей конфигурации
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict

class NDC(BaseModel):
    """Настройки подключения к серверу."""

    apply: bool = False
    Time_zone: str = "+3"
    type_id: int = 101
    id: str = "Demo"
    zone_pref: str = "1"
    Name_Obj: str = "Test_Van_1"
    adr_1: str = "http://192.168.2.100:8000"
    adr_2: str = "http://192.168.2.101:8000"

class PTI(BaseModel):
    """Настройки периодической передачи данных."""

    apply: bool = True
    interval: int = 15
    tim_beg: str = "00:00:00"

class DII(BaseModel):
    """Параметры отображения отладочной информации."""

    apply: bool = True
    display: int = 0

class DetectorConfig(BaseModel):
    """Конфигурация детектора."""

    model_path: str = "models/yolov8n.onnx"
    video_source: str = "video/test_vid.mp4"
    vehicle_class_id: int = 2

class Settings(BaseModel):
    """Объединённые настройки всей системы."""

    model_config = ConfigDict(populate_by_name=True)

    ndc: NDC = Field(default_factory=NDC, alias="NDC")
    pti: PTI = Field(default_factory=PTI, alias="PTI")
    dii: DII = Field(default_factory=DII, alias="DII")
    detector: DetectorConfig = Field(default_factory=DetectorConfig, alias="DETECTOR")