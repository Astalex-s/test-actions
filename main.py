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
            "/date": "Get current server date",
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


@app.get("/date")
async def get_server_date() -> Dict[str, str]:
    """Возвращает текущую дату сервера"""
    current_date = datetime.now()
    return {
        "date": current_date.strftime("%Y-%m-%d"),
        "day": current_date.strftime("%A"),
        "day_number": current_date.strftime("%d"),
        "month": current_date.strftime("%B"),
        "month_number": current_date.strftime("%m"),
        "year": current_date.strftime("%Y"),
        "iso_date": current_date.date().isoformat()
    }

