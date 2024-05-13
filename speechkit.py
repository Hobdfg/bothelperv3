import requests
from config import IAM_TOKEN, FOLDER_ID


def speech_to_text(data):
    params = "&".join([
        "topic=general",
        f"folderId={FOLDER_ID}",
        "lang=ru-RU"
    ])
    url = f"https://stt.api.clound.yandex.net/speech/v1/stt:recognize?{params}"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    response = requests.post(url=url, headers=headers, data=data)
    decoded_data = response.json
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка"