import json

from pydantic.json import pydantic_encoder

from database.queue_db.database import Session
from model.pydantic.test_rejected_files import TestRejectedFiles
from model.queue_db.rejected import Rejected


# Функция добавления записи о непринятых файлах в базу данных
def add_record(
        user_tg_id: int,
        chat_id: int,
        rejected: TestRejectedFiles
) -> None:
    session = Session()

    json_data = json.dumps(
        rejected,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ': '),
        default=pydantic_encoder
    )

    session.add(
        Rejected(
            telegram_id=user_tg_id,
            chat_id=chat_id,
            data=json_data
        )
    )
    session.commit()
    session.close()


# Функция проверки, пуста ли база данных непринятых файлов
def is_empty() -> bool:
    with Session() as session:
        data = session.query(Rejected).first()
        return data is None


# Функция проверки, не пуста ли база данных непринятых файлов
def is_not_empty() -> bool:
    with Session() as session:
        data = session.query(Rejected).first()
        return data is not None


# Функция получения первой записи о непринятых файлах из базы данных
def get_first_record() -> Rejected:
    """
       Получает первую запись о непринятых файлах из базы данных и удаляет ее.

       :return: Запись о непринятых файлах.
       """
    with Session() as session:
        record = session.query(Rejected).first()
        session.query(Rejected).filter(
            Rejected.id == record.id
        ).delete(synchronize_session='fetch')
        session.commit()
        return record
