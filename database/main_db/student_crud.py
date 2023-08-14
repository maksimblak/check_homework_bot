from database.main_db.database import Session
from model.main_db.student import Student
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline


# Функция для проверки наличия студента по ФИО
def has_student(full_name: str) -> bool:
    with Session() as session:
        student = session.query(Student).filter(
            Student.full_name.ilike(f'%{full_name}%')
        ).first()
        return student is not None


# Функция для проверки, является ли пользователь студентом
def is_student(telegram_id: int) -> bool:
    with Session() as session:
        student = session.query(Student).filter(
            Student.telegram_id == telegram_id
        ).first()
        return student is not None


# Функция для установки телеграм идентификатора для студента
def set_telegram_id(full_name: str, telegram_id: int) -> None:
    with Session() as session:
        session.query(Student).filter(
            Student.full_name.ilike(f'%{full_name}%')
        ).update(
            {Student.telegram_id: telegram_id}, synchronize_session='fetch'
        )
        session.commit()


# Функция для получения студента по идентификатору телеграм
def get_student_by_tg_id(telegram_id: int):
    """
    Функция запроса студента по идентификатору телеграмма

    :param telegram_id: телеграм id студента

    :return: Студент
    """
    with Session() as session:
        student = (
            session.query(Student).filter(Student.telegram_id == telegram_id).first()
        )
        return student


# Функция для получения дисциплин, назначенных студенту
def get_assign_disciplines(student_tg_id: int) -> list[Discipline]:
    with Session() as session:
        student = session.query(Student).filter(
            Student.telegram_id == student_tg_id
        ).first()

        return student.group.disciplines
