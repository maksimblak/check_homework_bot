from reports.base_report_builder import BaseReportBuilder

class FinishReportBuilder(BaseReportBuilder):
    """
    Класс для создания отчета о завершении дисциплины.
    Наследует функциональность из BaseReportBuilder.
    """

    def __init__(self, group_id: int, discipline_id: int):
        """
        Конструктор класса.

        :param group_id: Идентификатор группы.
        :param discipline_id: Идентификатор дисциплины.
        """
        super().__init__(group_id, discipline_id, 'finish_report')
