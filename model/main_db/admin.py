from sqlalchemy import Column, Integer, Boolean
from database.main_db.database import Base

class Admin(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'admin'

    # Определение колонки 'telegram_id' с типом данных Integer, которая будет использоваться как первичный ключ.
    telegram_id = Column('telegram_id', Integer, primary_key=True)

    # Определение колонки 'teacher_mode' с типом данных Boolean и значением по умолчанию False.
    teacher_mode = Column('teacher_mode', Boolean, default=False)

    # Метод __repr__ определяет строковое представление объекта Admin для отладки и вывода.
    def __repr__(self):
        return f'Admin [ID: {self.telegram_id}]'
