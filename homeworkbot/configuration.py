import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage
from homeworkbot.filters import AddStudentCallbackFilter
from homeworkbot.filters import IsAdmin, IsStudent, IsTeacher
from distutils.util import strtobool
from homeworkbot.middlewares import BanMiddleware, StudentFloodMiddleware

# Загрузка переменных окружения из файла .env
load_dotenv()

# Инициализация бота с использованием токена из переменных окружения и хранилищем состояний
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), state_storage=StateMemoryStorage())

# Добавление пользовательских фильтров
# Фильтр, связанный с состоянием пользователя
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
# Пользовательские фильтры для определения роли пользователя: админ, студент, преподаватель
bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsStudent())
bot.add_custom_filter(IsTeacher())
# Пользовательский фильтр для обработки callback-запросов добавления студентов
bot.add_custom_filter(AddStudentCallbackFilter())

# Настройка middleware для блокировки забаненных пользователей
bot.setup_middleware(BanMiddleware(bot))

# Проверка использования middleware для ограничения действий студентов
if bool(strtobool(os.getenv("FLOOD_MIDDLEWARE"))):
    # Создание и настройка middleware для ограничения действий студентов
    bot.setup_middleware(
        StudentFloodMiddleware(
            bot,
            int(os.getenv("STUDENT_UPLOAD_LIMIT")),
            int(os.getenv("STUDENT_COMMAND_LIMIT"))
        )
    )
