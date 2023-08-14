from pydantic import BaseModel


# хранение агрегированных данных о преподаватле с назначаемыми дисциплинами и группами студентов
class Teacher(BaseModel):
    full_name: str
    telegram_id: int
    is_admin: bool
    assign_disciplines: list[str]  # назначенные дисциплины
    assign_groups: list[str]  # назначенные группы
