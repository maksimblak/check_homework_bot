from pathlib import Path  # Импорт модуля Path из стандартной библиотеки для работы с путями файловой системы.

from utils.disciplines_utils import *  # Импорт функций и классов из модуля disciplines_utils.
from utils.excel_parser import ExcelDataParser
from utils.homeworks_utils import *  # Импорт функций и классов из модуля homeworks_utils.
from model.pydantic.db_start_data import StudentRaw, TeacherRaw


# Класс для конфигурации первого запуска.
class FirstRunConfigurator:
    # Инициализация класса с путями к файлам дисциплин и Excel.
    def __init__(self, disciplines_path: str, excel_path: str):
        # Создание объекта ExcelDataParser для парсинга данных из Excel.
        excel_init_data = ExcelDataParser(excel_path)

        self.__disciplines = load_disciplines_config(disciplines_path)  # Загрузка конфигурации дисциплин из файла.
        self.__students = excel_init_data.students                      # Получение данных о студентах из Excel.
        self.__teachers = excel_init_data.teachers                      # Получение данных об учителях из Excel.
        self.__create_directory()                                       # Создание директорий для заданий.

    # Метод для создания директорий для дисциплин.
    def __create_directory(self):
        # Получение текущей директории
        path = Path.cwd()
        for it in self.__disciplines.disciplines:
            # Создание директории для тестовых файлов.
            Path(path.joinpath(it.path_to_test)).mkdir(parents=True, exist_ok=True)
            # Создание директории для ответов.
            Path(path.joinpath(it.path_to_answer)).mkdir(parents=True, exist_ok=True)

    # Метод для подсчета общего числа заданий по дисц-не.
    def counting_tasks(self, discipline: DisciplineWorksConfig) -> int:
        return counting_tasks(discipline)

    @property  # Свойство для доступа к списку дисциплин.
    def disciplines(self) -> list[DisciplineWorksConfig]:
        return self.__disciplines.disciplines  # список для конфигурации дисциплин

    @property  # Свойство для доступа к данным о студентах.
    def students_config(self) -> dict[str, dict[str, list[StudentRaw]]]:
        return self.__students  # список для конфигурации студентов

    @property  # Свойство для доступа к данным об учителях.
    def teachers_config(self) -> dict[str, dict[str, list[TeacherRaw]]]:
        return self.__teachers

    # Метод для создания пустого JSON-файла для домашних заданий по конкретной дисциплине.
    def create_empty_homework_json(self, discipline_short_name: str) -> str:
        discipline = None
        for it in self.disciplines:
            if it.short_name == discipline_short_name:
                discipline = it

        if discipline is None:
            raise Exception(f'Discipline with short name "{discipline_short_name}" not found')

        empty_homework = create_homeworks(discipline)  # Создание пустых домашних заданий для дисциплины.
        return homeworks_to_json(empty_homework)  # Преобразование домашних заданий в JSON-формат.

    # Метод для преобразования конфигурации дисциплин в JSON-формат.
    def disciplines_works_to_json(self, discipline: DisciplineWorksConfig) -> str:
        return disciplines_works_to_json(discipline)
