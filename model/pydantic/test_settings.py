from pydantic import BaseModel


# Класс TestLocalSettings представляет локальные политики конкретной задачи.
class TestLocalSettings(BaseModel):
    """
    Локальные политики конкретной задачи
    """
    # Определение атрибута 'lab_number' с типом данных int,
    # представляющего номер лабораторной (домашней) работы.
    lab_number: int

    # Определение атрибута 'prohibition' с типом данных list[str] | None,
    # представляющего список запрещенных импортов или None, если запрещений нет.
    prohibition: list[str] | None

    # Определение атрибута 'restriction' с типом данных list[str] | None,
    # представляющего список ограниченных импортов или None, если ограничений нет.
    restriction: list[str] | None

    # Определение атрибута 'resolve_import' с типом данных list[str] | None,
    # представляющего список разрешенных импортов или None, если разрешений нет.
    resolve_import: list[str] | None


# Класс TestGlobalSettings представляет глобальные политики всей лабораторной (домашней) работы.
class TestGlobalSettings(BaseModel):
    """
    Глобальные политики всей лабораторной (домашней) работы
    """
    # Определение атрибута 'prohibition' с типом данных list[str] | None,
    # представляющего список запрещенных импортов или None, если запрещений нет.
    prohibition: list[str] | None

    # Определение атрибута 'restriction' с типом данных list[str] | None,
    # представляющего список ограниченных импортов или None, если ограничений нет.
    restriction: list[str] | None


# Класс TestSettings представляет агрегацию политик лабораторной (домашней) работы
# с зависимостями от внешних пакетов.
class TestSettings(BaseModel):
    """
    Агрегация политик лабораторной (домашней) работы
    с зависимостями от внешних пакетов
    """
    # Определение атрибута 'dependencies' с типом данных list[str] | None,
    # представляющего список зависимостей от внешних пакетов или None, если зависимостей нет.
    dependencies: list[str] | None

    # Определение атрибута 'global_level' с типом данных TestGlobalSettings,
    # представляющего глобальные политики всей лабораторной (домашней) работы.
    global_level: TestGlobalSettings

    # Определение атрибута 'local_level' с типом данных list[TestLocalSettings],
    # представляющего список локальных политик конкретных задач.
    local_level: list[TestLocalSettings]
