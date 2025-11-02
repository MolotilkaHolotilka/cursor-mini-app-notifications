# Деплой на Coolify

## Структура проекта для Coolify

Coolify может работать с несколькими подходами:

### Вариант 1: Только FastAPI (рекомендуется для начала)

FastAPI будет обслуживать и API, и статический фронтенд.

---

## Шаг 1: Подготовка проекта

### 1.1. Обновить main.py для статики

Добавьте обслуживание статических файлов в `main.py`:

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# В конце файла, перед запуском
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def read_root():
    return FileResponse('index.html')

@app.get("/index.html", include_in_schema=False)
async def read_index():
    return FileResponse('index.html')
```

### 1.2. Обновить Dockerfile

Dockerfile уже создан и готов к использованию.

### 1.3. Создать папку для статики

```bash
mkdir static
cp index.html static/
cp styles.css static/
cp app.js static/
```

---

## Шаг 2: Деплой на Coolify

### 2.1. Подключение репозитория

1. Зайдите в Coolify
2. Создайте новый проект
3. Выберите "Git Repository"
4. Подключите ваш GitHub/GitLab репозиторий

### 2.2. Настройка сборки

**Build Pack:** Dockerfile

**Dockerfile Path:** `./Dockerfile`

**Port:** `8000`

### 2.3. Переменные окружения

Добавьте в настройках Coolify:

```env
DATABASE_URL=sqlite+aiosqlite:///./notifications.db
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://your-domain.com,https://web.telegram.org
```

### 2.4. Volumes (для SQLite)

Если используете SQLite, добавьте volume для базы данных:

```
/app/notifications.db
```

Или лучше переключиться на PostgreSQL (см. ниже).

---

## Шаг 3: Обновить фронтенд

В `app.js` измените URL API:

```javascript
const API_BASE_URL = 'https://your-coolify-domain.com/api';
```

Или используйте относительный путь:

```javascript
const API_BASE_URL = '/api';
```

---

## Вариант 2: Отдельный статический фронтенд

### 2.1. FastAPI только для API

FastAPI остается как есть, без статики.

### 2.2. Фронтенд через статический хостинг

Разверните фронтенд отдельно:
- **Vercel** (рекомендуется)
- **Netlify**
- **Cloudflare Pages**
- Или через Coolify Static Site

---

## Рекомендации для продакшена

### 1. PostgreSQL вместо SQLite

Обновите `database.py`:

```python
import os
from urllib.parse import quote_plus

# PostgreSQL для продакшена
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{quote_plus(os.getenv('DB_USER', 'user'))}:{quote_plus(os.getenv('DB_PASSWORD', 'password'))}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'notifications')}"
)
```

Добавьте в `requirements.txt`:

```
asyncpg>=0.29.0
psycopg2-binary>=2.9.9
```

### 2. Настроить CORS правильно

В `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://web.telegram.org",
        "https://your-telegram-miniapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Добавить переменные окружения

Создайте `.env` файл или настройте в Coolify:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# Server
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=https://your-domain.com

# Telegram (опционально)
TELEGRAM_BOT_TOKEN=your_token

# Airtable (опционально)
AIRTABLE_API_KEY=your_key
```

---

## Структура для Coolify

```
your-project/
├── Dockerfile          # Для FastAPI
├── docker-compose.yml  # Опционально
├── .dockerignore
├── requirements.txt
├── main.py
├── models.py
├── database.py
├── services.py
├── routers/
│   ├── __init__.py
│   ├── notifications.py
│   ├── webhooks.py
│   └── stats.py
├── static/             # Статика (если вариант 1)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── index.html          # Для локальной разработки
├── styles.css
├── app.js
└── .env.example
```

---

## Проверка после деплоя

1. **Health Check:**
   ```
   https://your-domain.com/health
   ```

2. **API Docs:**
   ```
   https://your-domain.com/docs
   ```

3. **Frontend:**
   ```
   https://your-domain.com/
   ```

---

## Troubleshooting

### Ошибка подключения к БД
- Проверьте DATABASE_URL
- Убедитесь, что volume настроен правильно (для SQLite)
- Для PostgreSQL проверьте доступность БД

### CORS ошибки
- Проверьте ALLOWED_ORIGINS
- Убедитесь, что домен указан правильно

### Статика не загружается
- Проверьте, что файлы скопированы в static/
- Проверьте пути в app.js

---

## Следующие шаги

После успешного деплоя:
1. Настроить домен
2. Добавить SSL сертификат (автоматически через Coolify)
3. Настроить Telegram бота
4. Интегрировать Airtable webhooks

