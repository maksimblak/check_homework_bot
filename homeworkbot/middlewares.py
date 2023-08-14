from enum import Enum, auto
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message
from database.main_db import student_crud, common_crud


# Класс для промежуточного ПО, блокирующего доступ забаненных студентов
class BanMiddleware(BaseMiddleware):
    def __init__(self, bot: AsyncTeleBot) -> None:
        self.update_types = ['message']
        self.bot = bot

    async def pre_process(self, message: Message, data):
        # Проверяем, есть ли пользователь в списке забаненных
        if common_crud.is_ban(message.from_user.id):
            # Если пользователь забанен, отправляем ему сообщение и отменяем обновление
            await self.bot.send_message(
                message.chat.id,
                f'Функциональность бота недоступна, вы в бан-листе!!! '
                f'Для разблокировки обратитесь к своему преподавателю!'
            )
            return CancelUpdate()

    async def post_process(self, message, data, exception):
        pass


# Состояния для контроля ограничения на запросы студентов
class FloodMiddlewareState(Enum):
    UPLOAD_ANSWER = auto()
    WAIT_UPLOAD_ANSWER = auto()


# Класс для промежуточного ПО, лимитирующего запросы студентов
class StudentFloodMiddleware(BaseMiddleware):
    def __init__(self, bot: AsyncTeleBot, load_answers_limit: int, commands_limit: int) -> None:
        # Словари для отслеживания времени последнего запроса
        self.last_answer_time = {}
        self.last_command_time = {}
        # Состояния запросов студентов
        self.state = {}
        self.bot = bot
        self.load_answers_limit = load_answers_limit * 60  # Переводим в секунды
        self.commands_limit = commands_limit * 60  # Переводим в секунды
        self.update_types = ['message']

    async def pre_process(self, message: Message, data):
        if student_crud.is_student(message.from_user.id):
            if message.text in ['Ближайший дедлайн', 'Успеваемость', 'Загрузить ответ']:
                if (not message.from_user.id in self.last_answer_time and
                        message.text == 'Загрузить ответ'):
                    self.state[message.from_user.id] = FloodMiddlewareState.WAIT_UPLOAD_ANSWER
                    self.last_answer_time[message.from_user.id] = message.date
                    return

                if (not message.from_user.id in self.last_command_time and
                        message.text in ['Ближайший дедлайн', 'Успеваемость']):
                    self.last_command_time[message.from_user.id] = message.date
                    return

                is_flood = False
                last_time = 0
                match message.text:
                    case 'Загрузить ответ':
                        if (message.date - self.last_answer_time[message.from_user.id] <
                                self.load_answers_limit):
                            last_time = self.load_answers_limit
                            last_time -= message.date - self.last_answer_time[message.from_user.id]
                            is_flood = True
                        else:
                            self.state[message.from_user.id] = FloodMiddlewareState.WAIT_UPLOAD_ANSWER
                        self.last_answer_time[message.from_user.id] = message.date
                    case _:
                        if (message.date - self.last_command_time[message.from_user.id] <
                                self.commands_limit):
                            last_time = self.commands_limit
                            last_time -= message.date - self.last_command_time[message.from_user.id]
                            is_flood = True
                        self.last_command_time[message.from_user.id] = message.date

                if is_flood:
                    # Если есть нарушение лимита, отправляем сообщение и отменяем обновление
                    await self.bot.send_message(
                        message.chat.id,
                        f'Лимит до следующего обращения к боту еще не истек!!!'
                        f'Обратитесь к боту через {last_time // 60} минут...'
                    )
                    return CancelUpdate()

            elif message.text == '/start':
                return
            else:
                if (self.state[message.from_user.id] == FloodMiddlewareState.WAIT_UPLOAD_ANSWER and
                        message.content_type == 'document'):
                    self.state[message.from_user.id] = FloodMiddlewareState.UPLOAD_ANSWER
                else:
                    return CancelUpdate()

    async def post_process(self, message, data, exception):
        pass
