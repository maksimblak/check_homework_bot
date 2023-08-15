from pydantic import BaseModel


# Класс QueueInRaw представляет входные данные для очереди заданий.
class QueueInRaw(BaseModel):
    # Определение атрибута 'discipline_id' с типом данных int, представляющего идентификатор дисциплины.
    discipline_id: int

    # Определение атрибута 'lab_number' с типом данных int, представляющего номер лабораторной работы.
    lab_number: int

    # Определение атрибута 'files_path' с типом данных list[str], представляющего пути к файлам.
    files_path: list[str]
