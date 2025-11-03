FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY main.py .
COPY database.py .
COPY models.py .
COPY services.py .
COPY routers/ ./routers/

# Копируем статические файлы (из корня и из static/)
COPY index.html .
COPY app.js .
COPY styles.css .
COPY static/ ./static/

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

