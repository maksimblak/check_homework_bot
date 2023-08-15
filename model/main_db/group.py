from typing import List
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.main_db.database import Base
from model.main_db.discipline import Discipline
from model.main_db.discipline_group import association_discipline_to_group
from model.main_db.student import Student
from model.main_db.teacher import Teacher
from model.main_db.teacher_group import association_teacher_to_group


class Group(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'groups'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'group_name' с типом данных String(20), представляющей название группы.
    group_name: Mapped[str] = Column(String(20), unique=True)

    # Определение связи "один-ко-многим" с таблицей 'students' через атрибут 'students'.
    students: Mapped[List["Student"]] = relationship(
        back_populates="group",
        cascade="all, delete, delete-orphan",
        # cascade='save-update, merge, delete',
    )

    # Определение связи "многие-ко-многим" с таблицей 'disciplines' через атрибут 'disciplines'.
    disciplines: Mapped[List["Discipline"]] = relationship(
        secondary=association_discipline_to_group,
        back_populates="groups",
    )

    # Определение связи "многие-ко-многим" с таблицей 'teachers' через атрибут 'teachers'.
    teachers: Mapped[List["Teacher"]] = relationship(
        secondary=association_teacher_to_group,
        back_populates="groups",
    )

    # Метод __repr__ определяет строковое представление объекта Group для отладки и вывода.
    def __repr__(self):
        return f'Группа [ID: {self.id}, Название: {self.group_name}]'
