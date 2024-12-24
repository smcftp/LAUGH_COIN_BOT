from openai import AsyncOpenAI
import json

# Импорт ключа
from functions.config import set

# Создаем клиента OpenAI
client = AsyncOpenAI(
    api_key=set.openai_api_key
)

async def classify_text_async(sequence_to_classify: str, candidate_labels: list[str]) -> str:
    """
    Асинхронно классифицирует текст в одну из заданных категорий с использованием OpenAI.

    Args:
        sequence_to_classify (str): Текст для классификации.
        candidate_labels (list): Список категорий для классификации.
        client: Асинхронный экземпляр OpenAI клиента.

    Returns:
        str: Категория, к которой относится текст, или сообщение об ошибке.
    """
    # Определение инструмента для функции классификации
    tools = [
        {
            "type": "function",
            "function": {
                "name": "classify_text",
                "description": "Classify the input text into predefined categories.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "The category the input text belongs to.",
                        }
                    },
                    "required": ["category"],
                    "additionalProperties": False,
                },
            }
        }
    ]

    # Формируем промпт для модели
    prompt = (
        f"Classify the following text: '{sequence_to_classify}' into one of the following categories: "
        f"{', '.join(candidate_labels)}. "
        "Respond with the category that best describes the text."
    )

    try:
        model = "gpt-3.5-turbo"
        # model="gpt-4o-mini"
        
        # Создаём асинхронный запрос к OpenAI
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a text classifier."},
                {"role": "user", "content": prompt}
            ],
            tools=tools,
        )

        # Получаем категорию из результатов вызова функции
        category = str(json.loads(completion.choices[0].message.tool_calls[0].function.arguments)["category"])
        return category
    except (KeyError, ValueError, TypeError) as e:
        return f"Ошибка при анализе результата: {e}"
    except Exception as e:
        return f"Общая ошибка: {e}"


async def classify_function_calling(sequence_to_classify: str) -> str:
    """
    Асинхронно классифицирует текст в одну из заданных категорий с использованием OpenAI.

    Args:
        sequence_to_classify (str): Текст для классификации.
        candidate_labels (list): Список категорий для классификации.
        client: Асинхронный экземпляр OpenAI клиента.

    Returns:
        str: Категория, к которой относится текст, или сообщение об ошибке.
    """
    # Определение инструмента для функции классификации
    tools = [
        {
            "type": "function",
            "function": {
                "name": "handle_greeting",
                "description": "Any handle a greeting message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The greeting message from the user.",
                        },
                    },
                    "required": ["message"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "explain_bot_capabilities",
                "description": "Provide information about the bot's capabilities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query about the bot's functionality.",
                        },
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "generate_crypto_forecast",
                "description": "Generate a forecast for a specific cryptocurrency.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cryptocurrency": {
                            "type": "string",
                            "description": "The name of the cryptocurrency for the forecast.",
                        },
                        "trend": {
                            "type": "string",
                            "enum": ["повышение", "понижение"],
                            "description": "The trend of the cryptocurrency price (e.g., 'повышение' or 'понижение').",
                        },
                    },
                    "required": ["cryptocurrency", "trend"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "handle_negative_message",
                "description": "Respond to a negative or offensive message from the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The negative or offensive message from the user.",
                        },
                    },
                    "required": ["message"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "handle_undefined_message",
                "description": "Handle a message that does not fit into any predefined category.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The undefined message from the user.",
                        },
                    },
                    "required": ["message"],
                    "additionalProperties": False,
                },
            },
        },
    ]

    # Формируем промпт для модели
    prompt = sequence_to_classify

    try:
        model = "gpt-3.5-turbo"
        # model="gpt-4o-mini"
        
        # Создаём асинхронный запрос к OpenAI
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a text classifier."},
                {"role": "user", "content": prompt}
            ],
            tools=tools,
        )

        res_fun_cal = completion.choices[0].message.tool_calls
        print("res_fun_cal =", res_fun_cal)
        
        if res_fun_cal != None:

            # Обработка каждого элемента списка
            for item in res_fun_cal:
                if hasattr(item.function, 'name') and hasattr(item.function, 'arguments'):
                    # Достаём имя функции
                    function_name = item.function.name
                    
                    # Парсим аргументы функции
                    function_arguments = json.loads(item.function.arguments)
                    
                    # Извлекаем конкретные значения
                    cryptocurrency = function_arguments.get("cryptocurrency")
                    trend = function_arguments.get("trend")
                    
                    # Выводим информацию
                    print(f"Function name: {function_name}")
                    print(f"Cryptocurrency: {cryptocurrency}")
                    # print(f"Trend: {trend}")
        
            return function_name, cryptocurrency
        
        else:
            
            return None, None
      
    except (KeyError, ValueError, TypeError) as e:
        return f"Ошибка при анализе результата: {e}"
    except Exception as e:
        return f"Общая ошибка: {e}"