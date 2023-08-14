import asyncio
import pathlib

from telebot.types import InputFile, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.main_db import admin_crud, teacher_crud, common_crud
from homeworkbot import bot
from reports.run_report_builder import ReportBuilderTypeEnum, run_report_builder

# Префиксы для обработки различных типов отчетов
__report_prefix = [
    'fullReport_',
    'fullGrReport_',
    'finishReport_',
    'finishGrReport_',
    'shortReport_',
    'shortGrReport_',
]

# Словарь для перехода на следующий этап формирования отчета
__next_step = {
    'fullReport': 'fullGrReport',
    'finishReport': 'finishGrReport',
    'shortReport': 'shortGrReport',
}

# Словарь типов отчетов
__reports_builder_type = {
    'fullGrReport': ReportBuilderTypeEnum.FULL,
    'finishGrReport': ReportBuilderTypeEnum.FINISH,
    'shortGrReport': ReportBuilderTypeEnum.SHORT,
}


# Функция для проверки, является ли callback префиксом отчета
def __is_download_prefix_callback(data: str) -> bool:
    for it in __report_prefix:
        if it in data:
            return True
    return False


# Обработчик callback-запросов для скачивания и отправки отчетов
@bot.callback_query_handler(func=lambda call: __is_download_prefix_callback(call.data))
async def callback_download_full_report(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        # Обработка запроса для формирования отчета по группе и дисциплине
        case 'fullReport' | 'finishReport' | 'shortReport':
            await bot.edit_message_text(
                "Выберете предмет",
                call.message.chat.id,
                call.message.id)
            group_id = int(call.data.split('_')[1])
            if admin_crud.is_admin_no_teacher_mode(call.from_user.id):
                disciplines = common_crud.get_group_disciplines(group_id)
            else:
                disciplines = teacher_crud.get_assign_group_discipline(
                    call.from_user.id,
                    group_id
                )
            if len(disciplines) == 0:
                await bot.edit_message_text(
                    "За группой не числится дисциплин",
                    call.message.chat.id,
                    call.message.id)
            elif len(disciplines) > 1:
                markup = InlineKeyboardMarkup()
                markup.row_width = 1
                markup.add(
                    *[InlineKeyboardButton(
                        it.short_name,
                        callback_data=f'{__next_step[type_callback]}_{group_id}_{it.id}'
                    ) for it in disciplines]
                )
                await bot.edit_message_text(
                    "Выберите дисциплину:",
                    call.message.chat.id,
                    call.message.id,
                    reply_markup=markup,
                )
            else:
                await __create_report(
                    call,
                    group_id,
                    disciplines[0].id,
                    __reports_builder_type[__next_step[type_callback]]
                )
        # Обработка запроса для формирования отчета по группе и дисциплине
        case 'fullGrReport' | 'finishGrReport' | 'shortGrReport':
            group_id = int(call.data.split('_')[1])
            discipline_id = int(call.data.split('_')[2])
            await __create_report(call, group_id, discipline_id, __reports_builder_type[type_callback])
        # Если тип callback не распознан
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)


# Функция для формирования и отправки отчета
async def __create_report(
        call: CallbackQuery,
        group_id: int,
        discipline_id: int,
        builder_type: ReportBuilderTypeEnum) -> None:
    """
    Функция запуска формирования отчета в отдельном потоке

    :param call: CallbackQuery для отправки отчета и редактирования сообщений в чате
    :param group_id: id группы по которой формируется отчет
    :param discipline_id: id дисциплины по которой формируется отчет
    :param builder_type: тип формируемого отчета

    :return: None
    """

    # Отправка сообщения о начале формирования отчета
    await bot.edit_message_text(
        "Начинаем формировать отчет",
        call.message.chat.id,
        call.message.id)

    # Запуск формирования отчета в отдельном потоке с использованием asyncio.to_thread
    path_to_report = await asyncio.gather(
        asyncio.to_thread(run_report_builder, group_id, discipline_id, builder_type)
    )

    # Отправка сообщения о завершении формирования отчета
    await bot.edit_message_text(
        "Отчет успешно сформирован",
        call.message.chat.id,
        call.message.id)

    # Отправка сформированного отчета в виде документа
    await bot.send_document(
        call.message.chat.id,
        InputFile(pathlib.Path(path_to_report[0]))
    )
