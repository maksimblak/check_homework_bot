import json
from pathlib import Path

from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import Message

from database.main_db.crud_exceptions import DisciplineNotFoundException, GroupAlreadyExistException, \
    DisciplineAlreadyExistException, GroupNotFoundException
from homeworkbot.admin_handlers.utils import start_upload_file_message, finish_upload_file_message
from homeworkbot.configuration import bot
from database.main_db import admin_crud
from model.pydantic.db_start_data import DbStartData


class AdminStates(StatesGroup):
    upload_config = State()


# Обработчик команды на начальную загрузку данных конфигурации
@bot.message_handler(is_admin=True, commands=['upconfig'])
async def handle_upload_start_configuration(message: Message):
    await _handle_upload_start_configuration(message)


# Обработчик команды на начальную загрузку данных конфигурации для недостаточно привилегированных пользователей
@bot.message_handler(is_admin=False, commands=['upconfig'])
async def handle_no_upload_start_configuration(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Функция для обработки начала загрузки данных конфигурации
async def _handle_upload_start_configuration(message: Message):
    await bot.send_message(message.chat.id, "Загрузите json-файл для наполнения БД")
    await bot.set_state(message.from_user.id, AdminStates.upload_config, message.chat.id)


# Обработчик загрузки файла данных конфигурации
@bot.message_handler(state=AdminStates.upload_config, content_types=["document"])
async def handle_upload_discipline(message: Message):
    result_message = await start_upload_file_message(message)
    file_name = message.document.file_name
    if file_name[-4:] == "json":
        try:
            file_info = await bot.get_file(message.document.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            data = json.loads(downloaded_file)
            db_start_data = DbStartData(**data)

            admin_crud.remote_start_db_fill(db_start_data)
            path = Path.cwd()
            for discipline in db_start_data.disciplines:
                Path(path.joinpath(discipline.path_to_test)).mkdir(parents=True, exist_ok=True)
                Path(path.joinpath(discipline.path_to_answer)).mkdir(parents=True, exist_ok=True)
            await finish_upload_file_message(
                message,
                result_message,
                f'<i>Стартовое заполнение БД завершено!</i>'
            )
            await bot.delete_state(message.from_user.id, message.chat.id)
        except DisciplineNotFoundException as dnf_ex:
            await bot.reply_to(message, dnf_ex)
        except GroupAlreadyExistException as gae_ex:
            await bot.reply_to(message, gae_ex)
        except DisciplineAlreadyExistException as daex:
            await bot.reply_to(message, daex)
        except GroupNotFoundException as gnfex:
            await bot.reply_to(message, gnfex)
    else:
        await bot.reply_to(message, "Неверный тип файла")
