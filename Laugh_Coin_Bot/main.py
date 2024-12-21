import asyncio
import logging
from telegram_bot.handlers import register_handlers, dp

import functions.config as config

async def main() -> None:
    try:
        # Запуск Telegram-бота
        register_handlers(dp)
        await dp.start_polling(config.bot_tg)
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")

if __name__ == "__main__":
    asyncio.run(main())
