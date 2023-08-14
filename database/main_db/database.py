import os

# Импортируем библиотеку для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Импортируем функции для работы с базой данных
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Загружаем переменные окружения из файла .env
load_dotenv()

# Создаем подключение к базе данных SQLite, используя значение из переменной окружения
engine = create_engine(f'sqlite:///{os.getenv("DATABASE_NAME")}.sqlite')
# Создаем класс Session, который будет использоваться для работы с базой данных
Session = sessionmaker(bind=engine)


# Определяем функцию-слушателя, которая будет вызываться при каждом подключении к базе данных
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Создаем курсор для выполнения SQL-запросов
    cursor = dbapi_connection.cursor()
    # Устанавливаем параметр PRAGMA foreign_keys=ON, чтобы включить проверку внешних ключей
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Создаем базовый класс DeclarativeBase, который будет использоваться для определения моделей
class Base(DeclarativeBase):
    pass


# Функция для создания таблиц в базе данных на основе определенных моделей
def create_tables():
    Base.metadata.create_all(engine)
