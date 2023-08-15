from sqlalchemy.orm import Mapped, mapped_column
from database.main_db.database import Base


# Определение класса Chat, представляющего таблицу 'chats' в базе данных.
class Chat(Base):
    __tablename__ = 'chats'

    # Определение колонки 'chat_id' с типом данных Integer, которая используется как первичный ключ.
    chat_id: Mapped[int] = mapped_column(primary_key=True)

    # Метод __repr__ определяет строковое представление объекта Chat для отладки и вывода.
    def __repr__(self):
        return f'Chat [ID: {self.chat_id}]'
