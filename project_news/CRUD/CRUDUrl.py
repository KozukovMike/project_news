from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from .models import create_session, Url


class CRUDUrl:

    @staticmethod
    @create_session
    def add(url, session=None):
        session.add(url)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(url)
            return url

    @staticmethod
    @create_session
    def get(url_id, session=None):
        url = session.execute(
            select(Url)
            .where(Url.id == url_id)
        )
        url = url.first()
        if url:
            return url[0]

    @staticmethod
    @create_session
    def get_by_url(url_url, session=None):
        url = session.execute(
            select(Url)
            .where(Url.url == url_url)
        )
        url = url.first()
        if url:
            return url[0]

    @staticmethod
    @create_session
    def all(session=None):
        urls = session.execute(
            select(Url)
            .order_by(Url.id)
        )
        return [i[0] for i in urls]

    @staticmethod
    @create_session
    def update(url, session=None):
        url = url.__dict__
        del url['_saUrl_instance_state']
        session.execute(
            update(Url)
            .where(Url.id == url['id'])
            .values(**url)
        )
        try:
            session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_session
    def delete(url_id, session=None):
        session.execute(
            delete(Url)
            .where(Url.id == url_id)
        )
        session.commit()
