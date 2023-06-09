import pandas as pd
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas


class SentimentAnalysis:

    tokenizer = RegexTokenizer()

    @staticmethod
    def dostoevsky_analysis(df_where_word_in: pd.DataFrame, df: pd.DataFrame):

        '''
        функция проводит анализ тональности, используя библиотеку dostoevsky
        :param df_where_word_in: датафрейм с новостями где есть слово
        :param df: датафрейм изначальный с новостями
        :return: датафрейм со столбиком 'title' где находятся новости и с 4 столбиками оценки тональности,
        для каждой новости
        '''

        model = FastTextSocialNetworkModel(tokenizer=SentimentAnalysis.tokenizer)
        messages = df.loc[df_where_word_in.index, 'title']
        results = model.predict(messages, k=5)
        check = pd.DataFrame(results)
        res = pd.DataFrame(check.mean())
        check['title'] = df.loc[df_where_word_in.index, 'title'].reset_index().drop('index', axis=1)
        return res

    @staticmethod
    def dostoevsky_through_time(
            df_where_word_in: pd.DataFrame, df: pd.DataFrame,
            start_date: datetime, end_date: datetime, delta: timedelta
                                ):

        '''
        проводим анализ с помощью библиотеки dostoevsky через определенную константу времени
        :param df_where_word_in: датафрейм содержащий нужное слово
        :param df: датафрейм начальный
        :param start_date: дата с которой начинаем анализ
        :param end_date: дата которой заканчиваем анализ
        :param delta: константа времени через которую проводится анализ
        :return:
        '''

        current_date = start_date
        model = FastTextSocialNetworkModel(tokenizer=SentimentAnalysis.tokenizer)
        flag = True
        pdf_file = "sent_analysis_time.pdf"
        c = canvas.Canvas(pdf_file)
        buf = 840
        while flag:
            previous_date = current_date
            current_date = previous_date + delta

            if current_date > end_date:
                current_date = end_date
                flag = False
            #     print(current_date)
            messages = df.loc[df_where_word_in[df_where_word_in['date'].between(previous_date.strftime("%Y-%m-%d"),
                                                                                current_date.strftime(
                                                                                    "%Y-%m-%d"))].index, 'title']
            results = model.predict(messages, k=5)
            check = pd.DataFrame(results)
            text = pd.DataFrame(check.mean()).loc[["neutral", "positive", "negative"], :].to_string(header=False)
            if buf == 0:
                c.showPage()
                buf = 840
            buf -= 20
            c.drawString(0, buf, current_date.strftime('%Y-%m-%d'))
            if buf == 0:
                c.showPage()
                buf = 840
            buf -= 20
            c.drawString(0, buf, text)
            check['title'] = df.loc[df_where_word_in.index, 'title'].reset_index().drop('index', axis=1)
        c.showPage()
        c.save()
