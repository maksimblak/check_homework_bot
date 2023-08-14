from telebot.types import Message

from homeworkbot.admin_handlers.utils import create_groups_button
from homeworkbot.configuration import bot


# Обработчик команды на скачивание полного отчета для группы
@bot.message_handler(is_admin=True, commands=['finrep'])
async def handle_download_full_report(message: Message):
    await create_groups_button(message, 'finishReport')


# Обработчик команды на скачивание полного отчета для группы для недостаточно привилегированных пользователей
@bot.message_handler(is_admin=False, commands=['finrep'])
async def handle_no_download_full_report(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")
