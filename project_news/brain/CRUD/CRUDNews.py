from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from .models import create_session, News


class CRUDNews:

    @staticmethod
    @create_session
    def add(news, session=None):
        session.add(news)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(news)
            return news

    @staticmethod
    @create_session
    def get(news_id, session=None):
        news = session.execute(
            select(News)
            .where(News.id == news_id)
        )
        news = news.first()
        if news:
            return news[0]

    @staticmethod
    @create_session
    def all(session=None):
        news = session.execute(
            select(News)
            .order_by(News.id)
        )
        return [i[0] for i in news]

    @staticmethod
    @create_session
    def update(news, session=None):
        news = news.__dict__
        del news['_sa_instance_state']
        session.execute(
            update(News)
            .where(News.id == news['id'])
            .values(**news)
        )
        try:
            session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_session
    def delete(news_id, session=None):
        session.execute(
            delete(News)
            .where(News.id == news_id)
        )
        session.commit()
