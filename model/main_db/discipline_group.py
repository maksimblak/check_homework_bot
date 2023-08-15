from sqlalchemy import ForeignKey, Table, Column
from database.main_db.database import Base

# Определение таблицы-связи "association_discipline_to_group".
association_discipline_to_group = Table(
    "association_discipline_to_group",
    Base.metadata,

    # Определение колонки 'group_id' с типом данных ForeignKey, внешний ключ к таблице 'groups'.
    Column("group_id", ForeignKey("groups.id", ondelete='CASCADE'), primary_key=True),

    # Определение колонки 'discipline_id' с типом данных ForeignKey, внешний ключ к таблице 'disciplines'.
    Column("discipline_id", ForeignKey("disciplines.id", ondelete='CASCADE'), primary_key=True),
)
