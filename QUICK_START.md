# Быстрый старт - Тестирование

## Шаг 1: Запуск сервера

Два способа:

### Вариант А: Через скрипт (рекомендуется)
Дважды кликните на `start_server.bat`

### Вариант Б: Вручную
```bash
python main.py
```

Сервер запустится на **http://localhost:8000**

---

## Шаг 2: Проверка работы

### Способ 1: Через браузер
Откройте:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **Health Check**: http://localhost:8000/health

### Способ 2: Через тестовый скрипт
```bash
python test_api.py
```

Это создаст тестовые уведомления и покажет результаты.

---

## Шаг 3: Тестирование фронтенда

1. Откройте `index.html` в браузере
2. Или запустите HTTP сервер:
   ```bash
   python -m http.server 3000
   ```
3. Откройте http://localhost:3000

**Важно:** Убедитесь, что в `app.js` указан правильный URL:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## Что дальше?

1. ✅ Протестировать API локально
2. ⏳ Развернуть на хостинге
3. ⏳ Настроить Telegram бота
4. ⏳ Интегрировать с Airtable

---

## Полезные команды

**Остановить сервер:** Нажмите `Ctrl+C` в окне где запущен сервер

**Проверить работает ли сервер:**
```bash
curl http://localhost:8000/health
```

**Создать тестовое уведомление:**
```bash
python test_api.py
```

Или через браузер:
1. Откройте http://localhost:8000/docs
2. Найдите эндпоинт `POST /api/webhooks/airtable/test`
3. Нажмите "Try it out" → "Execute"

