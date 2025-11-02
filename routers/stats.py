from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database import get_db
from models import StatsResponse
from services import NotificationService

router = APIRouter()

@router.get("", response_model=StatsResponse)
async def get_stats(
    user_id: Optional[str] = Query(None, description="Фильтр по пользователю"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику уведомлений
    
    **Возвращает:**
    - `total`: Общее количество уведомлений
    - `unread`: Количество непрочитанных
    - `today`: Количество за сегодня
    - `by_type`: Распределение по типам
    - `by_user`: Топ 10 пользователей по активности
    """
    stats = await NotificationService.get_stats(db, user_id)
    return stats

