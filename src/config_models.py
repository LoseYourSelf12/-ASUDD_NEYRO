from pydantic import BaseModel

class NDC(BaseModel):
    apply: bool = False
    Time_zone: str = "+3"
    type_id: int = 101
    id: str = "Demo"
    zone_pref: str = "1"
    Name_Obj: str = "Test_Van_1"
    adr_1: str = "http://192.168.2.100:8000"
    adr_2: str = "http://192.168.2.101:8000"

class PTI(BaseModel):
    apply: bool = True
    interval: int = 15
    tim_beg: str = "00:00:00"

class DII(BaseModel):
    apply: bool = True
    display: int = 0

class DetectorConfig(BaseModel):
    model_path: str = "models/yolov8n.onnx"
    video_source: str = "video/test_vid.mp4"
    vehicle_class_id: int = 2

class Settings(BaseModel):
    NDC: NDC = NDC()
    PTI: PTI = PTI()
    DII: DII = DII()
    DETECTOR: DetectorConfig = DetectorConfig()
