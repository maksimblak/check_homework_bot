import json

from pydantic.json import pydantic_encoder
from model.pydantic.queue_out_raw import TestResult
from database.queue_db.database import Session
from model.queue_db.queue_out import QueueOut


# Функция проверки, пуста ли база данных исходящих очередей
def is_empty() -> bool:
    with Session() as session:
        data = session.query(QueueOut).first()
        return data is None


# Функция проверки, не пуста ли база данных исходящих очередей
def is_not_empty() -> bool:
    with Session() as session:
        data = session.query(QueueOut).first()
        return data is not None


# Функция получения всех записей из базы данных исходящих очередей
def get_all_records() -> list[QueueOut]:
    with Session() as session:
        return session.query(QueueOut).all()


# Функция удаления записи из базы данных исходящих очередей по ее идентификатору
def delete_record(record_id: int) -> None:
    with Session() as session:
        session.query(QueueOut).filter(
            QueueOut.id == record_id
        ).delete(synchronize_session='fetch')
        session.commit()


# Функция добавления записи в базу данных исходящих очередей
def add_record(user_tg_id: int, chat_id: int, data: TestResult) -> None:
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
        QueueOut(
            telegram_id=user_tg_id,
            chat_id=chat_id,
            data=json_data
        )
    )
    session.commit()
    session.close()
