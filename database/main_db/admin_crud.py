import os

from database.main_db.database import Session
from database.main_db.teacher_crud import is_teacher
from model.main_db.chat import Chat
from model.main_db.admin import Admin
from model.main_db.teacher import Teacher
from model.main_db.group import Group
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.student import Student
from utils.homeworks_utils import create_homeworks, homeworks_to_json
from model.pydantic.discipline_works import DisciplineWorksConfig
from utils.disciplines_utils import disciplines_works_from_json, disciplines_works_to_json, counting_tasks
from sqlalchemy.exc import IntegrityError
from model.pydantic.students_group import StudentsGroup
from database.main_db.crud_exceptions import DisciplineNotFoundException, GroupAlreadyExistException, \
    DisciplineAlreadyExistException, GroupNotFoundException
from model.pydantic.db_start_data import DbStartData
from sqlalchemy import delete, select


def is_admin_no_teacher_mode(telegram_id: int) -> bool:
    with Session() as session:  # Создание контекста сессии работы с базой данных.
        admin = session.query(Admin).get(telegram_id)  # Запрос к базе данных для получения объекта Admin по telegram_id
        if admin is None:  # Проверка, найден ли администратор.
            return False  # Возвращение False, если администратор не найден.
        return not admin.teacher_mode


# функция проверяет, является ли администратор активированным преподавателем.
def is_admin_with_teacher_mode(telegram_id: int) -> bool:
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        if admin is None:
            return False
        return admin.teacher_mode


# функция проверяет, является ли пользователь администратором.
def is_admin(telegram_id: int) -> bool:
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        return admin is not None


# Функция для проверки, является ли администратор активированным преподавателем
def is_admin_and_teacher(telegram_id: int) -> bool:
    _is_admin = is_admin(telegram_id)
    _is_teacher = is_teacher(telegram_id)
    return _is_admin and _is_teacher


# Эта функция добавляет чат в базу данных.
def add_chat(chat_id: int) -> None:
    with Session() as session:
        session.add(Chat(chat_id=chat_id))
        session.commit()


# функция добавляет преподавателя в базу данных.
def add_teacher(full_name: str, tg_id: int) -> None:
    """
    Функция добавления преподавателя

    :param full_name: ФИО препода
    :param tg_id: идентификатор препода в телегераме

    :return: None
    """
    with Session() as session:
        session.add(Teacher(full_name=full_name, telegram_id=tg_id))
        session.commit()


# функция возвращает список всех преподавателей из базы данных.
def get_teachers() -> list[Teacher]:
    with Session() as session:
        return session.query(Teacher).all()


# функция возвращает список групп, которые ещё не назначены данному преподавателю.
def get_not_assign_teacher_groups(teacher_id: int) -> list[Group]:
    with Session() as session:
        teacher = session.get(Teacher, teacher_id)
        assign_group = [it.id for it in teacher.groups]
        smt = select(Group).where(
            Group.id.not_in(assign_group)
        )
        return session.scalars(smt).all()


# функция назначает преподавателя к группе в базе данных.
def assign_teacher_to_group(teacher_id: int, group_id: int) -> None:
    with Session() as session:
        teacher = session.get(Teacher, teacher_id)
        teacher.groups.append(
            session.get(Group, group_id)
        )
        session.commit()


#  функция возвращает список всех групп из базы данных.
def get_all_groups() -> list[Group]:
    with Session() as session:
        return session.query(Group).all()


# функция добавляет студента в базу данных и назначает ему домашние задания по дисциплинам группы.
def add_student(full_name: str, group_id: int):
    session = Session()
    group: Group = session.get(Group, group_id)

    student = Student(
        full_name=full_name,
        group_id=group_id,
    )
    group.students.append(student)
    for discipline in group.disciplines:
        empty_homework = create_homeworks(
            disciplines_works_from_json(discipline.works)
        )

        student.homeworks.append(
            AssignedDiscipline(
                discipline_id=discipline.id,
                home_work=homeworks_to_json(empty_homework)
            )
        )
    session.commit()
    session.close()


# функция добавляет дисциплину в базу данных.
def add_discipline(discipline: DisciplineWorksConfig) -> None:
    with Session() as session:
        session.add(
            Discipline(
                full_name=discipline.full_name,
                short_name=discipline.short_name,
                path_to_test=discipline.path_to_test,
                path_to_answer=discipline.path_to_answer,
                works=disciplines_works_to_json(discipline),
                language=discipline.language,
                max_tasks=counting_tasks(discipline),
                max_home_works=len(discipline.works)
            )
        )
        session.commit()


# функция добавляет группы студентов в базу данных, а также назначает им дисциплины и домашние задания.
def add_students_group(student_groups: list[StudentsGroup]) -> None:
    session = Session()
    session.begin()
    try:
        for it in student_groups:
            group = Group(
                group_name=it.group_name,
                students=[Student(full_name=student_raw) for student_raw in it.students]
            )

            for discipline in it.disciplines_short_name:
                smt = select(Discipline).where(
                    Discipline.short_name.ilike(f"%{discipline}%")
                )
                current_discipline = session.scalars(smt).first()
                if current_discipline is None:
                    raise DisciplineNotFoundException(f'{discipline} нет в БД')

                group.disciplines.append(current_discipline)
                empty_homework = create_homeworks(
                    disciplines_works_from_json(current_discipline.works)
                )
                for student in group.students:
                    student.homeworks.append(
                        AssignedDiscipline(
                            discipline_id=current_discipline.id,
                            home_work=homeworks_to_json(empty_homework)
                        )
                    )
            session.add(group)
        session.commit()
    except DisciplineNotFoundException as ex:
        session.rollback()
        raise ex
    except IntegrityError as ex:
        session.rollback()
        raise GroupAlreadyExistException(f'{ex.params[0]} уже существует')
    finally:
        session.close()


