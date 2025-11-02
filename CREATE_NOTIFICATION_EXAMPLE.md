# Пример создания уведомления

## Правильный curl запрос (БЕЗ лишних полей)

```bash
curl -X 'POST' \
  'http://q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io/api/notifications' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "file_upload",
  "title": "Тестовое уведомление",
  "description": "Это тестовое уведомление, созданное через API",
  "user_id": "test_user",
  "user_name": "Тестовый пользователь",
  "source": "manual"
}'
```

## Упрощенный вариант (только обязательные поля)

```bash
curl -X 'POST' \
  'http://q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io/api/notifications' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "file_upload",
  "title": "Тестовое уведомление",
  "description": "Описание уведомления",
  "user_id": "user123",
  "user_name": "Имя пользователя"
}'
```

## С дополнительными полями

```bash
curl -X 'POST' \
  'http://q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io/api/notifications' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "file_upload",
  "title": "Загрузка файла",
  "description": "Загружен файл report.xlsx",
  "user_id": "manager_a",
  "user_name": "Менеджер А",
  "source": "airtable",
  "details": {
    "table_name": "Документы",
    "file_type": "XLSX"
  },
  "metadata": {
    "event_id": "event123"
  }
}'
```

## Что НЕ нужно отправлять:

❌ **НЕ отправляйте эти поля** - они устанавливаются автоматически:
- `id` - генерируется автоматически
- `status` - по умолчанию "unread"
- `timestamp` - устанавливается автоматически как текущее время

## Типы уведомлений:

- `file_upload` - загрузка файлов
- `record_create` - создание записей
- `record_update` - обновление записей
- `record_delete` - удаление записей
- `user_action` - действия пользователей

## Проверка создания:

После создания вы получите ответ:
```json
{
  "id": 1,
  "type": "file_upload",
  "title": "Тестовое уведомление",
  "description": "Это тестовое уведомление",
  "user_id": "test_user",
  "user_name": "Тестовый пользователь",
  "source": "manual",
  "status": "unread",
  "timestamp": "2025-11-02T17:35:38.486Z",
  "details": null,
  "metadata": null
}
```

Проверить созданное уведомление:
```bash
curl http://q84oskg0cs044ogwkok0os04.91.107.212.137.sslip.io/api/notifications/1
```


