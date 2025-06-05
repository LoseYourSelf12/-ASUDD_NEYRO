# Коммуникация с сервером и приём команд
from fastapi import FastAPI, Request
import uvicorn
import httpx
from logger import Logger
from skneyro_protocol import SkNeuroProtocol

logger_obj = Logger()
app = FastAPI()

protocol_instance: SkNeuroProtocol | None = None

@app.post("/command")
async def receive_command(request: Request):
    """Обработчик входящих команд от сервера."""
    data = await request.json()
    logger_obj.log(f"Received command: {data}", "INFO")
    if protocol_instance:
        parsed = protocol_instance.parse_message(data.get("message", ""))
        logger_obj.log(f"Parsed command: {parsed}", "DEBUG")
    return {"status": "Command received", "data": data}

async def send_post(url, data):
    """Отправка POST-запроса с результатами детекции."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
        logger_obj.log(f"Sent POST to {url}, response: {response.status_code}", "INFO")
    except Exception as e:
        logger_obj.log(f"Error sending POST: {e}", "ERROR")

async def start_communicator(protocol: SkNeuroProtocol, host="0.0.0.0", port=8000):
    """Запуск FastAPI сервера для приёма команд."""
    global protocol_instance
    protocol_instance = protocol
    config = uvicorn.Config(app, host=host, port=port, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()
