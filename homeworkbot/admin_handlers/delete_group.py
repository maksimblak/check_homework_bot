from telebot.types import Message, CallbackQuery

from database.main_db import admin_crud
from homeworkbot.admin_handlers.utils import create_groups_button
from homeworkbot.configuration import bot


# Обработчик команды на удаление группы
@bot.message_handler(is_admin=True, commands=['delgroup'])
async def handle_delete_group(message: Message):
    await create_groups_button(message, 'groupDel')


# Обработчик команды на удаление группы для недостаточно привилегированных пользователей
@bot.message_handler(is_admin=False, commands=['delgroup'])
async def handle_no_delete_group(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Callback-обработчик запроса на удаление группы
@bot.callback_query_handler(func=lambda call: 'groupDel_' in call.data)
async def callback_delete_group(call: CallbackQuery):
    group_id = int(call.data.split('_')[1])

    # Вызов функции для удаления группы из базы данных
    admin_crud.delete_group(group_id)

    # Отправка сообщения об успешном удалении группы
    await bot.edit_message_text(
        "Выбранная группа успешно удалена!",
        call.message.chat.id,
        call.message.id)
