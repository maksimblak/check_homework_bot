from sqlalchemy import JSON
from sqlalchemy.orm import mapped_column, Mapped

from database.queue_db.database import Base


class QueueIn(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'input'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'telegram_id' с типом данных Integer, не может быть пустой.
    telegram_id: Mapped[int] = mapped_column(nullable=False)

    # Определение колонки 'chat_id' с типом данных Integer, не может быть пустой.
    chat_id: Mapped[int] = mapped_column(nullable=False)

    # Определение колонки 'data' с типом данных JSON, представляющей данные в формате JSON.
    data: Mapped[str] = mapped_column(JSON, nullable=False)

    # Метод __repr__ определяет строковое представление объекта QueueIn для отладки и вывода.
    def __repr__(self):
        return f'Q(input) [ID: {self.id}, TG: {self.telegram_id}, chat: {self.chat_id}, \ndata: {self.data}\n]'
