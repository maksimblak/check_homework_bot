# Импорты необходимых модулей и классов
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import Message
from homeworkbot.configuration import bot
from database.main_db import admin_crud


# Определение состояний для администратора
class AdminStates(StatesGroup):
    chat_id = State()


# Обработчик команды /addchat для администратора
@bot.message_handler(is_admin=True, commands=['addchat'])
async def handle_add_chat(message: Message):
    await _handle_add_chat(message)


# Обработчик команды /addchat для неадминистраторов
@bot.message_handler(is_admin=False, commands=['addchat'])
async def handle_no_add_chat(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


# Внутренний обработчик для команды /addchat
async def _handle_add_chat(message: Message) -> None:
    await bot.set_state(message.from_user.id, AdminStates.chat_id, message.chat.id)
    await bot.send_message(message.chat.id, "Введите telegram id добавляемого группового чата:")


# Обработчик для ввода telegram id группового чата
@bot.message_handler(state=AdminStates.chat_id)
async def chat_correct(message: Message):
    if message.text.lstrip("-").isdigit():
        admin_crud.add_chat(int(message.text))
        await bot.send_message(message.chat.id, "Групповой чат успешно добавлен!")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(message.chat.id, "Убедитесь, что вводите число!")
