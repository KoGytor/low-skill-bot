import random
import telebot
import os
from deep_translator import MyMemoryTranslator
from dotenv import load_dotenv
from telebot import *

load_dotenv('mini_projects/data.env')

last_message = 0

token = os.getenv('TOKEN_BOT')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def function(message):
    global last_message
    button_game = types.InlineKeyboardButton(text='Игра "Рандом"🎲', callback_data = 'random')
    button_translator = types.InlineKeyboardButton(text = 'Переводчик текста🔡', callback_data = 'translate')
    markup = types.InlineKeyboardMarkup()
    markup.add(button_game)
    markup.add(button_translator)
    bot_message = bot.send_message(
        text = 'Чего бы вы хотели?',
        chat_id = message.chat.id,
        reply_markup=markup
    )
    last_message = bot_message.id

def menu(chat_id):
    global last_message
    bot.delete_message(
        chat_id = chat_id,
        message_id = last_message
    )
    button_game = types.InlineKeyboardButton(text='Игра "Рандом"🎲', callback_data = 'random')
    button_translator = types.InlineKeyboardButton(text = 'Переводчик текста🔡', callback_data = 'translate')
    markup = types.InlineKeyboardMarkup()
    markup.add(button_game)
    markup.add(button_translator)
    bot_message = bot.send_message(
        text = 'Чего бы вы хотели?',
        chat_id = chat_id,
        reply_markup=markup
    )
    last_message = bot_message.id

def translator(message):
    global last_message
    bot_message = sent_message = bot.send_message(
        message.chat.id,
        "Отправь текст для перевода:🔤"
    )
    bot.delete_message(
        chat_id = message.chat.id,
        message_id = last_message
    )
    last_message = bot_message.id

    bot.register_next_step_handler(sent_message, translate)

def translate(message):
    global last_message
    bot.delete_message(
        chat_id = message.chat.id,
        message_id = last_message
    )
    text = message.text
    translator = MyMemoryTranslator(source = 'ru-RU', target = 'en-GB')
    translated_text = translator.translate(text)

    markup = types.InlineKeyboardMarkup()
    button_menu = types.InlineKeyboardButton(text = 'Меню🏠', callback_data = 'menu')
    button_translate = types.InlineKeyboardButton(text = 'Перевести еще🔄', callback_data = 'translate')
    markup.add(button_menu, button_translate)

    bot_message = bot.send_message(
        text = translated_text,
        chat_id = message.chat.id,
        reply_markup = markup
    )

    last_message = bot_message.id

def random_game(chat_id):
    global last_message
    bot.delete_message(
        chat_id = chat_id,
        message_id = last_message
    )
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton(text = 'Меню🏠', callback_data='menu')
    button_1 = types.InlineKeyboardButton(text = '1️⃣', callback_data=1)
    button_2 = types.InlineKeyboardButton(text = '2️⃣', callback_data=2)
    button_3 = types.InlineKeyboardButton(text = '3️⃣', callback_data=3)
    button_4 = types.InlineKeyboardButton(text = '4️⃣', callback_data=4)
    button_5 = types.InlineKeyboardButton(text = '5️⃣', callback_data=5)
    button_6 = types.InlineKeyboardButton(text = '6️⃣', callback_data=6)
    markup.add(button_1, button_2, button_3)
    markup.add(button_4, button_5, button_6)
    markup.add(button_back)
    bot_message = bot.send_message(
        text = 'Угадайте, какое число было загадано ботом❓',
        chat_id = chat_id,
        reply_markup=markup
    )
    
    last_message = bot_message.id

def lose_menu(chat_id, choice):
    global last_message
    bot.delete_message(
        chat_id = chat_id,
        message_id = last_message
    )
    markup = types.InlineKeyboardMarkup()
    button_again = types.InlineKeyboardButton(text = 'Играть снова🔄', callback_data = 'random')
    button_menu = types.InlineKeyboardButton(text = 'Меню🏠', callback_data = 'menu')
    markup.add(button_again, button_menu)
    bot_message = bot.send_message(
        text = f'❌Увы, ты проиграл, выпала цифра {choice}.❌',
        chat_id = chat_id,
        reply_markup = markup
    )
    last_message = bot_message.id

def win_menu(chat_id, choice):
    global last_message
    bot.delete_message(
        chat_id = chat_id,
        message_id = last_message
    )
    markup = types.InlineKeyboardMarkup()
    button_again = types.InlineKeyboardButton(text = 'Играть снова🔄', callback_data = 'random')
    button_menu = types.InlineKeyboardButton(text = 'Меню🏠', callback_data = 'menu')
    markup.add(button_again, button_menu)
    bot_message = bot.send_message(
        text = f'✅Вы выйграли, выпала цифра {choice}!✅',
        chat_id = chat_id,
        reply_markup = markup
    )
    last_message = bot_message.id


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
    elif call.data == 'translate':
        translator(message)
        
        

bot.polling(none_stop=True)