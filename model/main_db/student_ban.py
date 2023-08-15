from sqlalchemy.orm import mapped_column, Mapped
from database.main_db.database import Base


class StudentBan(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'banlist'

    # Определение колонки 'telegram_id' с типом данных Integer, используется как первичный ключ.
    telegram_id: Mapped[int] = mapped_column(primary_key=True)

    # Метод __repr__ определяет строковое представление объекта StudentBan для отладки и вывода.
    def __repr__(self):
        return f'Ban [ID: {self.telegram_id}]'
