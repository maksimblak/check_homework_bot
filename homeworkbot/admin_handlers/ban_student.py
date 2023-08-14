from telebot.types import Message, CallbackQuery

from database.main_db import common_crud
from homeworkbot.admin_handlers.utils import create_groups_button, create_callback_students_button
from homeworkbot.configuration import bot


# Обработчик команды для начала процесса блокировки студента
@bot.message_handler(is_admin=True, commands=['ban'])
async def handle_ban_student(message: Message):
    # Создаем интерфейс выбора группы
    await create_groups_button(message, 'groupBan')


# Обработчик команды, если нет доступа для блокировки студента
@bot.message_handler(is_admin=False, commands=['ban'])
async def handle_no_ban_student(message: Message):
    # Отправляем сообщение о запрете доступа
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Обработчик интерактивных кнопок связанных с блокировкой студента
@bot.callback_query_handler(func=lambda call: 'studentBan_' in call.data or 'groupBan_' in call.data)
async def callback_ban_student(call: CallbackQuery):
    # Извлекаем тип обратного вызова
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'groupBan':
            # Если выбрана опция блокировки студента на уровне группы
            group_id = int(call.data.split('_')[1])
            # Получаем список студентов из выбранной группы
            students = common_crud.get_students_from_group_for_ban(group_id)
            # Создаем интерфейс с кнопками для выбора студента
            await create_callback_students_button(call, students, 'studentBan')
        case 'studentBan':
            # Если выбран конкретный студент для блокировки
            telegram_id = int(call.data.split('_')[1])
            # Блокируем студента в базе данных
            common_crud.ban_student(telegram_id)
            # Редактируем сообщение для показа успешной блокировки
            await bot.edit_message_text(
                "Студент добавлен в бан-лист",
                call.message.chat.id,
                call.message.id)
        case _:
            # Если тип обратного вызова не распознан, отправляем сообщение об ошибке
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)
