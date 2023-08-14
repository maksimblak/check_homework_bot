from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.main_db import common_crud
from homeworkbot.configuration import bot


# Обработчик команды на разбан студентов
@bot.message_handler(is_admin=True, commands=['unban'])
async def handle_unban_student(message: Message):
    await create_unban_student_buttons(message)


# Обработчик команды на разбан студентов для недостаточно привилегированных пользователей
@bot.message_handler(is_admin=False, commands=['unban'])
async def handle_no_unban_student(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Функция для создания кнопок выбора забаненных студентов
async def create_unban_student_buttons(message: Message):
    students = common_crud.get_ban_students(message.from_user.id)
    if len(students) < 1:
        await bot.send_message(message.chat.id, "Нет забаненных студентов!")
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        *[InlineKeyboardButton(
            it.full_name,
            callback_data=f'studentUnBan_{it.telegram_id}'
        ) for it in students]
    )
    await bot.send_message(
        message.chat.id,
        "Выберите студента для разбана:",
        reply_markup=markup
    )


# Обработчик нажатия на кнопку разбана студента
@bot.callback_query_handler(func=lambda call: 'studentUnBan_' in call.data)
async def callback_unban_student(call):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'studentUnBan':
            telegram_id = int(call.data.split('_')[1])
            common_crud.unban_student(telegram_id)
            await bot.edit_message_text(
                "Студент разбанен!",
                call.message.chat.id,
                call.message.id)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)
