import telebot
from speechkit import speech_to_text, text_to_speech
from yandex import ask_gpt
from config import TOKEN, max_tts_symbols, max_user_tts_symbols
from db import count_all_symbol, insert_row
MAX_USER_TTS_SYMBOLS = max_user_tts_symbols
MAX_TTS_SYMBOLS = max_tts_symbols

bot = telebot.TeleBot(TOKEN)

users = {}


@bot.message.handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    bot.send_message(message.from_user.id,"Привет! Я могу сгенерировать пост для соцсетей по словестному описанию.")


@bot.message_handler(commands=['debug'])
def log_errors(message):
    debug = True
    chat_id = message.chat.id
    error_message = "Произошла ошибка с API GPT"
    bot.send_message(chat_id, error_message)

@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщеним текст, чтобы я его озвучил!')
    bot.register_next_stap_handler(message, tts)

def tts(message):
    user_id = message.from_user.id
    text = message.text

    # Проверка, что сообщение действительно текстовое
    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return

        # Считаем символы в тексте и проверяем сумму потраченных символов
    text_symbol = is_tts_symbol_limit(message, text)
    if text_symbol is None:
        return

    # Записываем сообщение и кол-во символов в БД
    insert_row(user_id, text, text_symbol)

    # Получаем статус и содержимое ответа от SpeechKit
    status, content = text_to_speech(text)

    # Если статус True - отправляем голосовое сообщение, иначе - сообщение об ошибке
    if status:
        bot.send_voice(user_id, content)
    else:
        bot.send_message(user_id, content)

def is_tts_symbol_limit(message, text):
    user_id = message.from_user.id
    text_symbols = len(text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = count_all_symbol(user_id) + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        bot.send_message(user_id, msg)
        return None

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит SpeechKit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(text)


@bot.message.handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id] == 5:
            bot.send_message(user_id, "Вы уже сделали 5 запросов")
            return
    else:
        users[user_id] = 0

    if message.voice.duration > 15:
        bot.send_message(user_id, "Сообщение не должно быть дольше 15 секунд")
        return

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    status, text = speech_to_text(file)
    if not status:
        bot.send_message(message.chat.id, text)
        return

    if len(text.split()) > 100:
        bot.send_message(user_id, "Сообщение не должно содержать больше 100 слов")
        return

    status, gpt_answer = ask_gpt(text)
    if not status:
        bot.send_message(user_id, "Не удалось ответить. Попробуй другое описание.")
        return

    users[user_id] += 1
    bot.send_message(user_id, gpt_answer)


bot.polling(non_stop=True)