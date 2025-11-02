# 📋 Список всех эндпоинтов API

**Базовый URL:** `http://v44sc0ok08gsoow80044w48c.91.107.212.137.sslip.io`

**Документация:** 
- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## 🔍 Системные эндпоинты

### `GET /health`
Проверка работоспособности сервера

**Ответ:**
```json
{
  "status": "ok",
  "message": "App is running"
}
```

---

## 🔔 Уведомления (`/api/notifications`)

### `GET /api/notifications`
Получить список уведомлений с фильтрацией и пагинацией

**Query параметры:**
- `type` (optional): Тип уведомления
  - `file_upload` - загрузка файлов
  - `record_create` - создание записей
  - `record_update` - обновление записей
  - `record_delete` - удаление записей
  - `user_action` - действия пользователей
- `user_id` (optional): ID пользователя
- `status` (optional): Статус
  - `read` - прочитано
  - `unread` - непрочитано
- `limit` (optional, default: 100): Количество записей (1-1000)
- `offset` (optional, default: 0): Смещение для пагинации

**Пример запроса:**
```
GET /api/notifications?type=file_upload&limit=50&offset=0
```

**Ответ:**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "file_upload",
      "title": "Загрузка файла",
      "description": "Загружен файл report.xlsx",
      "user_id": "manager_a",
      "user_name": "Менеджер А",
      "source": "airtable",
      "status": "unread",
      "timestamp": "2024-01-01T12:00:00",
      "details": {
        "table_name": "Документы",
        "file_type": "XLSX"
      },
      "metadata": null
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

---

### `GET /api/notifications/{notification_id}`
Получить уведомление по ID

**Параметры:**
- `notification_id` (path): ID уведомления

**Пример:**
```
GET /api/notifications/1
```

**Ответ:**
```json
{
  "id": 1,
  "type": "file_upload",
  "title": "Загрузка файла",
  "description": "Загружен файл report.xlsx",
  "user_id": "manager_a",
  "user_name": "Менеджер А",
  "source": "airtable",
  "status": "unread",
  "timestamp": "2024-01-01T12:00:00",
  "details": {...},
  "metadata": null
}
```

---

### `POST /api/notifications`
Создать новое уведомление

**Тело запроса:**
```json
{
  "type": "file_upload",
  "title": "Загрузка файла",
  "description": "Загружен файл report.xlsx",
  "user_id": "manager_a",
  "user_name": "Менеджер А",
  "source": "airtable",
  "details": {
    "table_name": "Документы",
    "file_type": "XLSX"
  }
}
```

**Ответ:** (201 Created)
```json
{
  "id": 1,
  "type": "file_upload",
  "title": "Загрузка файла",
  ...
}
```

---

### `PATCH /api/notifications/{notification_id}`
Обновить уведомление

**Параметры:**
- `notification_id` (path): ID уведомления

**Тело запроса:**
```json
{
  "status": "read",
  "title": "Новый заголовок",
  "description": "Новое описание"
}
```

---

### `POST /api/notifications/{notification_id}/read`
Отметить уведомление как прочитанное

**Параметры:**
- `notification_id` (path): ID уведомления

**Пример:**
```
POST /api/notifications/1/read
```

**Ответ:**
```json
{
  "id": 1,
  "status": "read",
  ...
}
```

---

### `POST /api/notifications/batch/read`
Отметить несколько уведомлений как прочитанные

**Тело запроса:**
```json
{
  "notification_ids": [1, 2, 3, 4, 5]
}
```

**Ответ:**
```json
{
  "updated": [1, 2, 3, 4, 5],
  "not_found": [],
  "total_updated": 5
}
```

---

## 📊 Статистика (`/api/stats`)

### `GET /api/stats`
Получить статистику уведомлений

**Query параметры:**
- `user_id` (optional): Фильтр по пользователю

**Пример:**
```
GET /api/stats?user_id=manager_a
```

**Ответ:**
```json
{
  "total": 150,
  "unread": 25,
  "today": 10,
  "by_type": {
    "file_upload": 50,
    "record_create": 40,
    "record_update": 30,
    "record_delete": 20,
    "user_action": 10
  },
  "by_user": {
    "manager_a": 60,
    "manager_b": 50,
    "manager_c": 40
  }
}
```

---

## 🪝 Webhooks (`/api/webhooks`)

### `POST /api/webhooks/airtable`
Webhook для приема событий из Airtable

**Тело запроса (формат Airtable):**
```json
{
  "event": "record.created",
  "base": {
    "id": "base_id"
  },
  "webhook": {
    "id": "webhook_id"
  },
  "timestamp": "2024-01-01T00:00:00.000Z",
  "payload": {
    "tables": [
      {
        "id": "table_id",
        "name": "Table Name",
        "records": [
          {
            "id": "record_id",
            "fields": {
              "Name": "Record Name"
            }
          }
        ]
      }
    ],
    "eventMetadata": {
      "source": "airtable",
      "sourceMetadata": {
        "user": {
          "id": "user_id",
          "email": "user@example.com",
          "name": "User Name"
        }
      }
    }
  }
}
```

**Ответ:**
```json
{
  "status": "success",
  "notification_id": 1,
  "message": "Уведомление создано"
}
```

---

### `GET /api/webhooks/airtable/test`
Тестовый эндпоинт для создания уведомления (для разработки)

**Пример:**
```
GET /api/webhooks/airtable/test
```

**Ответ:**
```json
{
  "status": "success",
  "notification": {
    "id": 1,
    "title": "Тестовое уведомление",
    "description": "Тестовое описание",
    "type": "file_upload",
    "user_name": "Тестовый пользователь"
  }
}
```

---

## 📄 Статические файлы

### `GET /`
Главная страница (отдает `index.html`)

### `GET /index.html`
Альтернативный путь к главной странице

### `GET /static/{file}`
Статические файлы (CSS, JS, изображения)

---

## 🛠️ Документация

### `GET /docs`
Swagger UI - интерактивная документация API

### `GET /redoc`
ReDoc - альтернативная документация API

---

## 📝 Примеры использования

### Получить все непрочитанные уведомления:
```
GET /api/notifications?status=unread&limit=100
```

### Получить уведомления определенного типа за сегодня:
```
GET /api/notifications?type=file_upload&limit=50
```

### Получить статистику для конкретного пользователя:
```
GET /api/stats?user_id=manager_a
```

### Отметить уведомление как прочитанное:
```
POST /api/notifications/1/read
```

### Создать уведомление вручную:
```
POST /api/notifications
Content-Type: application/json

{
  "type": "user_action",
  "title": "Действие пользователя",
  "description": "Описание действия",
  "user_id": "user_123",
  "user_name": "Имя пользователя",
  "source": "manual"
}
```


