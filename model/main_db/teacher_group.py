from sqlalchemy import ForeignKey, Table, Column
from database.main_db.database import Base

# Определение таблицы-связи "association_teacher_to_group".
association_teacher_to_group = Table(
    "teacher_group",  # Имя таблицы в базе данных.
    Base.metadata,  # Использование метаданных базового класса.

    # Определение колонки 'teacher_id' с типом данных ForeignKey, внешний ключ к таблице 'teachers'.
    Column("teacher_id", ForeignKey("teachers.id", ondelete='CASCADE'), primary_key=True),

    # Определение колонки 'group_id' с типом данных ForeignKey, внешний ключ к таблице 'groups'.
    Column("group_id", ForeignKey("groups.id", ondelete='CASCADE'), primary_key=True),
)
