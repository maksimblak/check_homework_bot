import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

# Создание движка для базы данных очередей с использованием SQLite
engine = create_engine(f'sqlite:///{os.getenv("QUEUE_DB_NAME")}.sqlite')
# Создание сессии для базы данных очередей
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Функция для создания таблиц в базе данных
def create_tables():
    Base.metadata.create_all(engine)
