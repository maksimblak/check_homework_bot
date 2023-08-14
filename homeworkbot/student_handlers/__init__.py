# __init__.py
__all__ = ["student_menu", "student_keyboard"]


import homeworkbot.student_handlers.student_menu as student_menu
from homeworkbot.student_handlers.student_menu import student_keyboard
import homeworkbot.student_handlers.academic_performance as academic_performance
import homeworkbot.student_handlers.nearest_deadline as nearest_deadline
import homeworkbot.student_handlers.answer_handlers as answer_handlers