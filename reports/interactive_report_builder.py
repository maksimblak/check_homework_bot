import json
from datetime import datetime

from database.main_db import common_crud
from model.pydantic.home_work import DisciplineHomeWorks
from model.pydantic.student_report import StudentReport


def run_interactive_report_builder(
        student_id: int,
        discipline_id: int) -> StudentReport:
    """
    Функция запуска формирования интерактивного отчета об успеваемости конкретного студента.

    :param student_id: Идентификатор студента.
    :param discipline_id: Идентификатор дисциплины.

    :return: Структура данных StudentReport с информацией об успеваемости студента.
    """
    student_report = StudentReport()  # Создание экземпляра StudentReport для хранения отчета.
    student = common_crud.get_student_from_id(student_id)  # Получение данных о студенте из базы данных.
    student_answer = common_crud.get_student_discipline_answer(student_id, discipline_id)
    # Получение ответа студента по дисциплине.

    student_report.full_name = student.full_name  # Заполнение полного имени студента в отчете.
    home_works = DisciplineHomeWorks(
        **json.loads(student_answer.home_work)).home_works  # Загрузка данных о домашних работах студента.
    student_report.points = student_answer.point  # Заполнение баллов студента в отчете.

    # Подсчет выполненных лабораторных работ и несданных дедлайнов.
    for work in home_works:
        if work.is_done:
            student_report.lab_completed += 1
        if datetime.now().date() > work.deadline:
            if work.end_time is not None:
                if work.end_time.date() > work.deadline:
                    student_report.deadlines_fails += 1
            else:
                student_report.deadlines_fails += 1

    # Подсчет выполненных задач.
    for work in home_works:
        for task in work.tasks:
            if task.is_done:
                student_report.task_completed += 1

    discipline = common_crud.get_discipline(discipline_id)  # Получение данных о дисциплине.
    if student_report.task_completed != 0:
        student_report.task_ratio = student_report.task_completed / discipline.max_tasks  # Рассчет соотношения
        # выполненных задач.

    return student_report  # Возврат сформированного отчета об успеваемости студента.
