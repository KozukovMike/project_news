import pymorphy3


from constanta import News, NormalizedNews
from typing import List


def normalize(l_news: List[News]) -> List[NormalizedNews]:
    morph = pymorphy3.MorphAnalyzer()
    res = []
    for news in l_news:
        norm_list_of_words = [morph.parse(word)[0].normal_form for word in news.title.split()]
        res.append(
            NormalizedNews(
                title=news.title,
                url=news.url,
                date=news.date,
                normalized_title=norm_list_of_words,
                category=news.category,
            )
        )
    return res
