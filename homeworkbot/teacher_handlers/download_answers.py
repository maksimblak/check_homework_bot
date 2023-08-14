import asyncio
from pathlib import Path

from telebot.types import CallbackQuery, InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from database.main_db import teacher_crud, common_crud
from homeworkbot.configuration import bot
from reports.create_answers_archive import create_answers_archive

# Префиксы для обработки данных о скачивании ответов
__answer_prefix = [
    'dowTAnswersDis_',
    'dowTAnswersGr_',
]


# Проверка, содержит ли callback_data один из префиксов
def __is_answer_prefix_callback(data: str) -> bool:
    for it in __answer_prefix:
        if it in data:
            return True
    return False


# Обработчик callback-запросов для скачивания ответов
@bot.callback_query_handler(
    func=lambda call: __is_answer_prefix_callback(call.data)
)
async def callback_download_answers(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'dowTAnswersDis':
            # Извлечение идентификатора дисциплины из callback_data
            discipline_id = int(call.data.split('_')[1])
            discipline = common_crud.get_discipline(discipline_id)
            path = Path.cwd().joinpath(discipline.path_to_answer)
            dirs = [it for it in path.iterdir() if it.is_dir()]
            if not dirs:
                await bot.edit_message_text(
                    "Директории для скачивания ответов отсутствуют",
                    call.message.chat.id,
                    call.message.id)
            else:
                # Получение групп, к которым преподаватель привязан
                teacher_groups = teacher_crud.get_assign_groups(call.from_user.id)
                # Отфильтровать директории по группам преподавателя
                dirs = [
                    it for it in dirs if it.name in [tg.group_name for tg in teacher_groups]
                ]
                markup = InlineKeyboardMarkup()
                markup.row_width = 1
                markup.add(
                    *[InlineKeyboardButton(
                        it.name,
                        callback_data=f'dowTAnswersGr_{it.name}_{discipline_id}'
                    ) for it in dirs]
                )
                await bot.edit_message_text(
                    "Выберите группу:",
                    call.message.chat.id,
                    call.message.id,
                    reply_markup=markup,
                )
        case 'dowTAnswersGr':
            group_name = call.data.split('_')[1]
            discipline_id = int(call.data.split('_')[2])
            discipline = common_crud.get_discipline(discipline_id)
            path = Path.cwd().joinpath(discipline.path_to_answer)
            path = path.joinpath(group_name)
            await _download_answer(call, path)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)


# Функция для скачивания архива с ответами
async def _download_answer(call: CallbackQuery, path_to_group_folder: Path):
    await bot.edit_message_text(
        "Начинаем формировать архив",
        call.message.chat.id,
        call.message.id)

    # Создание архива в отдельном потоке
    path_to_archive = await asyncio.gather(
        asyncio.to_thread(create_answers_archive, path_to_group_folder)
    )

    await bot.edit_message_text(
        "Архив успешно сформирован",
        call.message.chat.id,
        call.message.id)

    # Отправка архива пользователю
    await bot.send_document(
        call.message.chat.id,
        InputFile(path_to_archive[0])
    )
