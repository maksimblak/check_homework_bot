import json

from pydantic.json import pydantic_encoder
from model.pydantic.queue_in_raw import QueueInRaw
from database.queue_db.database import Session
from model.queue_db.queue_in import QueueIn


# Функция добавления записи в базу данных очередей
def add_record(user_tg_id: int, chat_id: int, data: QueueInRaw) -> None:
    """
        Добавляет запись в базу данных очередей.

        :param user_tg_id: Телеграм ID пользователя.
        :param chat_id: ID чата.
        :param data: Данные для добавления.

        :return: None
        """
    session = Session()
    json_data = json.dumps(
        data,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ': '),
        default=pydantic_encoder
    )

    session.add(
        QueueIn(
            telegram_id=user_tg_id,
            chat_id=chat_id,
            data=json_data
        )
    )
    session.commit()
    session.close()


# Функция проверки, пуста ли база данных очередей
def is_empty() -> bool:
    """
        Проверяет, пуста ли база данных очередей.

        :return: True, если база данных пуста, иначе False.
        """
    with Session() as session:
        data = session.query(QueueIn).first()
        return data is None


# Функция проверки, не пуста ли база данных очередей
def is_not_empty() -> bool:
    """
        Проверяет, не пуста ли база данных очередей.

        :return: True, если база данных не пуста, иначе False.
        """
    with Session() as session:
        data = session.query(QueueIn).first()
        return data is not None


# Функция получения первой записи из базы данных очередей
def get_first_record() -> QueueIn:
    """
       Получает первую запись из базы данных очередей, удаляя ее после извлечения.

       :return: Первая запись из базы данных.
       """
    with Session() as session:
        record = session.query(QueueIn).first()
        session.query(QueueIn).filter(
            QueueIn.id == record.id
        ).delete(synchronize_session='fetch')
        session.commit()
        return record
