import json
from pydantic.json import pydantic_encoder
from model.pydantic.discipline_works import DisciplineWorksConfig
from model.pydantic.home_work import DisciplineHomeWorks, HomeWork, HomeTask  #


# Функция для создания домашних заданий на основе конфигурации дисциплины.
def create_homeworks(discipline: DisciplineWorksConfig) -> DisciplineHomeWorks:
    home_works_list: list[HomeWork] = []  # Создание пустого списка для домашних работ.
    for it in discipline.works:  # Проход по списку работ в конфигурации дисциплины.
        home_tasks_list = [HomeTask(number=i) for i in range(1, it.amount_tasks + 1)]  # Создание списка домашних задач.
        home_work = HomeWork(number=it.number, deadline=it.deadline,
                             tasks=home_tasks_list)  # Создание объекта домашней работы.
        home_works_list.append(home_work)  # Добавление домашней работы в список.
    return DisciplineHomeWorks(home_works=home_works_list)  # Возвращение объекта с домашними работами.


# Функция для создания объекта DisciplineHomeWorks из JSON-данных.
def homeworks_from_json(json_data: str) -> DisciplineHomeWorks:
    data = json.loads(json_data)  # Разбор JSON-данных.
    return DisciplineHomeWorks(**data)  # Создание объекта DisciplineHomeWorks с использованием разобранных данных.


# Функция для преобразования объекта DisciplineHomeWorks в формат JSON с использованием pydantic_encoder.
def homeworks_to_json(data: DisciplineHomeWorks) -> str:
    return json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ':'),
                      default=pydantic_encoder)
