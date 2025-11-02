from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    """Типы уведомлений"""
    FILE_UPLOAD = "file_upload"
    RECORD_CREATE = "record_create"
    RECORD_UPDATE = "record_update"
    RECORD_DELETE = "record_delete"
    USER_ACTION = "user_action"

class NotificationStatus(str, Enum):
    """Статусы уведомлений"""
    UNREAD = "unread"
    READ = "read"

# Request models
class NotificationCreate(BaseModel):
    """Модель для создания уведомления"""
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(..., description="ID пользователя/менеджера")
    user_name: str = Field(..., min_length=1, max_length=100)
    source: str = Field(default="airtable", description="Источник события")
    details: Optional[dict] = Field(default=None, description="Дополнительные детали")
    event_metadata: Optional[dict] = Field(default=None, alias="metadata", description="Метаданные события")
    
    class Config:
        populate_by_name = True  # Позволяет использовать как alias, так и имя поля
        extra = "ignore"  # Игнорировать лишние поля (id, status, timestamp)

class NotificationUpdate(BaseModel):
    """Модель для обновления уведомления"""
    read: Optional[bool] = None

class NotificationFilter(BaseModel):
    """Модель для фильтрации уведомлений"""
    type: Optional[NotificationType] = None
    user_id: Optional[str] = None
    status: Optional[NotificationStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: Optional[int] = Field(default=100, ge=1, le=1000)
    offset: Optional[int] = Field(default=0, ge=0)

# Response models
class NotificationResponse(BaseModel):
    """Ответ с уведомлением"""
    id: int
    type: NotificationType
    title: str
    description: str
    user_id: str
    user_name: str
    source: str
    status: NotificationStatus
    timestamp: datetime
    details: Optional[dict] = None
    metadata: Optional[dict] = Field(default=None, alias="event_metadata", serialization_alias="metadata")
    
    model_config = {"from_attributes": True, "populate_by_name": True}

class NotificationListResponse(BaseModel):
    """Ответ со списком уведомлений"""
    notifications: List[NotificationResponse]
    total: int
    limit: int
    offset: int

class StatsResponse(BaseModel):
    """Статистика уведомлений"""
    total: int
    unread: int
    today: int
    by_type: dict
    by_user: dict

# Webhook models
class AirtableWebhookPayload(BaseModel):
    """Payload от Airtable webhook"""
    base_id: str
    webhook_id: str
    event: str  # record.created, record.updated, attachment.created, etc.
    timestamp: datetime
    payload: dict

class AirtableEventData(BaseModel):
    """Данные события из Airtable"""
    base_id: str
    table_id: str
    record_id: Optional[str] = None
    action: str  # created, updated, deleted, attachment_added
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    fields: Optional[dict] = None
    attachment_url: Optional[str] = None

