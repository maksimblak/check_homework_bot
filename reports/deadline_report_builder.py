import json
from datetime import datetime

from database.main_db import common_crud
from model.pydantic.home_work import DisciplineHomeWorks
from model.pydantic.student_report import StudentReport


def run_deadline_report_builder(student_id: int, discipline_id: int) -> str:
    """
    Функция для формирования отчета о дедлайнах для студента.

    :param student_id: Идентификатор студента.
    :param discipline_id: Идентификатор дисциплины.

    :return: Строка с отчетом о дедлайнах.
    """
    student_report = StudentReport()  # Создание объекта для отчета.
    student = common_crud.get_student_from_id(student_id)  # Получение информации о студенте.
    student_answer = common_crud.get_student_discipline_answer(student_id, discipline_id)  # Получение ответов студента.

    # Заполнение информации о студенте в отчете.
    student_report.full_name = student.full_name
    home_works = DisciplineHomeWorks(**json.loads(student_answer.home_work)).home_works  # Загрузка данных о работах.

    current_date = datetime.now().date()  # Текущая дата.

    deadline_failed = 0  # Счетчик просроченных дедлайнов.
    nearest_deadline = None  # Ближайший дедлайн.

    # Просмотр работ студента.
    for work in home_works:
        if current_date < work.deadline:  # Если дедлайн еще не наступил.
            nearest_deadline = work.deadline
            break
        elif work.end_time is not None:  # Если есть время окончания работы.
            if work.deadline < work.end_time.date():  # Если дедлайн просрочен.
                deadline_failed += 1
        else:  # Если дедлайн просрочен и нет времени окончания работы.
            deadline_failed += 1

    # Формирование отчета в зависимости от ситуации.
    if deadline_failed == len(home_works):
        return f'У меня для тебя плохие новости! Прожми батоны, т.к. завалены все дедлайны!!!'
    elif nearest_deadline is not None:
        return f'Ближайший дедлайн {nearest_deadline} в 23:59'
    else:
        return f'Сроки всех дедлайнов истекли! Если имеешь задолженность - напрягай батоны!!!'
