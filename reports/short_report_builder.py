import json
from datetime import datetime

from database.main_db import common_crud
from model.pydantic.home_work import DisciplineHomeWorks
from reports.base_report_builder import BaseReportBuilder, ReportFieldEnum


class ShortReportBuilder(BaseReportBuilder):
    def __init__(self, group_id: int, discipline_id: int):
        # Вызов конструктора базового класса для инициализации свойств
        super().__init__(group_id, discipline_id, 'short_report')

    def build_report(self) -> None:
        # Вызов метода построения базового отчета для инициализации таблицы и шапки
        super().build_report()
        worksheet = self.wb.active  # Получение активного листа в книге

        students = common_crud.get_students_from_group(self.group_id)  # Получение списка студентов группы
        row = 1  # Начальная строка для заполнения отчета
        for student in students:
            answers = common_crud.get_student_discipline_answer(student.id, self.discipline_id)
            # Получение ответов студента
            home_works = DisciplineHomeWorks(
                **json.loads(answers.home_work)).home_works  # Получение заданий по домашним работам
            if row == 1:
                col = ReportFieldEnum.NEXT  # Начальный столбец для заполнения данных
                for number_lab, work in enumerate(home_works):
                    # Заполнение столбцов заголовка, отображающих долю выполненных задач и сроки дедлайнов
                    worksheet.cell(
                        row=row, column=col
                    ).value = f'lab{number_lab + 1}_ratio'
                    worksheet.cell(
                        row=row, column=col + 1
                    ).value = f'lab{number_lab + 1}_deadline'
                    col += 2
                row += 1
            if row > 1:
                col = ReportFieldEnum.NEXT  # Начальный столбец для заполнения данных
                for work in home_works:
                    cell = worksheet.cell(row=row, column=col + 1)  # Получение ячейки для статуса дедлайнов
                    if datetime.now().date() > work.deadline:  # Проверка, просрочен ли дедлайн
                        if work.end_time is not None:
                            # Проверка, было ли время на выполнение после дедлайна
                            if work.end_time.date() > work.deadline:
                                cell.value = 'bad'
                                cell.fill = BaseReportBuilder.RED_FILL  # Установка красной заливки
                            else:
                                cell.value = 'good'
                                cell.fill = BaseReportBuilder.GREEN_FILL  # Установка зеленой заливки
                        else:
                            cell.value = 'bad'
                            cell.fill = BaseReportBuilder.RED_FILL  # Установка красной заливки
                    else:
                        cell.value = 'good'
                        cell.fill = BaseReportBuilder.GREEN_FILL  # Установка зеленой заливки

                    tasks_in_lab = len(work.tasks)  # Общее количество задач в лабораторной работе
                    tasks_completed = 0
                    for task in work.tasks:
                        if task.is_done:
                            tasks_completed += 1  # Подсчет выполненных задач
                    worksheet.cell(
                        row=row, column=col
                    ).value = tasks_completed / tasks_in_lab  # Расчет и заполнение доли выполненных задач
                    col += 2
            row += 1
