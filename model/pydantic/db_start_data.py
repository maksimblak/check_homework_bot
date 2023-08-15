from dataclasses import dataclass
from pydantic import BaseModel
from model.pydantic.students_group import StudentsGroup
from model.pydantic.discipline_works import DisciplineWorksConfig
from model.pydantic.teacher import Teacher


# Класс DbStartData представляет начальные данные для заполнения базы данных.
class DbStartData(BaseModel):
    # Определение атрибута 'groups' для хранения списка объектов StudentsGroup.
    groups: list[StudentsGroup]

    # Определение атрибута 'disciplines' для хранения списка объектов DisciplineWorksConfig.
    disciplines: list[DisciplineWorksConfig]

    # Определение атрибута 'teachers' для хранения списка объектов Teacher.
    teachers: list[Teacher]

    # Определение атрибута 'chats' для хранения списка идентификаторов чатов.
    chats: list[int]


# Декоратор @dataclass применен к классу StudentRaw, описывающему необработанные данные студента.
@dataclass
class StudentRaw:
    full_name: str


# Декоратор @dataclass применен к классу TeacherRaw, описывающему необработанные данные преподавателя.
@dataclass
class TeacherRaw:
    full_name: str
    telegram_id: int
    is_admin: bool