# функция назначает преподавателя к дисциплине в базе данных.
def assign_teacher_to_discipline(teacher_id: int, discipline_id: int) -> None:
    with Session() as session:
        teacher = session.get(Teacher, teacher_id)
        teacher.disciplines.append(
            session.get(Discipline, discipline_id)
        )
        session.commit()


# функция возвращает список дисциплин, которые ещё не назначены данному преподавателю.
def get_not_assign_teacher_discipline(teacher_id: int) -> list[Discipline]:
    with Session() as session:
        teacher = session.get(Teacher, teacher_id)
        assign_discipline = [it.id for it in teacher.disciplines]
        smt = select(Discipline).where(
            Discipline.id.not_in(assign_discipline)
        )
        return session.scalars(smt).all()


# функция удаляет группу из базы данных.
def delete_group(group_id: int) -> None:
    with Session() as session:
        smt = delete(Group).where(Group.id == group_id)
        session.execute(smt)
        session.commit()


# функция удаляет студента из базы данных.
def delete_student(student_id: int) -> None:
    with Session() as session:
        smt = delete(Student).where(Student.id == student_id)
        session.execute(smt)
        session.commit()


# функция удаляет преподавателя из базы данных.
def delete_teacher(teacher_id: int) -> None:
    with Session() as session:
        smt = delete(Teacher).where(Teacher.id == teacher_id)
        session.execute(smt)
        session.commit()


# функция возвращает список всех дисциплин из базы данных.
def get_all_disciplines() -> list[Discipline]:
    with Session() as session:
        return session.query(Discipline).all()


# функция возвращает дисциплину по её идентификатору из базы данных.
def get_discipline(discipline_id: int) -> Discipline:
    with Session() as session:
        return session.query(Discipline).get(discipline_id)


# функция заполняет базу данных начальными данными из предоставленного JSON-файла.
def remote_start_db_fill(data: DbStartData) -> None:
    """
    Функция для стартовой конфигурации системы через загрузку json-файла

    :param data: данные по предметам, студентам, группам и преподавателям, а также
    какие дисциплины кому назначены и какой преподаватель их ведет

    :raises DisciplineNotFoundException: дисциплина не найдена
    :raises DisciplineAlreadyExistException: дисциплина уже существует (дублируется)
    :raises GroupAlreadyExistException: если группа с таким названием уже существует
    :raises GroupNotFoundException: если группа с таким названием не найдена

    :return: None
    """
    session = Session()
    session.begin()
    admin_default_tg = int(os.getenv("DEFAULT_ADMIN"))
    disciplines: dict[str, Discipline] = {}
    groups: dict[str, Group] = {}

    try:
        for discipline in data.disciplines:
            if discipline.short_name in disciplines:
                raise DisciplineAlreadyExistException(f"{discipline.short_name} дублируется")
            dis = Discipline(
                full_name=discipline.full_name,
                short_name=discipline.short_name,
                path_to_test=discipline.path_to_test,
                path_to_answer=discipline.path_to_answer,
                works=disciplines_works_to_json(discipline),
                language=discipline.language,
                max_tasks=counting_tasks(discipline),
                max_home_works=len(discipline.works)
            )
            disciplines[discipline.short_name] = dis

        session.add_all(disciplines.values())
        session.flush()

        for it in data.groups:
            group = Group(
                group_name=it.group_name,
                students=[
                    Student(full_name=student_raw)
                    for student_raw in it.students
                ]
            )
            groups[it.group_name] = group

            for name in it.disciplines_short_name:
                if name not in disciplines:
                    raise DisciplineNotFoundException(f'{name} нет в БД')

                empty_homework = create_homeworks(
                    disciplines_works_from_json(disciplines[name].works)
                )
                disciplines[name].groups.append(
                    groups[it.group_name]
                )

                for student in groups[it.group_name].students:
                    student.homeworks.append(
                        AssignedDiscipline(
                            discipline_id=disciplines[name].id,
                            home_work=homeworks_to_json(empty_homework)
                        )
                    )

        for it in data.teachers:
            teacher = Teacher(
                full_name=it.full_name,
                telegram_id=it.telegram_id
            )

            for tgr in it.assign_groups:
                if tgr not in groups:
                    raise GroupNotFoundException(f'Группа {tgr} не найдена')
                teacher.groups.append(groups[tgr])

            for tdis in it.assign_disciplines:
                if tdis not in disciplines:
                    raise DisciplineNotFoundException(f'Дисциплина {tdis} не найдена')
                teacher.disciplines.append(disciplines[tdis])

            if it.is_admin and teacher.telegram_id != admin_default_tg:
                session.add(
                    Admin(
                        telegram_id=teacher.telegram_id
                    )
                )
            session.add(teacher)

        for chat in data.chats:
            session.add(
                Chat(chat_id=chat)
            )
        session.commit()
    except DisciplineNotFoundException as ex:
        session.rollback()
        raise ex
    except DisciplineAlreadyExistException as daex:
        session.rollback()
        raise daex
    except GroupNotFoundException as gnfex:
        session.rollback()
        raise gnfex
    except IntegrityError as ex:
        session.rollback()
        raise GroupAlreadyExistException(f'{ex.params[0]} уже существует')
    finally:
        session.close()


# функция переключает режим администратора на режим преподавателя в базе данных.
def switch_admin_mode_to_teacher(admin_id: int) -> None:
    with Session() as session:
        admin = session.get(Admin, admin_id)
        admin.teacher_mode = True
        session.commit()
