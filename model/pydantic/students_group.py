from pydantic import BaseModel


class StudentsGroup(BaseModel):
    group_name: str # имя группы
    disciplines_short_name: list[str] # короткое имя дисциплины
    students: list[str] #студенты