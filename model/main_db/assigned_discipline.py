from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.main_db.database import Base
from model.main_db.student import Student


class AssignedDiscipline(Base):
    # Определение имени таблицы в базе данных, соответствующей этой модели.
    __tablename__ = 'assigned_discipline'

    # Определение колонки 'id' с типом данных Integer, используется как первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Определение колонки 'discipline_id' с типом данных Integer, внешний ключ к таблице 'disciplines'.
    discipline_id: Mapped[int] = mapped_column(ForeignKey('disciplines.id'), nullable=False)

    # Определение колонки 'student_id' с типом данных Integer, внешний ключ к таблице 'students',
    # при удалении студента из базы, соответствующие записи будут удаляться (CASCADE).
    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False
    )

    # Определение колонки 'point' с типом данных Float, со значением по умолчанию 0.
    point: Mapped[float] = mapped_column(default=0)

    # Определение колонки 'home_work' с типом данных JSON, представляющей данные о домашних заданиях.
    home_work: Mapped[str] = mapped_column(JSON, nullable=False)  # DisciplineHomeWorks

    # Определение связи "многие-к-одному" с таблицей 'students' через атрибут 'student'.
    student: Mapped["Student"] = relationship(
        back_populates="homeworks"
    )

    # Метод __repr__ определяет строковое представление объекта AssignedDiscipline для отладки и вывода.
    def __repr__(self):
        info: str = f'Дисциплина {self.discipline_id}, ' \
                    f'student_id: {self.student_id}, ' \
                    f'points: {self.point},' \
                    f'home_works: {self.home_work}]'
        return info
