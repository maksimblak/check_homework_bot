import os
import shutil
from pathlib import Path
from zipfile import ZipFile


async def save_test_files(path_to_test: str, downloaded_file: bytes) -> None:
    """
    Функция распаковки архива тестов по дисциплине

    :param downloaded_file: сырое представление архива (набор байт)
    :param path_to_test: корневая директория загрузки тестов по выбранной студентом дисциплине

    :return: None
    """
    path = Path.cwd()
    path = Path(path.joinpath(path_to_test))

    # Проверка наличия файлов в директории и их удаление
    if os.listdir(path):
        for file_path in os.listdir(path):
            shutil.rmtree(file_path)

    # Сохранение загруженного архива
    with open(path.joinpath('archive.zip'), "wb") as new_file:
        new_file.write(downloaded_file)

    # Распаковка архива и извлечение файлов
    with ZipFile(path.joinpath('archive.zip')) as zipObj:
        zipObj.extractall(path=Path(path))
