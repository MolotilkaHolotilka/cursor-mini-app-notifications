FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем только необходимые зависимости (FastAPI для статики)
RUN pip install --no-cache-dir fastapi uvicorn[standard]

# Копируем упрощенный main.py
COPY main.py .

# Копируем статические файлы
COPY static/ ./static/

# Открываем порт
EXPOSE 8000

# Запускаем упрощенное приложение (только статика)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

