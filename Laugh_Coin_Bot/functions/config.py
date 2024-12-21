from pydantic_settings import BaseSettings

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

############################################################

# Переменные окружения

class Settings(BaseSettings):
    openai_api_key: str
    telegram_bot_token: str

    class Config:
        env_file = ''

set = Settings()

############################################################

# Настройка телеграмм бота
bot_tg = Bot(token=set.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
