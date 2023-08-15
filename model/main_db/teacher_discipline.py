from sqlalchemy import ForeignKey, Table, Column
from database.main_db.database import Base

# Определение таблицы-связи "association_teacher_to_discipline".
association_teacher_to_discipline = Table(
    "teacher_discipline",  # Имя таблицы в базе данных.
    Base.metadata,  # Использование метаданных базового класса.

    # Определение колонки 'teacher_id' с типом данных ForeignKey, внешний ключ к таблице 'teachers'.
    Column("teacher_id", ForeignKey("teachers.id", ondelete='CASCADE'), primary_key=True),

    # Определение колонки 'discipline_id' с типом данных ForeignKey, внешний ключ к таблице 'disciplines'.
    Column("discipline_id", ForeignKey("disciplines.id", ondelete='CASCADE'), primary_key=True),
)
