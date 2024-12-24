import asyncio
import logging
from telegram_bot.handlers import register_handlers, dp

import functions.config as config

from telegram_bot.send_rand_mes import check_and_notify_users
    
async def main() -> None:
    try:
        # Регистрация обработчиков
        register_handlers(dp)
        
        # Запускаем задачу для проверки и уведомления пользователей
        asyncio.create_task(check_and_notify_users(config.bot_tg))
        
        # Запуск Telegram-бота
        await dp.start_polling(config.bot_tg)
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")

if __name__ == "__main__":
    asyncio.run(main())
