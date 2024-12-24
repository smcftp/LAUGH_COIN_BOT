from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from database.models import User

from datetime import datetime

# Добавление нового пользователя или обновление времени последнего посещения
async def add_or_update_user(session: AsyncSession, user_id: str, user_name: str):
    try:
        # Проверяем, существует ли пользователь
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

        if user:
          
            print("Updating user:", user_id, user_name)
            # Если пользователь существует, обновляем его имя и время активности
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(user_name=user_name, last_active=datetime.now())  # Устанавливаем текущее время
            )
            await session.commit()
        else:
            # Если пользователь не существует, создаем нового
            user = User(user_id=user_id, user_name=user_name)
            session.add(user)

        await session.commit()
        return user
    except Exception as e:
        print(f"Ошибка при добавлении или обновлении пользователя: {e}")
        return None

# Получение времени последнего посещения пользователя по user_id
async def get_last_active(session: AsyncSession, user_id: str):
    try:
        result = await session.execute(select(User.last_active).where(User.user_id == user_id))
        last_active = result.scalar()
        return last_active
    except Exception as e:
        print(f"Ошибка при получении времени последнего посещения: {e}")
        return None

# Получение списка всех пользователей с их полями
async def get_all_users(session: AsyncSession):
    try:
        result = await session.execute(select(User.user_id, User.user_name, User.last_active))
        users = result.all()  # Возвращаем список кортежей (user_id, user_name, last_active)
        return users
    except Exception as e:
        print(f"Ошибка при получении списка всех пользователей: {e}")
        return []
