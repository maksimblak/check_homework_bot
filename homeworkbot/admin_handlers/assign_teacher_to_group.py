from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from homeworkbot.admin_handlers.utils import create_teachers_button
from homeworkbot.configuration import bot
from database.main_db import admin_crud


# Обработчик команды для начала назначения преподавателя на группу
@bot.message_handler(is_admin=True, commands=['assigntgr'])
async def handle_assign_teacher_to_group(message: Message):
    # Вызываем функцию для создания интерфейса выбора преподавателя
    await create_teachers_button(message, 'assignTeacherGR')


# Обработчик команды, если нет доступа для назначения преподавателя на группу
@bot.message_handler(is_admin=False, commands=['assigntgr'])
async def handle_no_assign_teacher_to_group(message: Message):
    # Отправляем сообщение о запрете доступа
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Обработчик интерактивных кнопок связанных с назначением преподавателя на группу
@bot.callback_query_handler(func=lambda call: 'assignTeacherGR_' in call.data or 'assignGroupT_' in call.data)
async def callback_assign_teacher_to_group(call: CallbackQuery):
    # Извлекаем тип обратного вызова
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'assignTeacherGR':
            # Если выбрана опция назначения преподавателя на группу
            teacher_id = int(call.data.split('_')[1])
            # Получаем список групп, на которые преподаватель еще не назначен
            groups = admin_crud.get_not_assign_teacher_groups(teacher_id)
            if len(groups) < 1:
                # Если доступных групп нет, отправляем сообщение
                await bot.send_message(call.message.chat.id, "В БД отсутствуют группы, куда можно добавить студента!")
                return
            # Создаем интерфейс с кнопками для выбора группы
            markup = InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(
                *[InlineKeyboardButton(
                    it.group_name,
                    callback_data=f'assignGroupT_{it.id}_{teacher_id}'
                ) for it in groups]
            )
            # Редактируем сообщение для выбора группы
            await bot.edit_message_text(
                "Выберите группу, которой назначается преподаватель:",
                call.message.chat.id,
                call.message.id,
                reply_markup=markup,
            )
        case 'assignGroupT':
            # Если выбрана конкретная группа для назначения преподавателя
            group_id = call.data.split('_')[1]
            teacher_id = call.data.split('_')[2]
            # Назначаем преподавателя на выбранную группу
            admin_crud.assign_teacher_to_group(int(teacher_id), int(group_id))
            # Редактируем сообщение для показа успешного назначения
            await bot.edit_message_text(
                "Преподаватель назначен группе",
                call.message.chat.id,
                call.message.id,
            )
        case _:
            # Если тип обратного вызова не распознан, отправляем сообщение об ошибке
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)
