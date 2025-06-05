# src/communicator.py
from fastapi import FastAPI, Request
import uvicorn
from logger import Logger
from skneyro_protocol import SkNeuroProtocol

logger_obj = Logger()
app = FastAPI()

protocol_instance = None

@app.post("/command")
async def receive_command(request: Request):
    data = await request.json()
    logger_obj.log(f"Received command: {data}", "INFO")
    # Здесь можно добавить обработку команд с помощью protocol_instance.parse_message() или иного
    return {"status": "Command received", "data": data}

def send_post(url, data):
    import requests
    try:
        # response = requests.post(url, json=data)
        # logger_obj.log(f"Sent POST to {url}, response: {response.status_code}", "INFO")
        logger_obj.log(f"Sent POST to {url}, response: {200}", "INFO")
    except Exception as e:
        logger_obj.log(f"Error sending POST: {e}", "ERROR")

def start_communicator(protocol, host="0.0.0.0", port=8000):
    global protocol_instance
    protocol_instance = protocol
    uvicorn.run(app, host=host, port=port)
