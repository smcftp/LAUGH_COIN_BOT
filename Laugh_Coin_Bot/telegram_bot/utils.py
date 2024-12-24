from openai import AsyncOpenAI
import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Импорт ключа
from functions.config import set, cryptocurrencies, our_coin

from functions.classification import classify_text_async, classify_function_calling

import telegram_bot.prompts as prompts

# Создаем клиента OpenAI
client = AsyncOpenAI(
    api_key=set.openai_api_key
)

# Функция для генерации вдохновляющего сообщения о курсе криптовалюты
async def generate_crypto_message(state: str, coin_name: str) -> str:

    # Промпт, написания прогноаз
    
    
    # Отправляем запрос в OpenAI API для генерации сообщения
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
              "role": "system", 
              "content": "Ты — позитивный и вдохновлячющий блогер."
            },
            {
              "role": "user", 
              "content": prompt
            }
        ],
    )

    # Возвращаем сгенерированный текст
    return str(completion.choices[0].message.content)


async def process_api_response(prompt: str) -> str:
    
    # Отправляем запрос в OpenAI API для генерации сообщения
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
              "role": "system", 
              "content": "Ты — позитивный и вдохновлячющий блогер."
            },
            {
              "role": "user", 
              "content": prompt
            }
        ],
    )
    
    return str(completion.choices[0].message.content) 


async def dialogue_process(input_message: str, username: str) -> str:
    
    fun_name, coin = await classify_function_calling(sequence_to_classify=input_message)
    
    if fun_name == "handle_greeting":
        
        prompt = await prompts.gen_prompt_handle_greeting(name=username)
        greeting_answer = await process_api_response(prompt=prompt)
        return greeting_answer
    
    elif fun_name == "explain_bot_capabilities":
        
        prompt = await prompts.gen_prompt_bot_capabilities(name=username)
        bot_capabilities_answer = await process_api_response(prompt=prompt)
        return bot_capabilities_answer
        
    elif fun_name == "generate_crypto_forecast":
        
        # Проверка на None
        if coin is not None:
            # Проверяем значение coin
            # Функция совпадения
            
            cryptocurrencies_add = cryptocurrencies
            
            # Программно добавляем категорию "другие"
            if "Другие" not in cryptocurrencies_add:
                cryptocurrencies_add.append("Другие")
            
            find_coin = await classify_text_async(sequence_to_classify=coin, candidate_labels=cryptocurrencies_add)
            print("find_coin=", find_coin)
            
            # Если find_coin нету в базе данных коинов
            if find_coin == "Другие":
                return "Not found in database"
            
            if find_coin in cryptocurrencies and find_coin != our_coin:
                state = random.choice(["понижение", "повышение"])
                
                # Получение данных от api о цене coin
                
                prompt = await prompts.gen_prompt_crypto_forecast(state=state, coin_name=coin, name=username)
                crypto_forecast_answer = await process_api_response(prompt=prompt)
                return crypto_forecast_answer
                
            elif find_coin == our_coin:
                state = "повышение"
                
                # Получение данных от api о цене coin

                
                prompt = await prompts.gen_prompt_main_crypto_forecast(coin_name=coin, name=username)
                crypto_forecast_answer = await process_api_response(prompt=prompt)
                return crypto_forecast_answer
                
            else:
                # Коин не найден в базу данных
                return "Not found in database"
        else:
            print("Переменная coin равна None.")
    
    elif fun_name == "handle_negative_message":
        
        prompt = await prompts.gen_prompt_negative_message(name=username)
        bot_capabilities_answer = await process_api_response(prompt=prompt)
        return bot_capabilities_answer
    
    elif fun_name == "handle_undefined_message":
        
        base_message = "На данный момент мой функционал ограничен. 😊 Но разработчики уже трудятся над обновлением! 🚀✨ А пока улыбнитесь — это поднимает настроение 😄 и тренирует мышцы лица! 💪😊🌟"
                
        prompt = await prompts.gen_prompt_paraphrased_message(name=username, base_message=base_message)
        text = await process_api_response(prompt=prompt)
        return text
        
    else:
        
        base_message = "На данный момент мой функционал ограничен. 😊 Но разработчики уже трудятся над обновлением! 🚀✨ А пока улыбнитесь — это поднимает настроение 😄 и тренирует мышцы лица! 💪😊🌟"
                
        prompt = await prompts.gen_prompt_paraphrased_message(name=username, base_message=base_message)
        text = await process_api_response(prompt=prompt)
        return text
    
