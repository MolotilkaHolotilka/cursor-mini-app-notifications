from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from database import get_db
from models import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationFilter,
    NotificationType,
    NotificationStatus
)
from services import NotificationService

router = APIRouter()

@router.get("", response_model=dict)
async def get_notifications(
    type: Optional[NotificationType] = Query(None, description="Фильтр по типу"),
    user_id: Optional[str] = Query(None, description="Фильтр по пользователю"),
    status: Optional[NotificationStatus] = Query(None, description="Фильтр по статусу"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей"),
    offset: int = Query(0, ge=0, description="Смещение"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список уведомлений с фильтрацией и пагинацией
    
    **Параметры:**
    - `type`: Тип уведомления (file_upload, record_create, record_update, record_delete, user_action)
    - `user_id`: ID пользователя
    - `status`: Статус (read, unread)
    - `limit`: Количество записей (1-1000)
    - `offset`: Смещение для пагинации
    """
    filters = NotificationFilter(
        type=type,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset
    )
    
    notifications, total = await NotificationService.get_notifications(db, filters)
    
    return {
        "notifications": [
            NotificationResponse.model_validate(n) for n in notifications
        ],
        "total": total,
        "limit": limit,
        "offset": offset
    }

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить уведомление по ID"""
    notification = await NotificationService.get_notification(db, notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    return NotificationResponse.model_validate(notification)

@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новое уведомление
    
    **Пример запроса:**
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
    """
    notification = await NotificationService.create_notification(db, notification_data)
    return NotificationResponse.model_validate(notification)

@router.patch("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    update_data: NotificationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить уведомление (например, отметить как прочитанное)"""
    notification = await NotificationService.update_notification(
        db, notification_id, update_data
    )
    
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    return NotificationResponse.model_validate(notification)

@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Отметить уведомление как прочитанное"""
    notification = await NotificationService.mark_as_read(db, notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    return NotificationResponse.model_validate(notification)

@router.post("/batch/read", response_model=dict)
async def mark_notifications_read(
    request: dict,
    db: AsyncSession = Depends(get_db)
):
    """Отметить несколько уведомлений как прочитанные"""
    notification_ids = request.get("notification_ids", [])
    updated = []
    not_found = []
    
    for notification_id in notification_ids:
        notification = await NotificationService.mark_as_read(db, notification_id)
        if notification:
            updated.append(notification_id)
        else:
            not_found.append(notification_id)
    
    return {
        "updated": updated,
        "not_found": not_found,
        "total_updated": len(updated)
    }

