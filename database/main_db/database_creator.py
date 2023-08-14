from database.main_db.first_run_configurator import FirstRunConfigurator
from model.pydantic.db_creator_settings import DbCreatorSettings
from model.main_db.group import Group
from model.main_db.student import Student
from model.main_db.teacher import Teacher
from model.main_db.discipline import Discipline
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.teacher_discipline import association_teacher_to_discipline
from model.main_db.teacher_group import association_teacher_to_group
from model.main_db.discipline_group import association_discipline_to_group
from model.main_db.admin import Admin
from model.main_db.chat import Chat
from model.main_db.student_ban import StudentBan

from database.main_db.database import create_tables, Session


# Функция для создания основных таблиц в базе данных
def create_main_tables(settings: DbCreatorSettings) -> None:
    create_tables()  # Создание таблиц

    if not settings.remote_configuration:
        fill_db_from_files(
            settings.disciplines_path,
            settings.excel_data_path
        )
    else:
        session = Session()
        # Добавление администратора в случае удаленной конфигурации
        session.add(Admin(telegram_id=settings.default_admin))
        session.commit()
        session.close()


# Функция для заполнения базы данных данными из файлов
def fill_db_from_files(disciplines_path: str, excel_data_path: str) -> None:
    """
    Функция для заполнения основной БД при локальной конфигурации

    :param disciplines_path: путь до файла с конфигурацией дисциплин
    :param excel_data_path: путь до файла с данными о преподавателях и студентах

    :return: None
    """
    configurator = FirstRunConfigurator(disciplines_path, excel_data_path)
    disciplines: dict[str, Discipline] = {}
    groups: dict[str, Group] = {}

    session = Session()
    start_disciplines = configurator.disciplines
    for it in start_disciplines:
        # Создание объектов Discipline на основе конфигурации
        disciplines[it.short_name] = Discipline(
            full_name=it.full_name,
            short_name=it.short_name,
            path_to_test=it.path_to_test,
            path_to_answer=it.path_to_answer,
            language=it.language,
            max_tasks=configurator.counting_tasks(it),
            works=configurator.disciplines_works_to_json(it),
            max_home_works=len(it.works)
        )

    temp_students: dict[str, list[Student]] = {}
    for it in configurator.students_config:
        for group_name, students_raw_list in configurator.students_config[it].items():
            temp_students[it] = [
                Student(full_name=it.full_name) for it in students_raw_list
            ]

            groups[group_name] = Group(
                group_name=group_name,
                students=temp_students[it]
            )
            disciplines[it].groups.append(groups[group_name])

    for dis, teacher_group in configurator.teachers_config.items():
        for group_name, teachers_raw_list in teacher_group.items():

            for teachers_raw in teachers_raw_list:
                teacher = Teacher(
                    full_name=teachers_raw.full_name,
                    telegram_id=teachers_raw.telegram_id,
                )
                teacher.groups.append(groups[group_name])
                disciplines[dis].teachers.append(teacher)

                if teachers_raw.is_admin:
                    session.add(Admin(telegram_id=teachers_raw.telegram_id))

    session.add_all(disciplines.values())
    session.flush()
    for dis, student_list in temp_students.items():
        for student in student_list:
            # Заполнение домашних заданий для студентов
            student.homeworks.append(
                AssignedDiscipline(
                    discipline_id=disciplines[dis].id,
                    home_work=configurator.create_empty_homework_json(dis)
                )
            )

    session.commit()
    session.close()
