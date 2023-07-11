from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, create_engine, DATETIME
from .settings import DATABASE_URL


Base = declarative_base()


class Url(Base):
    __tablename__: str = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(VARCHAR(50), nullable=False, unique=True)


class Category(Base):
    __tablename__: str = 'categories'

    id = Column(Integer, primary_key=True)
    category = Column(VARCHAR(50), nullable=False, unique=True)


class News(Base):
    __tablename__: str = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(250), nullable=False, unique=True)
    date = Column(VARCHAR(30), nullable=False, unique=False)
    news_id = Column(Integer, ForeignKey('urls.id', ondelete='CASCADE'), nullable=False)
    categories_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_session(func):
    def wrapper(**kwargs):
        with Session() as session:
            return func(session=session, **kwargs)
    return wrapper


