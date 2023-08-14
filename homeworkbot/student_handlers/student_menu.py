from enum import Enum, auto
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
from homeworkbot import bot
from homeworkbot.student_handlers.utils import create_student_disciplines_button


# Исключение, специфичное для студента
class StudentException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"StudentException: {self.message}"


# Перечисление для команд студента
class StudentCommand(Enum):
    UPLOAD_ANSWER = auto()
    NEAREST_DEADLINE = auto
    ACADEMIC_PERFORMANCE = auto()


# Словарь с командами студента
__student_commands = {
    StudentCommand.UPLOAD_ANSWER: "Загрузить ответ",
    StudentCommand.NEAREST_DEADLINE: "Ближайший дедлайн",
    StudentCommand.ACADEMIC_PERFORMANCE: "Успеваемость",
}


# Создание клавиатуры для студента
def student_keyboard(message: Message | None = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(__student_commands[StudentCommand.UPLOAD_ANSWER]),
    )
    markup.add(
        KeyboardButton(__student_commands[StudentCommand.NEAREST_DEADLINE]),
        KeyboardButton(__student_commands[StudentCommand.ACADEMIC_PERFORMANCE]),
    )
    return markup


# Обработчик команд студента
@bot.message_handler(
    is_student=True, func=lambda message: is_student_command(message.text)
)
async def handle_commands(message: Message):
    command = get_current_student_command(message.text)
    match command:
        case StudentCommand.UPLOAD_ANSWER:
            await create_student_disciplines_button(message, 'uploadAnswer_0')
        case StudentCommand.NEAREST_DEADLINE:
            await create_student_disciplines_button(message, 'nearestDeadline')
        case StudentCommand.ACADEMIC_PERFORMANCE:
            await create_student_disciplines_button(message, 'academicPerf')


# Проверка, является ли сообщение командой студента
def is_student_command(command: str) -> bool:
    for key, value in __student_commands.items():
        if value == command:
            return True
    return False


# Получение текущей команды студента из текста сообщения
def get_current_student_command(command: str) -> StudentCommand:
    for key, value in __student_commands.items():
        if value == command:
            return key
    raise StudentException("Неизвестная команда")
