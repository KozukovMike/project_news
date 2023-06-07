import requests
import re


from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


from constanta import News


class ParsNews(ABC):

    headers = {
        'accept': '*/*',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    today = str(datetime.today().strftime('%Y-%m-%d'))

    @abstractmethod
    def pars_news(self):
        pass

    @staticmethod
    def to_errors(url: str):
        with open('news_pars_errors.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.now()}, {url}\n')

    @staticmethod
    def preprocessing_title(all_articles: List[str]) -> List[str]:
        all_articles = list(map(lambda x: x.text, all_articles))
        all_articles = list(map(str.strip, all_articles))
        all_articles = list(map(str.lower, all_articles))
        all_articles = list(filter(lambda x: x.count(' ') > 3, all_articles))
        return all_articles

    @staticmethod
    def preprocessing_url(url: str) -> str:
        url = re.findall(r'//[a-z, A-Z,., 1-9]+/', url)[0]
        url = url[2:len(url) - 1]
        return url


class GoogleNews(ParsNews):

    urls = {
        'world': 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru',
        'economy': 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru',
        'about all': 'https://news.google.com/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiTkNCSVNORG9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q2hJSUwyMHZNR1JzZUdwNkNnb0lMMjB2TUdSc2VHb29BQSowCAAqLAgKIiZDQklTRmpvSWJHOWpZV3hmZGpKNkNnb0lMMjB2TUdSc2VHb29BQVABUAE?hl=ru&gl=RU&ceid=RU%3Aru',
        'science': 'https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnlkUm9DVWxVb0FBUAE?hl=ru&gl=RU&ceid=RU%3Aru',
        'sport': 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru'
    }

    def pars_news(self) -> List[News]:
        res = []

        for category, url in GoogleNews.urls.items():
            try:
                html = requests.get(url, headers=GoogleNews.headers)
                soup = BeautifulSoup(html.text, 'lxml')
                all_articles = soup.find_all('h4', class_='gPFEn')
                all_articles = ParsNews.preprocessing_title(all_articles)
                url = ParsNews.preprocessing_url(url)
                for title in all_articles:
                    res.append(News(title=title,
                                    category=category,
                                    date=datetime.today().strftime('%Y-%m-%d'),
                                    url=url))

            except Exception as e:
                ParsNews.to_errors(url)

        return res


class By024(ParsNews):

    urls = {
        'society': 'https://024.by/news/society/',
        'economy': 'https://024.by/news/economies/',
        'politics': 'https://024.by/news/politics/',
        'world': 'https://024.by/news/world/',
        'motor': 'https://024.by/news/auto/',
        'culture': 'https://024.by/news/culture/',
        'sport': 'https://024.by/news/sports/',
        'incidents': 'https://minsknews.by/news-list/insidents/'
    }

    def pars_news(self) -> List[News]:
        res = []

        for category, url in By024.urls.items():
            try:
                html = requests.get(url, headers=By024.headers)
                soup = BeautifulSoup(html.text, 'lxml')
                all_articles = soup.find_all('h2', class_='grid__h2')
                all_articles = ParsNews.preprocessing_title(all_articles)
                url = ParsNews.preprocessing_url(url)
                for title in all_articles:
                    res.append(News(title=title,
                                    category=category,
                                    date=datetime.today().strftime('%Y-%m-%d'),
                                    url=url))

            except Exception as e:
                ParsNews.to_errors(url)

        return res


class MinskNews(ParsNews):

    urls = {
        'society': 'https://minsknews.by/news-list/society/',
        'economy': 'https://minsknews.by/news-list/economics/',
        'culture': 'https://minsknews.by/news-list/culture/',
        'sport': 'https://minsknews.by/news-list/sport/',
        'incidents': 'https://minsknews.by/news-list/insidents/'
    }

    def pars_news(self) -> List[News]:
        res = []

        for category, url in MinskNews.urls.items():
            try:
                html = requests.get(url, headers=MinskNews.headers)
                soup = BeautifulSoup(html.text, 'lxml')
                all_articles = soup.find_all('a', class_='content__description')
                all_articles = ParsNews.preprocessing_title(all_articles)
                url = ParsNews.preprocessing_url(url)
                for title in all_articles:
                    res.append(News(title=title,
                                    category=category,
                                    date=datetime.today().strftime('%Y-%m-%d'),
                                    url=url))

            except Exception as e:
                ParsNews.to_errors(url)

        return res


class Onliner(ParsNews):

    urls = {
        'economy': 'https://money.onliner.by/',
        'society': 'https://people.onliner.by/',
        'motor': 'https://auto.onliner.by/',
        'science': 'https://tech.onliner.by/',
    }

    def pars_news(self) -> List[News]:
        res = []

        for category, url in Onliner.urls.items():
            try:
                html = requests.get(url, headers=Onliner.headers)
                soup = BeautifulSoup(html.text, 'lxml')
                all_articles = soup.find_all('span', class_="news-helpers_hide_mobile-small")
                all_articles += soup.find_all('div', class_='news-tiles__subtitle max-lines-3')
                all_articles = ParsNews.preprocessing_title(all_articles)
                url = ParsNews.preprocessing_url(url)
                for title in all_articles:
                    res.append(News(title=title,
                                    category=category,
                                    date=datetime.today().strftime('%Y-%m-%d'),
                                    url=url))

            except Exception as e:
                ParsNews.to_errors(url)

        return res


class Regexparser(ParsNews):

    b = 'https://sport.unian.net/?_gl=1*1t6vn6x*_ga*MTQ3MTgxNDUyMy4xNjc4ODk3MTI3*_ga_TECJ2YKWSJ*MTY3ODg5NzEyNi4xLjEuMTY3ODg5NzY1NS4wLjAuMA..*_ga_DENC12J6P3*MTY3ODg5NzEyNi4xLjEuMTY3ODg5NzY1NS4yNy4wLjA.*_ga_238PLP1PQZ*MTY3ODg5NzEyNy4xLjEuMTY3ODg5NzY1NS4wLjAuMA..*_ga_P6EEJX21DY*MTY3ODg5NzEyNy4xLjEuMTY3ODg5NzY1NS4yNy4wLjA.'
    a = 'https://health.unian.net/?_gl=1*4zpid5*_ga*MTQ3MTgxNDUyMy4xNjc4ODk3MTI3*_ga_TECJ2YKWSJ*MTY3ODg5NzEyNi4xLjEuMTY3ODg5NzY2Mi4wLjAuMA..*_ga_DENC12J6P3*MTY3ODg5NzEyNi4xLjEuMTY3ODg5NzY2Mi4yMC4wLjA.*_ga_238PLP1PQZ*MTY3ODg5NzEyNy4xLjEuMTY3ODg5NzY2Mi4wLjAuMA..*_ga_P6EEJX21DY*MTY3ODg5NzEyNy4xLjEuMTY3ODg5NzY2Mi4yMC4wLjA.'
    urls = {
        'sport': ['https://iz.ru/rubric/sport', 'https://lenta.ru/rubrics/sport/', f'{b}',
                  'https://freesmi.by/category/sport', 'https://www.belnovosti.by/sport', 'https://sputnik.by/sport/',
                  'https://www.sb.by/articles/main_sport/', 'https://rsport.ria.ru/'],
        'politics': ['https://riafan.ru/category/politika', 'https://www.unian.net/politics',
                     'https://freesmi.by/category/politika', 'https://www.tvr.by/news/politika/',
                     'https://www.belnovosti.by/politika', 'https://ria.ru/politics/', 'https://sputnik.by/politics/',
                     'https://www.sb.by/articles/main_policy/'],
        'economy': ['https://by.tsargrad.tv/materials/rubric/jekonomika', 'https://riafan.ru/category/economica',
                    'https://iz.ru/rubric/ekonomika', 'https://lenta.ru/rubrics/economics/',
                    'https://www.unian.net/economics', 'https://freesmi.by/category/ekonomika',
                    'https://neg.by/novosti/kategorija/makroekonomika/', 'https://www.tvr.by/news/ekonomika/',
                    'https://www.belnovosti.by/ekonomika', 'https://sputnik.by/economy/', 'https://ria.ru/economy/',
                    'https://www.sb.by/articles/main_economy/'],
        'education': ['https://sputnik.by/education/'],
        'culture': ['https://lenta.ru/rubrics/culture/', 'https://freesmi.by/category/culture',
                    'https://www.tvr.by/news/kultura/', 'https://www.belnovosti.by/kultura',
                    'https://www.sb.by/articles/main_culture/', 'https://ria.ru/culture/'],
        'society': ['https://by.tsargrad.tv/materials/rubric/obshhestvo', 'https://riafan.ru/category/obshestvo',
                    'https://iz.ru/rubric/obshchestvo', 'https://freesmi.by/category/obshhestvo',
                    'https://www.tvr.by/news/obshchestvo/', 'https://www.belnovosti.by/obshchestvo',
                    'https://www.sb.by/articles/main_society/', 'https://ria.ru/society/',
                    'https://www.sb.by/articles/mozaika-zhizni/'],
        'world': ['https://by.tsargrad.tv/materials/rubric/v-mire', 'https://riafan.ru/category/ves-mir',
                  'https://iz.ru/rubric/mir', 'https://lenta.ru/rubrics/world/', 'https://www.unian.net/world',
                  'https://www.tvr.by/news/v_mire/', 'https://www.belnovosti.by/v-mire',
                  'https://www.sb.by/articles/main_world/', 'https://sputnik.by/world/', 'https://ria.ru/world/'],
        'health': [f'{a}', 'https://www.belnovosti.by/krasota-i-zdorove', 'https://www.sb.by/articles/health/',
                   'https://sputnik.by/health/'],
        'motor': ['https://www.belnovosti.by/avto', 'https://sputnik.by/motor/', 'https://www.sb.by/articles/drive/'],
        'tourism': ['https://www.unian.net/tourism', 'https://lenta.ru/rubrics/travel/', 'https://ria.ru/tourism/'],
        'religion': ['https://by.tsargrad.tv/materials/rubric/religija', 'https://ria.ru/religion/'],
        'science': ['https://lenta.ru/rubrics/science/', 'https://www.unian.net/science',
                    'https://freesmi.by/category/it-nauka-i-texnologii', 'https://www.sb.by/articles/kosmos/'],
        'show business': ['https://www.belnovosti.by/shoubiznes', 'https://www.sb.by/articles/telenedelya/'],
        'exchange rates': ['https://sputnik.by/kursy-valyut-belarus/'],
        'money issues': ['https://www.sb.by/articles/dela-zhiteyskie/'],
        'fashion': ['https://www.sb.by/articles/shpilki/'],
        'about all': ['https://tass.ru/tag/belorussiya', 'https://by.vesti.news/top100/',
                      'https://www.belnovosti.by/rekordy-i-antirekordy', 'https://www.belta.by/all_news',
                      'https://www.sb.by/blog/'],
        'incidents': ['https://by.tsargrad.tv/materials/rubric/proisshestvija',
                      'https://riafan.ru/category/proishestviya', 'https://www.unian.net/incidents',
                      'https://freesmi.by/category/katastrofy', 'https://www.sb.by/articles/main_Incidents/',
                      'https://ria.ru/incidents/', 'https://ria.ru/defense_safety/', 'https://sputnik.by/geoBelarus/',
                      'https://sputnik.by/tag_Russia/'],
    }

    def pars_news(self) -> List[News]:
        res = []

        for category, list_of_urls in Regexparser.urls.items():
            for url in list_of_urls:
                try:
                    html = requests.get(url, headers=Regexparser.headers)
                    soup = BeautifulSoup(html.text, 'lxml')
                    all_articles = soup.find_all(['a', 'div', 'span', 'h1', 'h4'],
                                                 {'class': re.compile("[a-z0-9_\-;]{0,100}(title)[a-z0-9_\-;]{0,100}")})
                    url = re.findall(r'//[a-z, A-Z,., 1-9]+/', url)[0]
                    all_articles = ParsNews.preprocessing_title(all_articles)
                    url = ParsNews.preprocessing_url(url)
                    for title in all_articles:
                        res.append(News(title=title,
                                        category=category,
                                        date=datetime.today().strftime('%Y-%m-%d'),
                                        url=url))

                except Exception as e:
                    ParsNews.to_errors(url)

        return res
