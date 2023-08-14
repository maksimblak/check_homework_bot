from datetime import date
from pydantic import BaseModel

class DisciplineWork(BaseModel):
    number: int                  # Номер работы по дисциплине
    amount_tasks: int            # Количество задач в работе
    deadline: date               # Срок выполнения работы

class DisciplineWorksConfig(BaseModel):
    full_name: str               # Полное название дисциплины
    short_name: str              # Краткое название дисциплины
    path_to_test: str            # Путь к тестовым данным
    path_to_answer: str          # Путь к ответам на задачи
    language: str                # Используемый язык 
    works: list[DisciplineWork]  # Список работ по дисциплине

class DisciplinesConfig(BaseModel):
    disciplines: list[DisciplineWorksConfig]  # Список конфигураций для разных дисциплин (обертка)
