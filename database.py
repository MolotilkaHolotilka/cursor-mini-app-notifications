from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text, Enum as SQLEnum
from datetime import datetime
from models import NotificationType, NotificationStatus

Base = declarative_base()

# SQLite база данных (для продакшена можно заменить на PostgreSQL)
DATABASE_URL = "sqlite+aiosqlite:///./notifications.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Notification(Base):
    """Модель уведомления в БД"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    source = Column(String(50), default="airtable")
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.UNREAD, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    details = Column(JSON, nullable=True)
    event_metadata = Column("metadata", JSON, nullable=True)  # metadata - зарезервированное слово в SQLAlchemy
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, user={self.user_name})>"

async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

