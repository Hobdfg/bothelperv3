import telebot

from speechkit import voice_to_text
from yandex_gpt import ask_gpt
from config import TOKEN

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
    status, text = voice_to_text(file)
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