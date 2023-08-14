from sqlalchemy import and_, select
from database.main_db.database import Session
from model.main_db.admin import Admin
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.group import Group
from model.main_db.student import Student
from model.main_db.teacher import Teacher


# Функция для проверки, является ли пользователь преподавателем
def is_teacher(telegram_id: int) -> bool:
    with Session() as session:
        teacher = session.query(Teacher).filter(
            Teacher.telegram_id == telegram_id
        ).first()
        return teacher is not None


# Функция для получения дисциплин, связанных с преподавателем в определенной группе
def get_assign_group_discipline(teacher_tg_id: int, group_id: int) -> list[Discipline]:
    """
    Функция запроса списка дисциплин, которые числятся за преподавателем у конкретной группы

    :param teacher_tg_id: телеграм идентификатор преподавателя
    :param group_id: идентификатор группы

    :return: список дисциплин
    """
    with Session() as session:
        teacher = session.query(Teacher).filter(
            Teacher.telegram_id == teacher_tg_id
        ).first()

        teacher_set = {it.short_name for it in teacher.disciplines}

        group = session.query(Group).filter(
            Group.id == group_id
        ).first()

        group_set = {it.short_name for it in group.disciplines}

        return [it for it in teacher.disciplines
                if it.short_name in teacher_set.intersection(group_set)]


# Функция для переключения режима преподавателя на режим администратора
def switch_teacher_mode_to_admin(teacher_tg_id: int) -> None:
    with Session() as session:
        session.query(Admin).filter(
            Admin.telegram_id == teacher_tg_id
        ).update(
            {'teacher_mode': False}
        )
        session.commit()


# Функция для получения групп, связанных с преподавателем
def get_assign_groups(teacher_tg_id: int) -> list[Group]:
    """
    Функция запроса списка групп, у которых ведет предметы преподаватель

    :param teacher_tg_id: телеграм идентификатор преподавателя

    :return: список групп
    """
    with Session() as session:
        smt = select(Teacher).where(Teacher.telegram_id == teacher_tg_id)
        teacher = session.scalars(smt).first()
        return teacher.groups


# Функция для получения дисциплин, связанных с преподавателем
def get_teacher_disciplines(teacher_tg_id: int) -> list[Discipline]:
    """
    Функция запроса списка дисциплин, которые числятся за преподавателем

    :param teacher_tg_id: телеграм идентификатор преподавателя

    :return: список дисциплин
    """
    with Session() as session:
        smt = select(Teacher).where(Teacher.telegram_id == teacher_tg_id)
        teacher = session.scalars(smt).first()
        return teacher.disciplines


# Функция для получения студентов, имеющих авторизацию по определенной группе
def get_auth_students(group_id: int) -> list[Student]:
    with Session() as session:
        students = session.query(Student).filter(
            and_(
                Student.group_id == group_id,
                Student.telegram_id.is_not(None),
            )
        ).all()
        return students
