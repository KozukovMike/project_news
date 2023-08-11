import io
import requests
import telebot
import pandas as pd

from datetime import datetime


class CustomErrors(Exception):

    def __init__(self):
        pass

    @staticmethod
    def to_file(file_name: str, e, command_name: str, message):
        with open(file_name, 'a', encoding='utf-8') as file:
            text = f'{e} at {datetime.now()} at command /{command_name}\n'
            file.write(text)
        bot.send_message(message.chat.id,
                         'Произошла ошибка, возможно вы не вызвали команду /initialization')


waiting_for_word = {}
keyboard_state = {}
# df = pd.read_csv('C:/Users/mike/PycharmProjects/parsing/dataframe.csv')
# df_norm = pd.read_csv('C:/Users/mike/PycharmProjects/parsing/my_dataframe.csv')

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('initialization', 'info')

keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('news', 'send_pdf1', 'send_pdf2')
keyboard2.row('send_analysis')
keyboard2.row('Вернуться')

bot = telebot.TeleBot('6284138251:AAGpCfjUCDhCynDSD9Uzv7bUrshfbyO48ZA')
url = 'http://127.0.0.1:8000/'


@bot.message_handler(commands=['start'])
def start(message):
    keyboard_state[message.chat.id] = keyboard1
    data = {'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            }
    response = requests.post(url=f'{url}start', json=data)
    res = response.json()
    if response.ok:
        bot.send_message(message.chat.id, res['message'], reply_markup=keyboard1, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'info')
def info(message):
    response = requests.post(url=f'{url}info', json={})
    res = response.json()
    if response.ok:
        bot.send_message(message.chat.id, res['message'], parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Возникла ошибка')


@bot.message_handler(func=lambda message: message.text == 'initialization')
def initialization(message):
    waiting_for_word['initialization'] = True
    bot.send_message(message.chat.id, 'Введите одно слово для анализа', reply_markup=keyboard2)
    keyboard_state[message.chat.id] = keyboard2

    @bot.message_handler(content_types=['text'])
    def word_init(message):

        data = {'word': message.text,
                'id':  message.chat.id,
                }
        response = requests.post(url=f'{url}initialization', json=data)
        if response.ok:
            bot.send_message(message.chat.id, f'Ваше слово {message.text}')
        elif response.status_code == 400:
            res = response.json()
            bot.send_message(message.chat.id, res['error'], parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'Возникла ошибка')
        del waiting_for_word['initialization']


@bot.message_handler(func=lambda message: message.text == 'news')
def get_news(message):
    try:
        id_ = message.chat.id
        response = requests.get(f'{url}news/{id_}')
        if response.status_code == 200:

            response_number = requests.post(url=f'{url}number', json={'id': id_})
            number = response_number.json()
            bot.send_message(message.chat.id, f'Кол-во новостей: {number["message"]}')

            with open(f'news{id_}.txt',  'wb') as file:
                file.write(response.content)

            with open(f'news{id_}.txt', 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            CustomErrors.to_file('errors', requests.exceptions.HTTPError, 'news', message)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'news', message)


@bot.message_handler(func=lambda message: message.text == 'send_pdf1')
def send_pdf1(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        id_ = message.chat.id
        response = requests.get(f'{url}send_pdf1/{id_}')
        if response.status_code == 200:
            pdf_content = response.content
            bot.send_document(message.chat.id, io.BytesIO(pdf_content), visible_file_name=f'{id_}.pdf')
        else:
            CustomErrors.to_file('errors', requests.exceptions.HTTPError, 'send_pdf1', message)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'send_pdf1', message)


@bot.message_handler(func=lambda message: message.text == 'send_pdf2')
def send_pdf2(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        id_ = message.chat.id
        response = requests.get(f'{url}send_pdf2/{id_}')
        if response.status_code == 200:
            pdf_content = response.content
            bot.send_document(message.chat.id, io.BytesIO(pdf_content), visible_file_name=f'{id_}.pdf')
        else:
            CustomErrors.to_file('errors', requests.exceptions.HTTPError, 'send_pdf2', message)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'send_pdf2', message)


@bot.message_handler(func=lambda message: message.text == 'send_analysis')
def sentiment_analysis(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        response = requests.post(url=f'{url}send_analysis', json={'id': message.chat.id})
        res = response.json()
        if response.status_code == 200:
            bot.send_message(message.chat.id, res['message'])
        else:
            CustomErrors.to_file('errors', requests.exceptions.HTTPError, 'sent_analysis', message)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'sent_analysis', message)


@bot.message_handler(func=lambda message: message.text == 'Вернуться')
def handle_return_button(message):
    keyboard_state[message.chat.id] = keyboard1
    bot.send_message(message.chat.id, 'вернулись к первому меню', reply_markup=keyboard1)
    del keyboard_state[message.chat.id]


bot.polling(none_stop=True)
