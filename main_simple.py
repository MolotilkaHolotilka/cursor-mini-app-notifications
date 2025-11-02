from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Telegram Mini App - Notification System",
    description="Frontend для системы уведомлений",
    version="1.0.0"
)

# Статические файлы (CSS, JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

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
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

