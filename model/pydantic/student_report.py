from pydantic import BaseModel


class StudentReport(BaseModel):
    full_name: str = '' #полное имя студента
    points: float = 0  #количество баллов
    lab_completed: int = 0 #количество завершенных лабораторных работ
    deadlines_fails: int = 0 #количество не выполненных дедлайнов
    task_completed: int = 0 #количество завершенных  задач
    task_ratio: int = 0 #соотношение выполненных задач от всего обьема задач