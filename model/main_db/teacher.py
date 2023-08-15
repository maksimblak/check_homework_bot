from dataclasses import dataclass
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.main_db.database import Base
from model.main_db.discipline import Discipline
from model.main_db.group import Group
from model.main_db.teacher_discipline import association_teacher_to_discipline
from model.main_db.teacher_group import association_teacher_to_group


class Teacher(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'teachers'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'full_name' с типом данных String(150), представляющей полное имя преподавателя.
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)

    # Определение колонки 'telegram_id' с типом данных Integer, уникальный идентификатор Telegram.
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    # Определение связи "многие-ко-многим" с таблицей 'disciplines' через атрибут 'disciplines'.
    disciplines: Mapped[List["Discipline"]] = relationship(
        secondary=association_teacher_to_discipline,
        back_populates="teachers",
    )

    # Определение связи "многие-ко-многим" с таблицей 'groups' через атрибут 'groups'.
    groups: Mapped[List["Group"]] = relationship(
        secondary=association_teacher_to_group,
        back_populates="teachers",
    )

    # Метод __repr__ определяет строковое представление объекта Teacher для отладки и вывода.
    def __repr__(self):
        info: str = f'Преподаватель [ФИО: {self.full_name}, ' \
                    f'Telegram ID: {self.telegram_id}]'
        return info
