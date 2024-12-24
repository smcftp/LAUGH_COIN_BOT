import asyncio
import logging
from datetime import datetime, timedelta
import random

from database.database import async_session
import database.crud as crud
from aiogram import Bot

import telegram_bot.prompts as prompts 
import telegram_bot.utils as utils

# Логгирование
logging.basicConfig(level=logging.INFO)

# Функция для отправки сообщений пользователям
async def check_and_notify_users(bot: Bot):
    while True:
        try:
            async with async_session() as session:
                # Получаем всех пользователей из базы данных
                users = await crud.get_all_users(session)

                current_time = datetime.now()

                for user_id, user_name, last_active in users:
                    if last_active:
                        # Вычисляем время отсутствия
                        time_since_last_active = current_time - last_active

                        # Напоминания через экспоненциальные интервалы
                        reminders = [
                            (2, 5),  # Первое напоминание: через 2-5 часов
                            (6, 12),  # Второе напоминание: через 6-12 часов
                            (12, 24),  # Третье напоминание: через 12-24 часов
                        ]

                        # Добавляем экспоненциальное увеличение интервалов
                        for i in range(4, 8):  # Интервалы 24-48, 48-96 и т.д.
                            reminders.append((2**i, 2**(i + 1)))

                        # Определяем, какое напоминание подходит
                        for idx, (min_hours, max_hours) in enumerate(reminders):
                            min_delta = timedelta(hours=min_hours)
                            max_delta = timedelta(hours=max_hours)

                            if min_delta <= time_since_last_active <= max_delta:
                                # Выбираем случайное время внутри интервала
                                random_delay = timedelta(
                                    seconds=random.randint(
                                        int(min_delta.total_seconds()),
                                        int(max_delta.total_seconds())
                                    )
                                )
                                
                                # Если текущее время подходит для напоминания
                                if time_since_last_active >= random_delay:
                                    try:
                                        
                                        prompt = await prompts.gen_prompt_rand_mes()
                                        text = await utils.process_api_response(prompt=prompt)
                                        
                                        await bot.send_message(
                                            chat_id=user_id,
                                            text=text
                                        )
                                        logging.info(f"Напоминание отправлено пользователю: {user_id}")
                                    except Exception as e:
                                        logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

                                # После отправки переходим к следующему пользователю
                                break
                                
        except Exception as e:
            logging.error(f"Ошибка в проверке пользователей: {e}")

        # Ожидаем 1 минуту перед повторной проверкой
        await asyncio.sleep(120)