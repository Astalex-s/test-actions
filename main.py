from fastapi import FastAPI
from datetime import datetime
from typing import Dict

app = FastAPI(title="Server Time API", version="1.0.0")


@app.get("/")
async def root() -> Dict[str, str]:
    """Корневой эндпоинт с информацией о API"""
    return {
        "message": "Server Time API",
        "endpoints": {
            "/time": "Get current server time",
            "/": "API information"
        }
    }


@app.get("/time")
async def get_server_time() -> Dict[str, str]:
    """Возвращает текущее время сервера"""
    current_time = datetime.now()
    return {
        "server_time": current_time.isoformat(),
        "timestamp": current_time.timestamp(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

