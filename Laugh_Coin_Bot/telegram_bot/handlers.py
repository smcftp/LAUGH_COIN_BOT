import logging
import random
from aiogram import Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from functions.config import dp, bot_tg, cryptocurrencies
from telegram_bot.utils import dialogue_process, process_api_response
import telegram_bot.prompts as prompts

from database.database import async_session
import database.crud as crud

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем состояния
class Form(StatesGroup):
    waiting_for_response = State()

# Стартовая команда
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        
        chat_id = message.chat.id
        username = message.from_user.first_name
        
        async with async_session() as session:
            # Добавление или обновление пользователя
            await crud.add_or_update_user(session, user_id=chat_id, user_name=username)
        
        await message.answer(f"Приветствую тебя {message.from_user.first_name}! 😊")

        # Создаем клавиатуру с кнопками
        # keyboard = ReplyKeyboardMarkup(
        #     keyboard=[
        #         [KeyboardButton(text='🚀 Bitcoin'), KeyboardButton(text='💎 MemCoin')],  # Первый ряд из 2 кнопок
        #         [KeyboardButton(text='🌊 Ripple'), KeyboardButton(text='🌕 Ethereum')],  # Второй ряд из 2 кнопок
        #         [KeyboardButton(text='💫 Litecoin')]  # Третий ряд с одной кнопкой
        #     ],
        #     resize_keyboard=True  # Опция для уменьшения размера кнопок
        # )
        
        text = """
        Сегодня чудесный день, чтобы взглянуть на мир с надеждой и радостью, а также на прогнозы цифровых активов! 🌞\nВыбери свою монету для прогноза, друг мой, и пусть этот выбор станет вдохновением на весь день! 😊🌟
        """

        # Отправляем сообщение с клавиатурой
        # await message.answer(text=text, reply_markup=keyboard)
        await state.set_state(Form.waiting_for_response)

    except Exception as e:
        logger.error(f"Ошибка в обработчике команды /start: {e}")
        await message.answer("Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊")


# Обработка текстовых сообщений (выбор криптовалюты)
@dp.message(F.text)
async def handle_text_message(message: Message, state: FSMContext) -> None:
    try:
        chat_id = message.chat.id
        selected_crypto = message.text
        username = message.from_user.first_name
        print("selected_crypto = ", selected_crypto)
        
        # Удаляем клавиатуру после нажатия кнопки
        # await message.answer(text="Анализ...⌛",reply_markup=ReplyKeyboardRemove())
        sent_message = await bot_tg.send_message(chat_id=chat_id, text="Анализ...⌛", reply_markup=ReplyKeyboardRemove())
        
        async with async_session() as session:
            # Добавление или обновление пользователя
            await crud.add_or_update_user(session, user_id=str(chat_id), user_name=str(username))

        
        # Если выбранная криптовалюта есть в списке
        if selected_crypto in cryptocurrencies:
            if selected_crypto == "💎 MemCoin":
                # Позитивный прогноз для MemCoin
                state = "повышение"
                
                # Генерация потсоянно положительного ответа
                prompt = await prompts.gen_prompt_main_crypto_forecast(coin_name=selected_crypto, name=username)
                response = await process_api_response(prompt=prompt)
            else:
                # Рандобно направление
                state = random.choice(["понижение", "повышение"])
                
                # Генерация рандомного для других криптовалют
                prompt = await prompts.gen_prompt_crypto_forecast(state=state, coin_name=selected_crypto, name=username)
                response = await process_api_response(prompt=prompt)
               
            await bot_tg.delete_message(chat_id=chat_id, message_id=sent_message.message_id) 
            await message.answer(response)  # Отправляем прогноз пользователю
        else:
            
            result = await dialogue_process(input_message=message.text, username=username)
            await bot_tg.delete_message(chat_id=chat_id, message_id=sent_message.message_id) 

            if result == "Not found in database":
                
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text='🚀 Bitcoin'), KeyboardButton(text='💎 MemCoin')],  # Первый ряд из 2 кнопок
                        [KeyboardButton(text='🌊 Ripple'), KeyboardButton(text='🌕 Ethereum')],  # Второй ряд из 2 кнопок
                        [KeyboardButton(text='💫 Litecoin')]  # Третий ряд с одной кнопкой
                    ],
                    resize_keyboard=True  # Опция для уменьшения размера кнопок
                )
                
                base_message = "Я пока не знаю этого мемкоина, но скоро меня обновят, и я стану умнее! 🌟 Пожалуйста, выберите вашу любимую криптовалюту, нажав на кнопку ниже — и улыбнитесь себе и миру вокруг! 😊🚀"
                
                prompt = await prompts.gen_prompt_paraphrased_message(name=username, base_message=base_message)
                text = await process_api_response(prompt=prompt)

                await message.answer(
                    text=text,
                    reply_markup=keyboard  # Создаем клавиатуру к нопками
                )
                return
            
            await message.answer(result)            
            
    except Exception as e:
        logger.error(f"Ошибка в обработке текстового сообщения: {e}")
        await bot_tg.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
        
        base_message = "Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊"
                
        prompt = await prompts.gen_prompt_paraphrased_message(name=username, base_message=base_message)
        text = await process_api_response(prompt=prompt)
        
        await message.answer(text=text)


# Обработчик для неизвестных ошибок
@dp.errors()
async def global_error_handler(update: types.Update, exception: Exception) -> None:
    logger.error(f"Необработанная ошибка: {exception}")
    if update.message:
        
        username = update.message.from_user.first_name
        
        base_message = "Друзья, не беда! 😊❌ Произошла небольшая ошибка. Попробуйте снова чуть позже — всё получится! 🌟 Улыбайтесь, ведь впереди только лучшее! 😊"
                
        prompt = prompts.gen_prompt_paraphrased_message(name=username, base_message=base_message)
        text = await process_api_response(prompt=prompt)
        
        await update.message.answer(text=text)
    return True  # Возвращаем True, чтобы продолжить обработку других обновлений


@dp.message(F.text & F.chat.type.in_({"group", "supergroup"}))
async def handle_group_message(message: Message):
    
    bot_username = "example_bot"
    
    if f"@{bot_username}" in message.text:
        await message.reply("Привет! Чем я могу помочь?")


# Регистрация обработчиков
def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(handle_text_message, F.text)
