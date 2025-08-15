import telebot
from random import randint
from datetime import datetime
import reqests
import os
import gdown
from flask import Flask, request 
TOKEN = ("os.getenv(BOT _TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode=None)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"


@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_update([update])
    return '', 200


@bot.message_handler(commands =['start'])
def send_welcome(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Игра: угадай число на кубике")
        button2 = telebot.types.KeyboardButton(text="Игровой автомат")
        button3 = telebot.types.KeyboardButton(text="Время(/date)")
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Привет", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands =['list'])
def list(message)
    try:
        bot.send_message(message.chat.id, "Список команд: 1.Время /date")


@bot.message_handler(commands =['date'])
def date(message):
    try:
        bot.send_message(message.chat.id, "Сейчас: " + str(datetime.today()))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands =['random'])
def random(message):
    try:
        bot.send_message(message.chat.id, "Случайное число: " + str(randint(1, 1000)))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands=['image'])
def send_image(message):
    try:
        file = open("mama.jpg", 'rb')
        bot.send_photo(message.chat.id, file, caption="Вот ваше изображение: ")
        file.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")



@bot.message_handler(content_types=['text'])
def answer(message):
    try:
        text = message.text

        if text == "Привет":
            bot.send_message(message.chat.id, "Привет!")
        elif text == "Как дела?":
            bot.send_message(message.chat.id, "Прекрасно!")
        elif text == "Как тебя зовут?":
            bot.send_message(message.chat.id, "Меня зовут Бот!")
        elif text == "Игровой автомат":
           value = bot.send_dice(message.chat.id, emoji='🎰').dice.value
           if value in (1, 16, 22, 32, 43, 48):
               bot.send_message(message.chat.id, "Победа!")
           elif value == 64:
               bot.send_message(message.chat.id, "Джекпот!")
           else:
               bot.send_message(message.chat.id, "Попробуй ещё раз")
        elif text == "Игра в кубик":
            keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=3)
            button1 = telebot.types.InlineKeyboardButton("1", callback_data='1')
            button2 = telebot.types.InlineKeyboardButton("2", callback_data='1')
            button3 = telebot.types.InlineKeyboardButton("3", callback_data='3')
            button4 = telebot.types.InlineKeyboardButton("4", callback_data='4')
            button5 = telebot.types.InlineKeyboardButton("5", callback_data='5')
            button6 = telebot.types.InlineKeyboardButton("6", callback_data='6')
            keyboard2.add(button1, button2, button3, button4, button5, button6)
            bot.send_message(message.chat.id, "Игра:Угадай число на кубике", reply_markup=keyboard2)
        else:
            bot.send_message(message.chat.id, text)
    except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {e}")
@bot.callback_query_handler(func=lambda call: call.data in ("1", "2", "3", "4", "5", "6"))
def dice_answer(call):
    value = bot.send_dice(call.message.chat.id, emoji='').dice.value
    if str(value) == call.data:
        bot.send_message(call.message.chat.id, "Вы угадали!")
    else:
        bot.send_message(call.message.chat.id, "Попробуй ещё раз")



if __name__ == "__main__ ок":
    server_url = os.getenv("RENDER_EXTERNAL_URL")
    if server_url and TOKEN:
        webhook_url = f"{server_url}/{TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
        try:
            r = requests.get(set_webhook_url)
            print("Webhook установлен:", r.text)
        except Exception as e:
            print("Ошибка при установке webhook:", e)

        port = int(os.environ.get("PORT", 10000))
        print(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port)
    else:
        print("Запуск бота в режиме pooling")
        bot.remove_webhook()
        bot.polling(none_stop=True)
