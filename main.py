from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from database import init_db
from routers import notifications, stats, webhooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация при запуске
    await init_db()
    yield
    # Очистка при завершении (если нужно)

app = FastAPI(
    title="Telegram Mini App - Notification System",
    description="API для системы уведомлений",
    version="1.0.0",
    lifespan=lifespan
)

# CORS настройки для GitHub Pages и Telegram WebApp
allowed_origins = [
    "https://molotilkaholotilka.github.io",
    "https://notification.rybushk.in",
    "https://web.telegram.org",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]

# Добавляем разрешенные origin из переменной окружения (если указаны)
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роутеры
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

# Статические файлы (CSS, JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check для Coolify
@app.get("/health")
async def health():
    return {"status": "ok", "message": "App is running"}

# Главная страница - отдаем index.html
@app.get("/", include_in_schema=False)
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "index.html not found"}

@app.get("/index.html", include_in_schema=False)
async def index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "index.html not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Отключено для продакшена
        log_level="info"
    )

