import json
import telebot
from urllib.request import Request, urlopen
from random import randint, choice, shuffle
import cowsay
import os
from dotenv import load_dotenv
load_dotenv()

music = [
    {
        "id": "AwACAgQAAxkDAAM4ZA2SksJY9x4VTPOX6pZ-6TOl2j4AAhMPAALyYWhQyLSz9GI_2hEvBA",
        "right": "Твоё Нежное Безумие - Весна 13",
        "wrong": [
            "Твоё нежное безумие - Муттер_",
            "Твоё нежное безумие - Любящий Брат",
            "твоё нежное безумие - печенье и шоколад"
            ]
        },
    {
        "id": "AwACAgQAAxkDAAM6ZA2SkuCdvLA0dwlWPoSCK1Az3DIAAhQPAALyYWhQVmXOz2-URnkvBA",
        "right": "Твоё нежное безумие - Любящий Брат",
        "wrong": [
            "твоё нежное безумие - печенье и шоколад",
            "Твоё Нежное Безумие - Весна 13",
            "Твоё нежное безумие - Муттер_"
            ]
        },
    {
        "id": "AwACAgQAAxkDAAM8ZA2Sk0W2Z095xlfS-q3pNekdId4AAhUPAALyYWhQiz0T7m7z2eYvBA",
        "right": "Твоё нежное безумие - Муттер_",
        "wrong": [
            "Твоё Нежное Безумие - Весна 13",
            "Твоё нежное безумие - Любящий Брат",
            "твоё нежное безумие - печенье и шоколад"
            ]
        },
    {
        "id": "AwACAgQAAxkDAAM-ZA2SlCz_6-mCPf-gCAh8Q7P3efAAAhYPAALyYWhQW6y3uIVa7gsvBA",
        "right": "твоё нежное безумие - печенье и шоколад",
        "wrong": [
            "Твоё нежное безумие - Муттер_",
            "Твоё нежное безумие - Любящий Брат",
            "Твоё Нежное Безумие - Весна 13"
            ]
        }
]

bot = telebot.TeleBot(os.getenv("TOKEN"))

def generate_markup(right, wrong):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
    answers = wrong + [right]
    shuffle(answers)
    for elem in answers:
        markup.add(elem)
    return markup 

users = { }
stats = { }

@bot.message_handler(commands=['game'])
def game(message):
    global users
    song = choice(music)
    markup = generate_markup(song["right"], song["wrong"])
    bot.send_voice(message.chat.id, song["id"], reply_markup = markup)
    users[message.chat.id] = song["right"]
    
@bot.message_handler(commands=['stats'])
def stats_get(message):
        right_count, all_count = stats.get(message.chat.id, (0,0) )
        bot.send_message(message.chat.id, f'Правильных ответов: {right_count}, игр: {all_count}')
        
@bot.message_handler(content_types=['text'])
def check_answer(message):
    right_count, all_count = stats.get(message.chat.id, (0,0) )
    
    right = users.get(message.chat.id, None)
    if not right:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
        return
    all_count += 1
    if message.text == right:
        text = 'Верно!'
        right_count += 1
    else:
        text = 'Увы, Вы не угадали. Попробуйте ещё раз!'
    bot.send_message(message.chat.id, text, reply_markup = telebot.types.ReplyKeyboardRemove())
    users.pop(message.chat.id)
    stats[message.chat.id] = (right_count, all_count)

bot.infinity_polling()
