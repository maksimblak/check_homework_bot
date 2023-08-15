from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database.main_db.database import Base
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.group import Group


class Student(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'students'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'full_name' с типом данных String(120), представляющей полное имя студента.
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)

    # Определение колонки 'group_id' с типом данных Integer, внешний ключ к таблице 'groups',
    # при удалении группы из базы, соответствующие записи будут удаляться (CASCADE).
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id', ondelete='CASCADE'),
        nullable=False
    )

    # Определение колонки 'telegram_id' с типом данных Integer, уникальный идентификатор Telegram.
    telegram_id: Mapped[int] = mapped_column(nullable=True, unique=True)

    # Определение связи "многие-к-одному" с таблицей 'groups' через атрибут 'group'.
    group: Mapped["Group"] = relationship(
        back_populates="students"
    )

    # Определение связи "один-ко-многим" с таблицей 'assigned_disciplines' через атрибут 'homeworks'.
    homeworks: Mapped[List["AssignedDiscipline"]] = relationship(
        back_populates="student", cascade="all, delete, delete-orphan"
    )

    # Метод __repr__ определяет строковое представление объекта Student для отладки и вывода.
    def __repr__(self):
        info: str = f'Студент [ФИО: {self.full_name}, ' \
                    f'ID группы: {self.group}, Telegram ID: {self.telegram_id}]'
        return info
