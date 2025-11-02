# REST API Документация

## Базовый URL
```
http://localhost:8000/api  # для разработки
https://your-domain.com/api  # для продакшена
```

## Эндпоинты

### Уведомления

#### GET `/api/notifications`
Получить список уведомлений с фильтрацией и пагинацией

**Query параметры:**
- `type` (optional): Тип уведомления (`file_upload`, `record_create`, `record_update`, `record_delete`, `user_action`)
- `user_id` (optional): ID пользователя
- `status` (optional): Статус (`read`, `unread`)
- `limit` (optional): Количество записей (1-1000, по умолчанию 100)
- `offset` (optional): Смещение для пагинации (по умолчанию 0)

**Пример запроса:**
```bash
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

#### GET `/api/notifications/{notification_id}`
Получить уведомление по ID

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
  "metadata": {...}
}
```

---

#### POST `/api/notifications`
Создать новое уведомление

**Тело запроса:**
```json
{
  "type": "file_upload",
  "title": "Загрузка файла",
  "description": "Загружен файл report.xlsx в таблицу Документы",
  "user_id": "manager_a",
  "user_name": "Менеджер А",
  "source": "airtable",
  "details": {
    "table_name": "Документы",
    "file_type": "XLSX",
    "attachment_url": "https://..."
  },
  "metadata": {
    "base_id": "appXXX",
    "table_id": "tblXXX"
  }
}
```

**Ответ:** 201 Created с данными созданного уведомления

---

#### PATCH `/api/notifications/{notification_id}`
Обновить уведомление

**Тело запроса:**
```json
{
  "read": true
}
```

---

#### POST `/api/notifications/{notification_id}/read`
Отметить уведомление как прочитанное

**Ответ:**
```json
{
  "id": 1,
  "status": "read",
  ...
}
```

---

#### POST `/api/notifications/batch/read`
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
  "updated": [1, 2, 3],
  "not_found": [4, 5],
  "total_updated": 3
}
```

---

### Статистика

#### GET `/api/stats`
Получить статистику уведомлений

**Query параметры:**
- `user_id` (optional): Фильтр по пользователю

**Ответ:**
```json
{
  "total": 150,
  "unread": 45,
  "today": 12,
  "by_type": {
    "file_upload": 50,
    "record_create": 40,
    "record_update": 35,
    "record_delete": 15,
    "user_action": 10
  },
  "by_user": {
    "Менеджер А": 60,
    "Менеджер Б": 50,
    "Менеджер В": 40
  }
}
```

---

### Webhooks

#### POST `/api/webhooks/airtable`
Webhook для приема событий из Airtable

**Настройка:**
1. Перейти в Airtable → Settings → Webhooks
2. Создать новый webhook
3. Указать URL: `https://your-domain.com/api/webhooks/airtable`
4. Выбрать события: `record.created`, `record.updated`, `attachment.created`

**Ответ:**
```json
{
  "status": "success",
  "notification_id": 123,
  "message": "Уведомление создано"
}
```

---

#### GET `/api/webhooks/airtable/test`
Тестовый эндпоинт для создания уведомления (для разработки)

---

## Типы уведомлений

- `file_upload` - Загрузка файла
- `record_create` - Создание записи
- `record_update` - Обновление записи
- `record_delete` - Удаление записи
- `user_action` - Действие пользователя

## Статусы уведомлений

- `unread` - Непрочитанное
- `read` - Прочитанное

---

## Коды ошибок

- `400` - Невалидный запрос
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

