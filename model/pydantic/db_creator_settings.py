from dataclasses import dataclass


@dataclass
class DbCreatorSettings:
    remote_configuration: bool  # Флаг удаленной конфигурации
    default_admin: int | None = None  # Идентификатор администратора по умолчанию или None по умолчанию
    disciplines_path: str = ''  # Путь к данным о дисциплинах (по умолчанию - пустая строка)
    excel_data_path: str = ''  # Путь к данным Excel (по умолчанию - пустая строка)
