from pydantic import BaseModel


# Класс StudentsGroup представляет данные о группе студентов.
class StudentsGroup(BaseModel):
    # Определение атрибута 'group_name' с типом данных str, представляющего имя группы.
    group_name: str

    # Определение атрибута 'disciplines_short_name' с типом данных list[str],
    # представляющего список коротких имен дисциплин, связанных с группой.
    disciplines_short_name: list[str]

    # Определение атрибута 'students' с типом данных list[str], представляющего список студентов в группе.
    students: list[str]
