from enum import Enum
from database.main_db.database import Session
from model.main_db.chat import Chat
from model.main_db.admin import Admin
from model.main_db.teacher import Teacher
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.student import Student
from database.main_db import admin_crud
from model.main_db.group import Group
from model.main_db.student_ban import StudentBan
import json
from datetime import datetime
import utils.homeworks_utils as utils
from model.main_db.teacher_group import association_teacher_to_group
from model.pydantic.queue_in_raw import QueueInRaw
from model.queue_db.queue_in import QueueIn
from testing_tools.logger.report_model import LabReport
from sqlalchemy import exists, and_, select, delete


# Определение перечисления UserEnum, которое содержит роли пользователей системы.

class UserEnum(Enum):
    Admin = 0
    Teacher = 1
    Student = 2
    Unknown = 3


# функция проверяет роль пользователя (администратор, преподаватель, студент) по его telegram_id.
def user_verification(telegram_id: int) -> UserEnum:
    with Session() as session:
        user = session.query(Admin).get(telegram_id)
        if user is not None:
            return UserEnum.Admin
        user = session.query(Teacher).filter(
            Teacher.telegram_id == telegram_id
        ).first()
        if user is not None:
            return UserEnum.Teacher
        user = session.query(Student).filter(
            Student.telegram_id == telegram_id
        ).first()
        if user is not None:
            return UserEnum.Student
    return UserEnum.Unknown


# функция возвращает список всех зарегистрированных чатов в системе.
def get_chats() -> list[int]:
    with Session() as session:
        chats = session.query(Chat).all()
        return [it.chat_id for it in chats]


# функция возвращает список дисциплин, привязанных к определенной группе.
def get_group_disciplines(group_id: int) -> list[Discipline]:
    with Session() as session:
        group = session.get(Group, group_id)
        return group.disciplines


# функция добавляет идентификатор студента в бан-лист.
def ban_student(telegram_id: int) -> None:
    """
    Функция для записи идентификатора студента в бан-лист

    :param telegram_id: телеграм id студента

    :return: None
    """
    with Session() as session:
        session.add(StudentBan(telegram_id=telegram_id))
        session.commit()


# функция удаляет идентификатор студента из бан-листа.
def unban_student(telegram_id: int) -> None:
    with Session() as session:
        smt = delete(StudentBan).where(StudentBan.telegram_id == telegram_id)
        session.execute(smt)
        session.commit()


# функция проверяет, находится ли студент в бан-листе.
def is_ban(telegram_id: int) -> bool:
    """
    Функция проверки нахождения студента в бан-листе

    :param telegram_id: телеграм id студента

    :return: True, если студент забанен, иначе False
    """
    with Session() as session:
        tg_id = session.query(StudentBan).get(telegram_id)
        return tg_id is not None


# функция возвращает список забаненных студентов, в зависимости от роли преподавателя.
def get_ban_students(teacher_telegram_id: int) -> list[Student]:
    with Session() as session:
        if admin_crud.is_admin_no_teacher_mode(teacher_telegram_id):
            smt = select(Student).where(
                exists().where(StudentBan.telegram_id == Student.telegram_id)
            )
            return session.scalars(smt).all()
        else:
            smt = select(Student).where(
                exists().where(StudentBan.telegram_id == Student.telegram_id)
            ).join(
                Group,
                Student.group_id == Group.id
            ).join(
                association_teacher_to_group,
                association_teacher_to_group.c.group_id == Group.id
            ).join(
                Teacher,
                association_teacher_to_group.c.teacher_id == Teacher.id
            ).where(
                Teacher.telegram_id == teacher_telegram_id
            )
            return session.scalars(smt).all()


# функция возвращает список студентов определенной группы, которые не находятся в бан-листе.
def get_students_from_group_for_ban(group_id: int) -> list[Student]:
    with Session() as session:
        students = session.query(Student).filter(
            and_(
                Student.group_id == group_id,
                Student.telegram_id.is_not(None),
                ~exists().where(StudentBan.telegram_id == Student.telegram_id)
            )
        ).all()
        return students


# функция возвращает список студентов из определенной группы.
def get_students_from_group(group_id) -> list[Student]:
    """
    Функция запроса списка студентов из конкретной группы

    :param group_id: идентификатор группы

    :return: список студентов
    """
    with Session() as session:
        students = session.query(Student).filter(
            Student.group_id == group_id
        ).all()
        return students


# функция возвращает информацию о группе по её идентификатору.
def get_group(group_id: int) -> Group:
    with Session() as session:
        return session.query(Group).get(group_id)


# функция возвращает информацию о дисциплине по её идентификатору.
def get_discipline(discipline_id: int) -> Discipline:
    with Session() as session:
        return session.query(Discipline).get(discipline_id)


# функция возвращает информацию о назначенной дисциплине для студента.
def get_student_discipline_answer(student_id: int, discipline_id: int) -> AssignedDiscipline:
    with Session() as session:
        answers = session.query(AssignedDiscipline).filter(
            AssignedDiscipline.student_id == student_id,
            AssignedDiscipline.discipline_id == discipline_id
        ).first()
        return answers


# функция возвращает информацию о студенте по его идентификатору.
def get_student_from_id(student_id: int) -> Student:
    with Session() as session:
        return session.query(Student).get(student_id)


# функция записывает результаты тестирования заданий из лабораторной работы или домашней работы.
def write_test_result(lab_report: LabReport, input_record: QueueIn) -> None:
    """
    Функция записи результата тестирования заданий из л/р или домашка с
    расчетом заработанных балов по выполнению работы. Если успевает до дедлайнов,
    то все норм. Иначе баллы срезаются в 2 раза.

    :param lab_report: Отчет по результатам тестирования заданий работы
    :param input_record: исходные данные, отправляемые на тестирование

    :return: None
    """
    session = Session()
    task_raw = QueueInRaw(**json.loads(input_record.data))

    student = session.query(Student).filter(
        Student.telegram_id == input_record.telegram_id
    ).first()

    assig_discipline = session.query(AssignedDiscipline).filter(
        AssignedDiscipline.student_id == student.id,
        AssignedDiscipline.discipline_id == task_raw.discipline_id
    ).first()

    hwork = utils.homeworks_from_json(assig_discipline.home_work)

    lab = None
    for it in hwork.home_works:
        if lab_report.lab_id == it.number:
            lab = it
            break

    task_done = 0
    for task in lab.tasks:
        task_done += 1 if task.is_done else 0
        for task_result in lab_report.tasks:
            if task.number == task_result.task_id:
                task.amount_tries += 1
                task.last_try_time = task_result.time
                if not task.is_done and task_result.status:
                    task.is_done = True
                    task_done += 1

    lab.tasks_completed = task_done

    too_slow = False
    if (task_done == len(lab.tasks)) and not lab.is_done:
        end_time = datetime.now()
        lab.end_time = end_time
        lab.is_done = True
        if lab.deadline < end_time.date():
            too_slow = True

        discipline = session.query(Discipline).get(assig_discipline.discipline_id)

        scale_point = 100.0 / discipline.max_tasks
        lab_points = (task_done * scale_point)
        if too_slow:
            lab_points *= 0.5

        assig_discipline.point += lab_points

    assig_discipline.home_work = utils.homeworks_to_json(hwork)
    session.commit()
    session.close()
