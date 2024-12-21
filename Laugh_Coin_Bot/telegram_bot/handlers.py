import logging
import random
from aiogram import Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from functions.config import dp
from telegram_bot.utils import generate_crypto_message

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем состояния
class Form(StatesGroup):
    waiting_for_response = State()

# Список криптовалют и их прогнозов
cryptocurrencies = [
    '🚀 Bitcoin', '💎 MemCoin', '🌊 Ripple', '🌕 Ethereum', '💫 Litecoin'
]

# Стартовая команда
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        await message.answer(f"Приветствую тебя {message.from_user.first_name}! 😊")

        # Создаем клавиатуру с кнопками
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='🚀 Bitcoin'), KeyboardButton(text='💎 MemCoin')],  # Первый ряд из 2 кнопок
                [KeyboardButton(text='🌊 Ripple'), KeyboardButton(text='🌕 Ethereum')],  # Второй ряд из 2 кнопок
                [KeyboardButton(text='💫 Litecoin')]  # Третий ряд с одной кнопкой
            ],
            resize_keyboard=True  # Опция для уменьшения размера кнопок
        )
        
        text = """
        Сегодня чудесный день, чтобы взглянуть на мир с надеждой и радостью, а также на прогнозы цифровых активов! 🌞\nВыбери свою монету для прогноза, друг мой, и пусть этот выбор станет вдохновением на весь день! 😊🌟
        """

        # Отправляем сообщение с клавиатурой
        await message.answer(text=text, reply_markup=keyboard)
        await state.set_state(Form.waiting_for_response)

    except Exception as e:
        logger.error(f"Ошибка в обработчике команды /start: {e}")
        await message.answer("Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊")


# Обработка текстовых сообщений (выбор криптовалюты)
@dp.message(F.text)
async def handle_text_message(message: Message, state: FSMContext) -> None:
    try:
        selected_crypto = message.text
        print("selected_crypto = ", selected_crypto)

        # Если выбранная криптовалюта есть в списке
        if selected_crypto in cryptocurrencies:
            if selected_crypto == "💎 MemCoin":
                # Позитивный прогноз для MemCoin
                state = "повышение"
                
                # Генерация потсоянно положительного ответа
                response = await generate_crypto_message(state=state, coin_name=selected_crypto)
            else:
                # Рандобно направление
                state = random.choice(["понижение", "повышение"])
                
                # Генерация рандомного для других криптовалют
                response = await generate_crypto_message(state=state, coin_name=selected_crypto)
                
            await message.answer(response)  # Отправляем прогноз пользователю
        else:
            # Если текст не соответствует кнопкам
            await message.answer("🌟 Пожалуйста, выберите вашу любимую криптовалюту, нажав на кнопку ниже — и улыбнитесь себе и миру вокруг! 😊🚀")
    
    except Exception as e:
        logger.error(f"Ошибка в обработке текстового сообщения: {e}")
        await message.answer("Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊")


# Обработчик для неизвестных ошибок
@dp.errors()
async def global_error_handler(update: types.Update, exception: Exception) -> None:
    logger.error(f"Необработанная ошибка: {exception}")
    if update.message:
        await update.message.answer("Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊")
    return True  # Возвращаем True, чтобы продолжить обработку других обновлений


# Регистрация обработчиков
def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(handle_text_message, F.text)
