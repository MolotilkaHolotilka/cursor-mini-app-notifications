from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
from models import (
    NotificationCreate, 
    NotificationUpdate, 
    NotificationResponse,
    NotificationFilter,
    NotificationType,
    NotificationStatus,
    StatsResponse
)
from database import Notification

class NotificationService:
    """Сервис для работы с уведомлениями"""
    
    @staticmethod
    async def create_notification(
        db: AsyncSession,
        notification_data: NotificationCreate
    ) -> Notification:
        """Создать новое уведомление"""
        notification = Notification(
            type=notification_data.type,
            title=notification_data.title,
            description=notification_data.description,
            user_id=notification_data.user_id,
            user_name=notification_data.user_name,
            source=notification_data.source,
            details=notification_data.details,
            event_metadata=notification_data.event_metadata,
            status=NotificationStatus.UNREAD,
            timestamp=datetime.utcnow()
        )
        
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification
    
    @staticmethod
    async def get_notifications(
        db: AsyncSession,
        filters: NotificationFilter
    ) -> tuple[List[Notification], int]:
        """Получить список уведомлений с фильтрацией"""
        query = select(Notification)
        count_query = select(func.count(Notification.id))
        
        # Применяем фильтры
        conditions = []
        
        if filters.type:
            conditions.append(Notification.type == filters.type)
        
        if filters.user_id:
            conditions.append(Notification.user_id == filters.user_id)
        
        if filters.status:
            conditions.append(Notification.status == filters.status)
        
        if filters.start_date:
            conditions.append(Notification.timestamp >= filters.start_date)
        
        if filters.end_date:
            conditions.append(Notification.timestamp <= filters.end_date)
        
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))
        
        # Сортировка по времени (новые сначала)
        query = query.order_by(Notification.timestamp.desc())
        
        # Пагинация
        query = query.offset(filters.offset).limit(filters.limit)
        
        # Выполняем запросы
        result = await db.execute(query)
        notifications = result.scalars().all()
        
        count_result = await db.execute(count_query)
        total = count_result.scalar()
        
        return notifications, total
    
    @staticmethod
    async def get_notification(
        db: AsyncSession,
        notification_id: int
    ) -> Optional[Notification]:
        """Получить уведомление по ID"""
        result = await db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_notification(
        db: AsyncSession,
        notification_id: int,
        update_data: NotificationUpdate
    ) -> Optional[Notification]:
        """Обновить уведомление"""
        notification = await NotificationService.get_notification(db, notification_id)
        
        if not notification:
            return None
        
        if update_data.read is not None:
            notification.status = (
                NotificationStatus.READ if update_data.read 
                else NotificationStatus.UNREAD
            )
        
        await db.commit()
        await db.refresh(notification)
        return notification
    
    @staticmethod
    async def mark_as_read(
        db: AsyncSession,
        notification_id: int
    ) -> Optional[Notification]:
        """Отметить уведомление как прочитанное"""
        return await NotificationService.update_notification(
            db,
            notification_id,
            NotificationUpdate(read=True)
        )
    
    @staticmethod
    async def get_stats(
        db: AsyncSession,
        user_id: Optional[str] = None
    ) -> StatsResponse:
        """Получить статистику уведомлений"""
        # Общее количество
        total_query = select(func.count(Notification.id))
        if user_id:
            total_query = total_query.where(Notification.user_id == user_id)
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Непрочитанные
        unread_query = select(func.count(Notification.id)).where(
            Notification.status == NotificationStatus.UNREAD
        )
        if user_id:
            unread_query = unread_query.where(Notification.user_id == user_id)
        unread_result = await db.execute(unread_query)
        unread = unread_result.scalar() or 0
        
        # Сегодня
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_query = select(func.count(Notification.id)).where(
            Notification.timestamp >= today_start
        )
        if user_id:
            today_query = today_query.where(Notification.user_id == user_id)
        today_result = await db.execute(today_query)
        today = today_result.scalar() or 0
        
        # По типам
        type_query = select(
            Notification.type,
            func.count(Notification.id).label('count')
        )
        if user_id:
            type_query = type_query.where(Notification.user_id == user_id)
        type_query = type_query.group_by(Notification.type)
        type_result = await db.execute(type_query)
        by_type = {row[0].value: row[1] for row in type_result.fetchall()}
        
        # По пользователям (топ 10)
        user_query = select(
            Notification.user_id,
            Notification.user_name,
            func.count(Notification.id).label('count')
        )
        if user_id:
            user_query = user_query.where(Notification.user_id == user_id)
        user_query = user_query.group_by(Notification.user_id, Notification.user_name)
        user_query = user_query.order_by(func.count(Notification.id).desc())
        user_query = user_query.limit(10)
        user_result = await db.execute(user_query)
        by_user = {
            row[1]: row[2] for row in user_result.fetchall()
        }
        
        return StatsResponse(
            total=total,
            unread=unread,
            today=today,
            by_type=by_type,
            by_user=by_user
        )

class AirtableService:
    """Сервис для обработки событий из Airtable"""
    
    @staticmethod
    async def process_airtable_event(
        db: AsyncSession,
        event_data: dict
    ) -> Notification:
        """Обработать событие из Airtable и создать уведомление"""
        
        # Парсим данные события
        action = event_data.get("action", "unknown")
        base_id = event_data.get("base_id", "unknown")
        table_id = event_data.get("table_id", "unknown")
        user_id = event_data.get("user_id", "unknown")
        user_name = event_data.get("user_name", "Неизвестный пользователь")
        fields = event_data.get("fields", {})
        attachment_url = event_data.get("attachment_url")
        
        # Определяем тип уведомления
        notification_type = NotificationType.USER_ACTION
        title = ""
        description = ""
        details = {
            "base_id": base_id,
            "table_id": table_id,
            "table_name": event_data.get("table_name", "Unknown")
        }
        
        if action == "attachment_added" or attachment_url:
            notification_type = NotificationType.FILE_UPLOAD
            title = "Загрузка файла"
            file_name = attachment_url.split("/")[-1] if attachment_url else "файл"
            description = f'Загружен файл "{file_name}" в таблицу "{details["table_name"]}"'
            details["attachment_url"] = attachment_url
            details["file_type"] = file_name.split(".")[-1].upper() if "." in file_name else "UNKNOWN"
        
        elif action == "created":
            notification_type = NotificationType.RECORD_CREATE
            title = "Создание записи"
            record_name = fields.get("Name") or fields.get("title") or "Новая запись"
            description = f'Создана запись "{record_name}" в таблице "{details["table_name"]}"'
            details["record_id"] = event_data.get("record_id")
        
        elif action == "updated":
            notification_type = NotificationType.RECORD_UPDATE
            title = "Обновление записи"
            record_name = fields.get("Name") or fields.get("title") or "Запись"
            description = f'Обновлена запись "{record_name}" в таблице "{details["table_name"]}"'
            details["record_id"] = event_data.get("record_id")
        
        elif action == "deleted":
            notification_type = NotificationType.RECORD_DELETE
            title = "Удаление записи"
            description = f'Удалена запись из таблицы "{details["table_name"]}"'
        
        # Создаем уведомление
        notification_data = NotificationCreate(
            type=notification_type,
            title=title,
            description=description,
            user_id=user_id,
            user_name=user_name,
            source="airtable",
            details=details,
            event_metadata=event_data
        )
        
        return await NotificationService.create_notification(db, notification_data)

