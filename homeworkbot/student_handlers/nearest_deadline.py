import asyncio

from telebot.types import CallbackQuery

from database.main_db import student_crud
from homeworkbot import bot
from reports.deadline_report_builder import run_deadline_report_builder


# Callback-функция для обработки запросов о ближайших дедлайнах
@bot.callback_query_handler(func=lambda call: 'nearestDeadline_' in call.data)
async def callback_nearest_deadline(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'nearestDeadline':
            discipline_id = int(call.data.split('_')[1])
            student = student_crud.get_student_by_tg_id(call.from_user.id)
            await __create_report(call, student.id, discipline_id)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id
            )


# Внутренняя функция для создания и отправки отчета о ближайших дедлайнах
async def __create_report(
        call: CallbackQuery,
        student_id: int,
        discipline_id: int) -> None:
    await bot.edit_message_text(
        "Начинаем расчет ^_^",
        call.message.chat.id,
        call.message.id)

    report = await asyncio.gather(
        asyncio.to_thread(run_deadline_report_builder, student_id, discipline_id)
    )
    student_report = report[0]

    await bot.edit_message_text(
        f'<i>{student_report}</i>',
        call.message.chat.id,
        call.message.id,
        parse_mode="HTML"
    )
