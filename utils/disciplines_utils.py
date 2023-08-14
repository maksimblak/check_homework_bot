import json  # Импорт модуля json для работы с JSON-данными.
from pydantic.json import pydantic_encoder  # Импорт кодировщика pydantic_encoder из модуля pydantic.json.
from model.pydantic.discipline_works import DisciplinesConfig, DisciplineWorksConfig  # Импорт необходимых классов.


def load_disciplines_config(
        file_path: str) -> DisciplinesConfig:  # Функция для загрузки конфигураций дисциплин из JSON-файла и создания объекта DisciplinesConfig.
    with open(file_path, encoding='utf-8') as json_file:  # Открытие  json файла
        data = json.load(json_file)  # Загрузка JSON-данных из файла.
        return DisciplinesConfig(**data)  # Создание объекта DisciplinesConfig с использованием загруженных данных.


def disciplines_config_to_json(
        data: DisciplinesConfig) -> str:  # Функция для преобразования объекта DisciplinesConfig в формат JSON с использованием pydantic_encoder.
    return json.dumps(
        data,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ':'),
        default=pydantic_encoder
    )


def disciplines_config_from_json(
        json_data: str) -> DisciplinesConfig:  # Функция для создания объекта DisciplinesConfig из JSON-данных.
    data = json.loads(json_data)  # Разбор JSON-данных.
    return DisciplinesConfig(**data)  # Создание объекта DisciplinesConfig с использованием разобранных данных.


def disciplines_works_to_json(
        data: DisciplineWorksConfig) -> str:  # Функция для преобразования объекта DisciplineWorksConfig в формат JSON с использованием pydantic_encoder.
    return json.dumps(
        data,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ':'),
        default=pydantic_encoder
    )


# Функция для загрузки данных дисциплины из байтов и создания объекта DisciplineWorksConfig.
def load_discipline(downloaded_data: bytes) -> DisciplineWorksConfig:
    data = json.loads(downloaded_data)  # Разбор JSON-данных из байтов.
    return DisciplineWorksConfig(**data)  # Создание объекта DisciplineWorksConfig с использованием разобранных данных.


# Функция для создания объекта DisciplineWorksConfig из JSON-данных.
def disciplines_works_from_json(json_data: str) -> DisciplineWorksConfig:
    data = json.loads(json_data)  # Разбор JSON-данных.
    return DisciplineWorksConfig(**data)  # Создание объекта DisciplineWorksConfig с использованием разобранных данных.


# Функция для подсчета общего количества задач в рамках дисциплины.
def counting_tasks(discipline: DisciplineWorksConfig) -> int:
    result = 0
    for it in discipline.works:  # Проход по списку работ в дисциплине.
        result += it.amount_tasks  # Увеличение общего количества задач.
    return result  # Возвращение общего количества задач.
