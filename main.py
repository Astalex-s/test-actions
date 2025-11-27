from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from typing import Dict
from zoneinfo import ZoneInfo

app = FastAPI(title="Server Time API", version="1.0.0")

# Маппинг названий городов на часовые пояса IANA
TIMEZONE_MAP = {
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg",
    "ekaterinburg": "Asia/Yekaterinburg",
    "санкт-петербург": "Europe/Moscow",
    "saint-petersburg": "Europe/Moscow",
    "st-petersburg": "Europe/Moscow",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "красноярск": "Asia/Krasnoyarsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "irkutsk": "Asia/Irkutsk",
    "владивосток": "Asia/Vladivostok",
    "vladivostok": "Asia/Vladivostok",
    "нью-йорк": "America/New_York",
    "new-york": "America/New_York",
    "лондон": "Europe/London",
    "london": "Europe/London",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "шанхай": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "берлин": "Europe/Berlin",
    "berlin": "Europe/Berlin",
    "париж": "Europe/Paris",
    "paris": "Europe/Paris",
    "сидней": "Australia/Sydney",
    "sydney": "Australia/Sydney",
}


@app.get("/")
async def root() -> Dict[str, str]:
    """Корневой эндпоинт с информацией о API"""
    return {
        "message": "Server Time API",
        "endpoints": {
            "/time": "Get current server time",
            "/date": "Get current server date",
            "/convert-time": "Convert time from UTC to specified timezone",
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


@app.get("/convert-time")
async def convert_time(
    time: str = Query(..., description="Время в UTC в формате HH:MM или HH:MM:SS"),
    timezone: str = Query(..., description="Название города или часового пояса (например: Екатеринбург, Moscow, Asia/Yekaterinburg)")
) -> Dict[str, str]:
    """
    Конвертирует время из UTC в указанный часовой пояс.
    
    Примеры:
    - time=15:00&timezone=Екатеринбург → 20:00 (UTC+5)
    - time=15:00&timezone=Asia/Yekaterinburg → 20:00
    """
    try:
        # Парсим время
        time_parts = time.split(":")
        if len(time_parts) < 2:
            raise ValueError("Неверный формат времени. Используйте HH:MM или HH:MM:SS")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2]) if len(time_parts) > 2 else 0
        
        if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
            raise ValueError("Время вне допустимого диапазона")
        
        # Создаем datetime в UTC
        utc_time = datetime.now(ZoneInfo("UTC")).replace(
            hour=hour, minute=minute, second=second, microsecond=0
        )
        
        # Определяем часовой пояс
        timezone_lower = timezone.lower().strip()
        tz_name = TIMEZONE_MAP.get(timezone_lower)
        
        if not tz_name:
            # Пробуем использовать переданное значение как IANA timezone name
            try:
                tz = ZoneInfo(timezone)
            except Exception as e:
                error_msg = str(e)
                if "No such file or directory" in error_msg or "zoneinfo" in error_msg.lower():
                    raise HTTPException(
                        status_code=500,
                        detail=f"Ошибка работы с часовыми поясами. Убедитесь, что tzdata установлен. Ошибка: {error_msg}"
                    )
                raise HTTPException(
                    status_code=400,
                    detail=f"Неизвестный часовой пояс: {timezone}. "
                           f"Доступные города: {', '.join(set([k for k in TIMEZONE_MAP.keys() if not '/' in k]))}"
                )
        else:
            try:
                tz = ZoneInfo(tz_name)
            except Exception as e:
                error_msg = str(e)
                if "No such file or directory" in error_msg or "zoneinfo" in error_msg.lower():
                    raise HTTPException(
                        status_code=500,
                        detail=f"Ошибка работы с часовыми поясами. Убедитесь, что tzdata установлен. Ошибка: {error_msg}"
                    )
                raise
        
        # Конвертируем в указанный часовой пояс
        converted_time = utc_time.astimezone(tz)
        
        return {
            "utc_time": utc_time.strftime("%H:%M:%S"),
            "utc_time_iso": utc_time.isoformat(),
            "timezone": str(tz),
            "converted_time": converted_time.strftime("%H:%M:%S"),
            "converted_time_full": converted_time.strftime("%Y-%m-%d %H:%M:%S"),
            "converted_time_iso": converted_time.isoformat(),
            "timezone_offset": converted_time.strftime("%z")
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка конвертации: {str(e)}")

