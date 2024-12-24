import asyncio

from database import async_session
import crud 
from database import init_db

async def setup_database():
    await init_db()
    
async def example_usage():
  
    await setup_database()
    
    async with async_session() as session:
        # Добавление или обновление пользователя
        await crud.add_or_update_user(session, user_id="12345", user_name="JohnDoe")

        # Получение времени последнего посещения
        last_active = await crud.get_last_active(session, user_id="12345")
        print(f"Last active: {last_active}")

        # Получение списка всех пользователей
        all_users = await crud.get_all_users(session)
        for user in all_users:
            print(f"User ID: {user[0]}, Name: {user[1]}, Last Active: {user[2]}")

if __name__ == "__main__":
    asyncio.run(example_usage())