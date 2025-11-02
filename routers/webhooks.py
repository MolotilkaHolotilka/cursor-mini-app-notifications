from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json

from database import get_db
from models import AirtableWebhookPayload
from services import AirtableService, NotificationService

router = APIRouter()

@router.post("/airtable")
async def airtable_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Webhook для приема событий из Airtable
    
    **Настройка webhook в Airtable:**
    1. Перейти в настройки базы данных
    2. Выбрать "Automations" -> "Webhooks"
    3. Создать новый webhook
    4. Указать URL: https://your-domain.com/api/webhooks/airtable
    5. Выбрать события: record.created, record.updated, attachment.created
    
    **Формат payload от Airtable:**
    ```json
    {
        "base": {
            "id": "base_id"
        },
        "webhook": {
            "id": "webhook_id"
        },
        "event": "record.created",
        "timestamp": "2024-01-01T00:00:00.000Z",
        "payload": {
            "base": {...},
            "tables": [...],
            "eventMetadata": {
                "source": "airtable",
                "sourceMetadata": {
                    "user": {
                        "id": "user_id",
                        "email": "user@example.com"
                    }
                }
            }
        }
    }
    ```
    """
    try:
        # Получаем данные из запроса
        body = await request.json()
        
        # Парсим событие Airtable
        event_type = body.get("event", "")
        base_id = body.get("base", {}).get("id", "")
        payload = body.get("payload", {})
        
        # Определяем тип действия
        action = "unknown"
        if "record.created" in event_type:
            action = "created"
        elif "record.updated" in event_type:
            action = "updated"
        elif "record.deleted" in event_type:
            action = "deleted"
        elif "attachment" in event_type.lower():
            action = "attachment_added"
        
        # Извлекаем информацию о пользователе
        user_info = payload.get("eventMetadata", {}).get("sourceMetadata", {}).get("user", {})
        user_id = user_info.get("id", "unknown")
        user_email = user_info.get("email", "unknown@example.com")
        user_name = user_info.get("name", user_email.split("@")[0])
        
        # Извлекаем информацию о таблице и записи
        tables = payload.get("tables", [])
        if not tables:
            raise HTTPException(status_code=400, detail="Нет данных о таблицах")
        
        table_data = tables[0]  # Берем первую таблицу
        table_id = table_data.get("id", "")
        table_name = table_data.get("name", "Unknown Table")
        
        records = table_data.get("records", [])
        record_data = records[0] if records else {}
        record_id = record_data.get("id", "")
        fields = record_data.get("fields", {})
        
        # Проверяем наличие вложений
        attachment_url = None
        for field_name, field_value in fields.items():
            if isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, dict) and "url" in item:
                        attachment_url = item["url"]
                        break
        
        # Формируем данные события
        event_data = {
            "action": action,
            "base_id": base_id,
            "table_id": table_id,
            "table_name": table_name,
            "record_id": record_id,
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "fields": fields,
            "attachment_url": attachment_url
        }
        
        # Создаем уведомление
        notification = await AirtableService.process_airtable_event(db, event_data)
        
        return {
            "status": "success",
            "notification_id": notification.id,
            "message": "Уведомление создано"
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Невалидный JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки webhook: {str(e)}")

@router.get("/airtable/test")
async def test_airtable_webhook(db: AsyncSession = Depends(get_db)):
    """Тестовый эндпоинт для создания уведомления (для разработки)"""
    test_event = {
        "action": "file_upload",
        "base_id": "test_base",
        "table_id": "test_table",
        "table_name": "Тестовая таблица",
        "user_id": "test_user",
        "user_name": "Тестовый пользователь",
        "fields": {"Name": "Тестовая запись"},
        "attachment_url": "https://example.com/test_file.xlsx"
    }
    
    notification = await AirtableService.process_airtable_event(db, test_event)
    
    return {
        "status": "success",
        "notification": {
            "id": notification.id,
            "title": notification.title,
            "description": notification.description,
            "type": notification.type.value,
            "user_name": notification.user_name
        }
    }

