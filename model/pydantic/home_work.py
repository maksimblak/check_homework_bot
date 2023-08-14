from pydantic import BaseModel
from datetime import datetime, date


class HomeTask(BaseModel):  # Модель для представления домашней задачи
    number: int  # Номер задачи
    is_done: bool = False  # Флаг, указывающий, выполнена ли задача (по умолчанию - False)
    last_try_time: datetime | None = None  # Время последней попытки выполнения задачи (datetime) или None
    amount_tries: int = 0  # Количество попыток выполнения задачи (по умолчанию - 0)


class HomeWork(BaseModel):  # Модель для представления домашней работы
    number: int  # Номер домашней работы
    deadline: date  # Срок сдачи домашней работы (дата)
    tasks: list[HomeTask]  # Список задач, связанных с данной домашней работой
    is_done: bool = False  # Флаг, указывающий, выполнена ли домашняя работа (по умолчанию - False)
    tasks_completed: int = 0
    end_time: datetime | None = None  # Время завершения домашней работы (datetime) или None (по умолчанию - None)


class DisciplineHomeWorks(BaseModel):
    home_works: list[HomeWork]  # Список домашних работ для данной дисциплины
