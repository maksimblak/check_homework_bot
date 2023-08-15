from datetime import datetime

from pydantic import BaseModel


class TestLogInit(BaseModel):
    """
    Модель инициализации лога тестирования.

    Содержит информацию о студенте, номере работы и времени запуска.
    """
    student_id: int
    lab_id: int
    run_time: datetime


class TaskReport(BaseModel):
    """
    Модель отчета о задаче.

    Содержит информацию о задаче, времени выполнения, статусе и описании.
    """
    task_id: int
    time: datetime
    status: bool
    description: set[str] = []


class LabReport(BaseModel):
    """
    Модель отчета о лабораторной работе.

    Содержит информацию о номере лабораторной работы и списках задач.
    """
    lab_id: int
    tasks: list[TaskReport] = []
