import random
import telebot
import os
from dotenv import load_dotenv
from telebot import *

load_dotenv('mini_projects/data.env')

token = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def function(message):
    button1 = types.InlineKeyboardButton(text='Игра "Рандом', callback_data='random')
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(
        text = 'Чего бы вы хотели?',
        chat_id = message.chat.id,
        reply_markup=markup
    )

def menu(chat_id):
    button1 = types.InlineKeyboardButton(text='Игра "Рандом', callback_data='random')
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(
        text = 'Чего бы вы хотели?',
        chat_id = chat_id,
        reply_markup=markup
    )

def random_game(chat_id):
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton(text = 'Меню', callback_data='menu')
    button_1 = types.InlineKeyboardButton(text = '1', callback_data=1)
    button_2 = types.InlineKeyboardButton(text = '2', callback_data=2)
    button_3 = types.InlineKeyboardButton(text = '3', callback_data=3)
    button_4 = types.InlineKeyboardButton(text = '4', callback_data=4)
    button_5 = types.InlineKeyboardButton(text = '5', callback_data=5)
    button_6 = types.InlineKeyboardButton(text = '6', callback_data=6)
    markup.add(button_1, button_2, button_3)
    markup.add(button_4, button_5, button_6)
    markup.add(button_back)
    bot.send_message(
        text = '!Угадай число от 1 до 6!',
        chat_id = chat_id,
        reply_markup=markup
    )

def lose_menu(chat_id, choice):
    markup = types.InlineKeyboardMarkup()
    button_again = types.InlineKeyboardButton(text = 'Играть снова', callback_data = 'random')
    button_menu = types.InlineKeyboardButton(text = 'Меню', callback_data = 'menu')
    markup.add(button_again, button_menu)
    bot.send_message(
        text = f'Увы, ты проиграл, выпала цифра {choice}.',
        chat_id = chat_id,
        reply_markup = markup
    )

def win_menu(chat_id, choice):
    markup = types.InlineKeyboardMarkup()
    button_again = types.InlineKeyboardButton(text = 'Играть снова', callback_data = 'random')
    button_menu = types.InlineKeyboardButton(text = 'Меню', callback_data = 'menu')
    markup.add(button_again, button_menu)
    bot.send_message(
        text = f'Вы выйграли, выпала цифра {choice}!',
        chat_id = chat_id,
        reply_markup = markup
    )


@bot.callback_query_handler(func=lambda call: True)
def send_message(call):
    message = call.message
    chat_id = message.chat.id
    if call.data == 'random':
        random_game(chat_id)
    elif call.data in ['1','2','3','4','5','6']:
        choice = random.randint(1, 6)
        if choice != int(call.data):
            lose_menu(chat_id, choice)
        else:
            win_menu(chat_id, choice)
    elif call.data == 'menu':
        menu(chat_id)


bot.polling(none_stop=True)