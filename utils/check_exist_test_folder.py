import os
from pathlib import Path
from database.main_db import common_crud


# Функция, которая проверяет существование тестовой папки для определенной дисциплины и работы
def is_test_folder_exist(discipline_id: int, work_id: int) -> bool:
    # Получаем информацию о дисциплине с помощью функции get_discipline из модуля common_crud
    discipline = common_crud.get_discipline(discipline_id)

    # Создаем путь к папке с тестами с использованием текущей рабочей директории (cwd),
    # пути к тестам из информации о дисциплине и идентификатора работы
    test_folder_path = Path.cwd().joinpath(discipline.path_to_test).joinpath(str(work_id))

    # Проверяем, существует ли путь к папке с тестами
    # и возвращаем True, если путь существует, и False, если не существует
    return os.path.exists(test_folder_path)
