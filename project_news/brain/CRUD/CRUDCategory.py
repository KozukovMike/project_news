from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from .models import create_session, Category


class CRUDCategory:

    @staticmethod
    @create_session
    def add(category, session=None):
        session.add(category)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(category)
            return category

    @staticmethod
    @create_session
    def get(category_id, session=None):
        category = session.execute(
            select(Category)
            .where(Category.id == category_id)
        )
        category = category.first()
        if category:
            return category[0]

    @staticmethod
    @create_session
    def get_by_category(category_category, session=None):
        category = session.execute(
            select(Category)
            .where(Category.category == category_category)
        )
        category = category.first()
        if category:
            return category[0]

    @staticmethod
    @create_session
    def all(session=None):
        categories = session.execute(
            select(Category)
            .order_by(Category.id)
        )
        return [i[0] for i in categories]

    @staticmethod
    @create_session
    def update(category, session=None):
        category = category.__dict__
        del category['_sa_instance_state']
        session.execute(
            update(Category)
            .where(Category.id == category['id'])
            .values(**category)
        )
        try:
            session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_session
    def delete(category_id, session=None):
        session.execute(
            delete(Category)
            .where(Category.id == category_id)
        )
        session.commit()
