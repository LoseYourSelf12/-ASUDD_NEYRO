# SkNeuro Detector

This project implements a small prototype of a vehicle detector that counts cars in video frames and periodically sends the result to a remote server. Detection is performed with a YOLOv8 model in ONNX format. A FastAPI application listens for control commands while the detection loop runs asynchronously.

## Requirements

- Python 3.10+
- Packages listed in `requirements.txt`

Install dependencies using

```bash
pip install -r requirements.txt
```

## Configuration

Settings are stored in `configs/skneyro_config.yaml`. A default file will be created on first run. Important options include:

- `DETECTOR.model_path` – path to the ONNX model
- `DETECTOR.video_source` – path to the video file or camera index
- `DETECTOR.vehicle_class_id` – class id that should be counted
- `PTI.interval` – delay between detections in seconds
- `NDC.adr_1` – URL of the server that receives results

Edit this file to match your environment.

## Running

Start the application with

```bash
python src/main.py
```

The FastAPI server will run on port `8000` by default (see `communicator.py`).
Detection results are posted to the configured `NDC.adr_1` endpoint.

## Testing the System

1. Place a test video at the path specified in `DETECTOR.video_source`.
2. Ensure the server URL in `NDC.adr_1` is reachable or use a tool like `httpbin.org/post` for testing.
3. Run the application. Logs will show FPS information and POST request status.
4. To send a command, POST JSON to `http://localhost:8000/command` with a `message` field containing a protocol string. The message will be parsed and logged.

This setup is suitable for experimenting on a regular PC or on micro‑computers such as Jetson Nano (with the TensorRT execution provider enabled when available).
