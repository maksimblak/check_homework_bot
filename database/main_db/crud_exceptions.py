# Исключение, вызываемое, если группа не найдена
class GroupNotFoundException(Exception):
    ...


# Исключение, вызываемое, если дисциплина не найдена
class DisciplineNotFoundException(Exception):
    ...


# Исключение, вызываемое, если студент не найден
class StudentNotFoundException(Exception):
    ...


# Исключение, вызываемое, если преподаватель не найден
class TeacherNotFoundException(Exception):
    ...


# Исключение, вызываемое, если группа уже существует
class GroupAlreadyExistException(Exception):
    ...


# Исключение, вызываемое, если дисциплина уже существует
class DisciplineAlreadyExistException(Exception):
    ...


# Исключение, вызываемое, если студент уже существует
class StudentAlreadyExistException(Exception):
    ...


# Исключение, вызываемое, если преподаватель уже существует
class TeacherAlreadyExistException(Exception):
    ...
