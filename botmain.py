import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from response import Resp
import os

version = "0.0.1"
apihelper.proxy = {'http': os.environ['HTTP_PROXY'],
                   'https': os.environ['HTTPS_PROXY']}
token = os.environ['TG_TOKEN']
bot = telebot.TeleBot(token)

@bot.callback_query_handler(func=lambda call: call.data == 'Back_menu')
def to_menu(call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="Moscow", callback_data="Moscow"),
               InlineKeyboardButton(text="Perm", callback_data="Perm"))
    bot.edit_message_text(text="Select city", chat_id=chat_id, message_id=message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: '-' in call.data)
def forecat(call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    city = call.data.split('-')[0]
    time = call.data.split('-')[1]
    resp = Resp(city=city, time=time)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Back to menu", callback_data="Back_menu"))
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=resp.get_resp(), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: '-' not in call.data)
def city_choise(call):
    data = call.data
    chat_id = call.from_user.id
    message_id = call.message.message_id
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Today", callback_data=f"{data}-Today"),
               InlineKeyboardButton(text="Tomorrow", callback_data=f"{data}-Tomorrow"),
               InlineKeyboardButton(text="Week", callback_data=f"{data}-Week"))
    bot.edit_message_text(text="When?", message_id=message_id, chat_id=chat_id, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="Moscow", callback_data="Moscow"),
               InlineKeyboardButton(text="Perm", callback_data="Perm"))
    bot.send_message(chat_id=chat_id, text="Select city", reply_markup=markup)


if __name__ == '__main__':
    print(f"VERSION: {version}")
    while True:
        bot.polling()