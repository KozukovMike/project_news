import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymorphy3
import spacy
from reportlab.pdfgen import canvas


class Chart:

    @staticmethod
    def box_plot_mentions(df_where_word_in: pd.DataFrame):

        '''
        выводит график кол-во новостей по категориям с нужным словом
        :param df_where_word_in: датафрейм со словом нормлаизовнный
        :return: ничего, но записывает в pdf file
        '''

        number_of_mentions = df_where_word_in.groupby('category')['category'].value_counts()
        buf = []
        a = []
        for name, value in number_of_mentions.items():
            buf.append(name)
            a.append(value)
        d = {'0': buf, '1': a}
        number_of_mentions = pd.DataFrame(data=d)
        number_of_mentions.columns = ['category', 'amount']
        fig, ax = plt.subplots(figsize=(6, 2))

        _ = sns.barplot(x='category', y='amount', data=number_of_mentions, palette="magma")

        ax.grid(True)
        ax.set(title="number of articles in each category")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=35)

        plt.subplots_adjust(bottom=0.3, top=0.7, left=0.1, right=0.9)
        plt.savefig('chart.png')
        pdf = canvas.Canvas('example.pdf')
        pdf.drawImage('chart.png', 0, 650)
        pdf.save()
        # plt.show()

    @staticmethod
    def big_names(df_where_word_in: pd.DataFrame, df: pd.DataFrame):

        '''
        выводит 3 графика личностей, компаний и стран с нужным словоем
        :param df_where_word_in: датафрейм со словом
        :param df: датафрейм обычный
        :return: ничего, но записывает в pdf file
        '''

        morph = pymorphy3.MorphAnalyzer()
        nlp = spacy.load("ru_core_news_lg")

        people = {}
        companies = {}
        countries = {}

        for title in df.loc[df_where_word_in.index, 'title']:
            doc = nlp(title)
            for entity in doc.ents:
                if entity.label_ == "PER":
                    entity = morph.parse(entity.text)[0].normal_form
                    if entity not in people.keys():
                        people[entity] = 1
                    else:
                        people[entity] += 1
                elif entity.label_ == "ORG":
                    entity = morph.parse(entity.text)[0].normal_form
                    if entity not in companies.keys():
                        companies[entity] = 1
                    else:
                        companies[entity] += 1
                elif entity.label_ == "LOC":
                    entity = morph.parse(entity.text)[0].normal_form
                    if entity not in countries.keys():
                        countries[entity] = 1
                    else:
                        countries[entity] += 1

        people = dict(sorted(people.items(), key=lambda x: x[1], reverse=True)[:10])
        companies = dict(sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10])
        countries = dict(sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10])

        plt.figure(figsize=(6, 4))
        plt.subplots_adjust(bottom=0.3, top=0.8)
        plt.bar(people.keys(), people.values(), color='orange')
        plt.title('личности')
        plt.ylabel('кол-во упоминаний')
        plt.xticks(rotation=90)

        plt.savefig('chart1.png')
        pdf = canvas.Canvas('example1.pdf')
        pdf.drawImage('chart1.png', 0, 450)
        pdf.showPage()

        # plt.show()

        plt.figure(figsize=(6, 4))
        plt.subplots_adjust(bottom=0.3, top=0.8)
        plt.bar(companies.keys(), companies.values(), color='orange')
        plt.title('компании')
        plt.ylabel('кол-во упоминаний')
        plt.xticks(rotation=90)

        plt.savefig('chart2.png')
        pdf.drawImage('chart2.png', 0, 450)
        pdf.showPage()

        # plt.show()

        plt.figure(figsize=(6, 4))
        plt.subplots_adjust(bottom=0.3, top=0.8)
        plt.bar(countries.keys(), countries.values(), color='orange')
        plt.title('географические объекты')
        plt.ylabel('кол-во упоминаний')
        plt.xticks(rotation=90)

        plt.savefig('chart3.png')
        pdf.drawImage('chart3.png', 0, 450)
        pdf.save()
        pdf.showPage()

        # plt.show()
