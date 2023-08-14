from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.main_db import student_crud
from homeworkbot import bot


# Создание InlineKeyboardButton для выбора дисциплин студентом
async def create_student_disciplines_button(message: Message, prefix: str):
    # Получение списка дисциплин, на которые студент записан
    disciplines = student_crud.get_assign_disciplines(message.from_user.id)

    # Проверка, есть ли у студента доступные дисциплины
    if len(disciplines) < 1:
        await bot.send_message(message.chat.id, "В БД отсутствуют дисциплины!")
        return

    # Создание клавиатуры
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Добавление кнопок для каждой доступной дисциплины
    markup.add(
        *[
            InlineKeyboardButton(it.short_name, callback_data=f"{prefix}_{it.id}")
            for it in disciplines
        ]
    )

    # Отправка сообщения с клавиатурой для выбора дисциплины
    await bot.send_message(
        message.chat.id, "Выберете дисциплину:", parse_mode="HTML", reply_markup=markup
    )
