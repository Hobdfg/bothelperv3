import requests
import logging
from config import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, IAM_TOKEN, FOLDER_ID

logging.Basic(filename=LOGS, level=logging.ERROR, format="%(asctime)s %(message)s", filemode="w")

def ask_gpt(message):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content_Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": [
            {
                'role': 'user',
                'text': messages
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус код: {response.status_code}", None
        answer = response.json()['result']['alternative'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращение к GPT", None