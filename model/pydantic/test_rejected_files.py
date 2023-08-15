from enum import IntEnum
from pydantic import BaseModel


# Класс RejectedType представляет перечисление для типов отклоненных файлов.
class RejectedType(IntEnum):
    TemplateError = 0  # Ошибка в шаблоне (неправильное название и т.д.)
    KeyWordsError = 1  # Ошибка в ключевых словах (запрещенные или отсутствующие ключевые слова и т.д.)


# Класс TestRejectedFiles представляет данные об отклоненных файлах в тестовой задаче.
class TestRejectedFiles(BaseModel):
    # Определение атрибута 'type' с типом данных RejectedType,
    # представляющего тип отклоненных файлов.
    type: RejectedType

    # Определение атрибута 'description' с типом данных str,
    # представляющего описание причины отклонения файлов.
    description: str

    # Определение атрибута 'files' с типом данных list[str],
    # представляющего список путей к отклоненным файлам.
    files: list[str]
