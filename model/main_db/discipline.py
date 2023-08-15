from typing import List

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database.main_db.database import Base
from model.main_db.discipline_group import association_discipline_to_group
from model.main_db.group import Group
from model.main_db.teacher import Teacher
from model.main_db.teacher_discipline import association_teacher_to_discipline


class Discipline(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'disciplines'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'full_name' с типом данных String(100), представляющей полное имя дисциплины.
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Определение колонки 'short_name' с типом данных String(10), представляющей короткое имя дисциплины.
    short_name: Mapped[str] = mapped_column(String(10), nullable=False)

    # Определение колонки 'path_to_test' с типом данных String(200), представляющей путь к тестам.
    path_to_test: Mapped[str] = mapped_column(String(200), nullable=False)

    # Определение колонки 'path_to_answer' с типом данных String(200), представляющей путь к ответам на тесты.
    path_to_answer: Mapped[str] = mapped_column(String(200), nullable=False)

    # Определение колонки 'language' с типом данных String(10), представляющей язык дисциплины.
    language: Mapped[str] = mapped_column(String(10), nullable=False)

    # Определение колонки 'max_tasks' с типом данных Integer, представляющей максимальное количество задач.
    max_tasks: Mapped[int] = mapped_column(nullable=False)

    # Определение колонки 'max_home_works' с типом данных Integer, представляющей максимальное количество д з.
    max_home_works: Mapped[int] = mapped_column(nullable=False)

    # Определение колонки 'works' с типом данных JSON, представляющей конфигурацию заданий.
    works: Mapped[str] = mapped_column(JSON, nullable=False)  # DisciplineWorksConfig

    # Определение связи "многие-ко-многим" с таблицей 'groups' через атрибут 'groups'.
    groups: Mapped[List["Group"]] = relationship(
        secondary=association_discipline_to_group,
        back_populates="disciplines",
    )

    # Определение связи "многие-ко-многим" с таблицей 'teachers' через атрибут 'teachers'.
    teachers: Mapped[List["Teacher"]] = relationship(
        secondary=association_teacher_to_discipline,
        back_populates="disciplines",
    )

    # Метод __repr__ определяет строковое представление объекта Discipline для отладки и вывода.
    def __repr__(self):
        info: str = f'Дисциплина {self.short_name}, ' \
                    f'max_tasks: {self.max_tasks}, ' \
                    f'works: {self.works}]'
        return info
