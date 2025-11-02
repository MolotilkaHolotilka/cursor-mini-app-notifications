from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum
import uvicorn
import os

from database import init_db, get_db, Notification, NotificationStatus
from services import NotificationService, AirtableService
from routers import notifications, webhooks, stats

app = FastAPI(
    title="Telegram Mini App - Notification System",
    description="REST API для системы уведомлений Telegram Mini App",
    version="1.0.0"
)

# CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация БД при старте
@app.on_event("startup")
async def startup_event():
    await init_db()
    print("✅ База данных инициализирована")

# Подключение роутеров
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

# Статические файлы (CSS, JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Главная страница - отдаем index.html
@app.get("/", include_in_schema=False)
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    return {
        "status": "ok",
        "message": "Notification System API",
        "version": "1.0.0"
    }

@app.get("/index.html", include_in_schema=False)
async def index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    raise HTTPException(status_code=404, detail="index.html not found")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

