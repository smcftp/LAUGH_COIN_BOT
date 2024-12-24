from pydantic_settings import BaseSettings

from openai import OpenAI

import platform
import struct
import ctypes

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from telethon import TelegramClient, events

from openai import OpenAI

############################################################

# Переменные окружения

class Settings(BaseSettings):
    openai_api_key: str
    telegram_bot_token: str

    class Config:
        env_file = 'D:\\Programming\\Python\\GPT\\Laugh_Coin_Bot\\.env'

set = Settings()

############################################################

# Настройка телеграмм бота
bot_tg = Bot(token=set.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

############################################################

# Список криптовалют и их прогнозов
cryptocurrencies = [
    'Bitcoin', 'MemCoin', 'Ripple', 'Ethereum', 'Litecoin'
]

our_coin = "MemCoin"
