from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)  # Уникальный идентификатор пользователя
    user_name = Column(String, nullable=False)  # Имя пользователя
    last_active = Column(DateTime, default=func.now(), onupdate=func.now())  # Последняя активность пользователя
