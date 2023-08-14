import asyncio
import os
import pathlib
import shutil
from datetime import datetime

from telebot.types import Message, InputFile

from homeworkbot.configuration import bot


# Обработчик команды на скачивание всех данных по ответам и тестам
@bot.message_handler(is_admin=True, commands=['dowall'])
async def handle_download_all_test_and_answer(message: Message):
    await _handle_download_all_test_and_answer(message)


# Обработчик команды на скачивание всех данных по ответам и тестам для недостаточно привилегированных пользователей
@bot.message_handler(is_admin=False, commands=['dowall'])
async def handle_no_download_all_test_and_answer(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Функция для скачивания всех данных по ответам и тестам
async def _handle_download_all_test_and_answer(message: Message):
    await bot.send_message(
        message.chat.id,
        "Начинаем формировать отчет")

    # Вызов функции для асинхронного создания архива
    path_to_archive = await asyncio.gather(
        asyncio.to_thread(create_archive_all_data)
    )

    await bot.send_message(
        message.chat.id,
        "Архив успешно сформирован",
    )

    # Отправка архива пользователю
    await bot.send_document(
        message.chat.id,
        InputFile(path_to_archive[0])
    )


# Функция для создания архива всех данных по ответам и тестам
def create_archive_all_data() -> pathlib.Path:
    path = pathlib.Path(pathlib.Path.cwd().joinpath(os.getenv("TEMP_REPORT_DIR")))
    file_name = f'data_{datetime.now().date()}'

    shutil.make_archive(
        str(path.joinpath(f'{file_name}')),
        'zip', pathlib.Path.cwd().joinpath('_disciplines')
    )

    return path.joinpath(f'{file_name}.zip')
