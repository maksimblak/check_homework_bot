from enum import Enum

from reports.base_report_builder import BaseReportBuilder
from reports.finish_report_builder import FinishReportBuilder
from reports.full_report_builder import FullReportBuilder
from reports.short_report_builder import ShortReportBuilder


class ReportBuilderTypeEnum(Enum):
    """
    Типы строителей отчетов.
    """
    FINISH = 1
    FULL = 2
    SHORT = 3


def run_report_builder(
        group_id: int,
        discipline_id: int,
        builder_type: ReportBuilderTypeEnum) -> str:
    """
    Функция запуска формирования файлового отчета.

    :param group_id: Идентификатор группы, по которой формируется отчет.
    :param discipline_id: Идентификатор дисциплины, по которой формируется отчет.
    :param builder_type: Тип формируемого отчета.

    :return: Путь до сформированного отчета.
    """
    report_builder: BaseReportBuilder | None = None  # Создание переменной для хранения экземпляра строителя отчета.

    # Определение типа строителя отчета с помощью конструкции "match".
    match builder_type:
        case ReportBuilderTypeEnum.FINISH:
            report_builder = FinishReportBuilder(group_id, discipline_id)
            # Инициализация строителя "FinishReportBuilder".
        case ReportBuilderTypeEnum.FULL:
            report_builder = FullReportBuilder(group_id, discipline_id)
        case ReportBuilderTypeEnum.SHORT:
            report_builder = ShortReportBuilder(group_id, discipline_id)

    report_builder.build_report()  # Запуск формирования отчета.
    report_builder.save_report()  # Сохранение отчета.
    return report_builder.get_path_to_report()  # Возврат пути к сформированному отчету.
