import telebot
import pymorphy3


from brain.normalize import df_where_word_in
from brain.charts import Chart
from brain.sentiment_analysis import SentimentAnalysis
from datetime import datetime, timedelta
from brain.db import DynamoDBClient


bot = telebot.TeleBot('6284138251:AAGpCfjUCDhCynDSD9Uzv7bUrshfbyO48ZA')

waiting_for_word = {}
word = {}
df_where_word = {}
keyboard_state = {}
df = DynamoDBClient.get_from_bd('News')
df_norm = DynamoDBClient.get_from_bd('NormalizedNews')[['normalized_title', 'url', 'date', 'category']]


class CustomErrors(Exception):

    def __init__(self):
        pass

    @staticmethod
    def to_file(file_name: str, e: Exception, command_name: str, message):
        with open(file_name, 'a', encoding='utf-8') as file:
            text = f'{e} at {datetime.now()} at command /{command_name}\n'
            file.write(text)
        bot.send_message(message.chat.id,
                         'Произошла ошибка, возможно вы не вызвали команду /initialization')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    text = f'Здравствуйте, {message.from_user.first_name.capitalize()} {message.from_user.last_name.capitalize()}! ' \
           f'напишите команду /project для информации о проектах ' \
           f'напишите команду /info для информации о командах '
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['project'])
def project(message):
    pass


@bot.message_handler(commands=['info'])
def info(message):
    text = 'команда /initialization позволит вам начать работу бота\n' \
           'все последующие команды без предыдущей не работают!!!\n\n' \
           'команда /news высылает файл формата txt со всеми новостями, имеющие искомое слово\n\n' \
           'команда /send_pdf1 высылает pdf file с графиком, который показывает сколько' \
           'новостей с вашим словом и в каких категориях эти новости\n\n' \
           'команда /send_pdf2 высылает pdf file с 3 графиками, в которых ' \
           'показаны самые часто упоминаемые знаменитый лица, географические объекты и большие компании\n\n' \
           'команда /sent_analysis показывает анализ настроения новостей с ващим словом\n\n' \
           'команад /sent_analysis_time позволяет сделать анализ настроения новостей во времени, ' \
           'подробнее можно узнать вызвав эту команду\n\n'
    bot.send_message(message.chat.id, text)
    pass


@bot.message_handler(commands=['news'])
def get_news(message):
    try:
        news = df.loc[df_where_word[message.chat.id].index, 'title']
        bot.send_message(message.chat.id, f'Количество новойстей: {len(news.index)}')
        news.to_csv('news.txt', index=False, sep='\t')

        with open('news.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'news', message)


@bot.message_handler(commands=['initialization'])
def initialization(message):
    waiting_for_word['initialization'] = True
    bot.send_message(message.chat.id, 'Введите слово для анализа')

    @bot.message_handler(func=lambda x: waiting_for_word.get('initialization'))
    def take_word(message):
        enter_word = message.text
        global word, df_where_word
        if len(enter_word.split()) > 1:
            mes = 'Вы ввели больше одного слова,  к сожалению мы не можем так обработать, чтобы ввести заново слово ' \
                  'вызовите команду /initialization'
            bot.send_message(message.chat.id, mes)
        else:
            word[message.chat.id] = enter_word
            bot.send_message(message.chat.id, f'Ваше слово {enter_word}')
            morph = pymorphy3.MorphAnalyzer()
            word_normal = morph.parse(enter_word)[0].normal_form
            df_where_word[message.chat.id] = df_where_word_in(df_norm, word_normal)
        del waiting_for_word['initialization']


@bot.message_handler(commands=['send_pdf1'])
def send_pdf1(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        Chart.box_plot_mentions(df_where_word[message.chat.id])
        with open('example.pdf', 'rb') as pdf_file:
            bot.send_document(message.chat.id, pdf_file)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'send_pdf1', message)


@bot.message_handler(commands=['send_pdf2'])
def send_pdf2(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        Chart.big_names(df_where_word[message.chat.id], df)
        with open('example1.pdf', 'rb') as pdf_file:
            bot.send_document(message.chat.id, pdf_file)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'send_pdf2', message)


@bot.message_handler(commands=['sent_analysis'])
def sentiment_analysis(message):
    bot.send_message(message.chat.id, 'Это может занять некоторое время')
    try:
        res = SentimentAnalysis.dostoevsky_analysis(df_where_word[message.chat.id], df)
        res = res.loc[["neutral", "positive", "negative"], :].to_string(header=False)
        bot.send_message(message.chat.id, res)
    except Exception as e:
        CustomErrors.to_file('errors', e, 'sent_analysis', message)


@bot.message_handler(commands=['sent_analysis_time'])
def sentiment_analysis_through_time(message):
    waiting_for_word['sent_analysis_time'] = True
    text = 'Введите дату с которой начинать анализ в виде год-месяц-день\n' \
           'Введите дату которой заканчивается анализ в виде год-месяц-день\n' \
           'Введите кол-во дне через которые проводить анализ числом\n' \
           'Все это одним сообщением\n' \
           'Пример: 2023-03-20 2023-04-05 3'
    bot.send_message(message.chat.id, text)

    @bot.message_handler(func=lambda x: waiting_for_word.get('sent_analysis_time'))
    def processing(message):
        start_date, end_date, delta = message.text.split()[0], message.text.split()[1], message.text.split()[2]
        bot.send_message(message.chat.id, f'{start_date},  {end_date}, {delta}')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = timedelta(days=int(delta))
        if start_date > end_date:
            bot.send_message(message.chat.id, 'Вы ввели конечную дату больше начальной')
        else:
            try:
                SentimentAnalysis.dostoevsky_through_time(df_where_word[message.chat.id], df, start_date,
                                        end_date,
                                        delta)
                with open('sent_analysis_time.pdf', 'rb') as pdf_file:
                    bot.send_document(message.chat.id, pdf_file)
                del waiting_for_word['sent_analysis_time']
            except Exception as e:
                del waiting_for_word['sent_analysis_time']
                CustomErrors.to_file('errors', e, 'sent_analysis_time', message)


bot.polling(none_stop=True)

