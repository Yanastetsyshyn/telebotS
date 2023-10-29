import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Доброго дня, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот створений для генерації паролів.У боті є дві команди: /start - для інформації про бота та /newpassword - для генерації самаго пароля  .".format(message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(commands=['newpassword'])
def password(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("UA")
    item2 = types.KeyboardButton("EN")

    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Оберіть мову для пароля", reply_markup=markup)
    bot.register_next_step_handler(message, process_language_choice)

def process_language_choice(message):
    if message.text == "UA":
        bot.send_message(message.chat.id, "Введіть кількість букв в паролі")
        bot.register_next_step_handler(message, generate_ua_password)
    elif message.text == "EN":
        bot.send_message(message.chat.id, "Введіть кількість букв в паролі")
        bot.register_next_step_handler(message, generate_en_password)
    else:
        bot.send_message(message.chat.id, "Не знаю що відповісти")

def generate_ua_password(message):
    try:
        length = int(message.text)
        ua_alphabet = "йцукенгшщззхїєждлорпавіфячсмитьбю1234567890"
        password = ''.join(random.choice(ua_alphabet) for _ in range(length))
        bot.send_message(message.chat.id, f"Ось ваш пароль українською: {password}")
        bot.send_message(message.chat.id,"Дякую за використання бота!")
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть ціле число для довжини паролю")
def generate_en_password(message):
    try:
        length = int(message.text)
        en_alphabet = "qwertyuioplkjhgfdsazxcvbnm1234567890"
        password = ''.join(random.choice(en_alphabet) for _ in range(length))
        bot.send_message(message.chat.id, f"Ось ваш пароль англіскькою мовою: {password}")
        bot.send_message(message.chat.id,"Дякую за використання бота!")
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть ціле число для довжини паролю")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Не знаю що відповісти")

# RUN
bot.polling(none_stop=True)

