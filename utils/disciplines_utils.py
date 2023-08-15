import json
from pydantic.json import pydantic_encoder
from model.pydantic.discipline_works import DisciplinesConfig, DisciplineWorksConfig


# Загружает конфигурации дисциплин из JSON-файла, и создает объект DisciplinesConfig.
def load_disciplines_config(file_path: str) -> DisciplinesConfig:
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return DisciplinesConfig(**data)


# Преобразует объект DisciplinesConfig в формат JSON с использованием pydantic_encoder.
def disciplines_config_to_json(data: DisciplinesConfig) -> str:
    return json.dumps(
        data,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ':'),
        default=pydantic_encoder
    )


# Создает объект DisciplinesConfig из JSON-данных.
def disciplines_config_from_json(json_data: str) -> DisciplinesConfig:
    data = json.loads(json_data)
    return DisciplinesConfig(**data)


# Преобразует объект DisciplineWorksConfig в формат JSON с использованием pydantic_encoder.
def disciplines_works_to_json(data: DisciplineWorksConfig) -> str:
    return json.dumps(
        data,
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ':'),
        default=pydantic_encoder
    )


# Загружает данные дисциплины из байтов и создает объект DisciplineWorksConfig.
def load_discipline(downloaded_data: bytes) -> DisciplineWorksConfig:
    data = json.loads(downloaded_data)
    return DisciplineWorksConfig(**data)


# Создает объект DisciplineWorksConfig из JSON-данных.
def disciplines_works_from_json(json_data: str) -> DisciplineWorksConfig:
    data = json.loads(json_data)
    return DisciplineWorksConfig(**data)


# Подсчитывает общее количество задач в рамках дисциплины.
def counting_tasks(discipline: DisciplineWorksConfig) -> int:
    result = 0
    for it in discipline.works:
        result += it.amount_tasks
    return result
