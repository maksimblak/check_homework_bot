from unittest import mock
#import lab7_11
from math import sqrt

task = 11
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_11(capsys, logger):
    input_data = ['2', '3', '9']

    for data in input_data:
        try:
            n = int(data)
            with mock.patch('builtins.input', lambda: data):
                #lab7_11.app()
                result = sqrt((n + 2.5 * n) ** 3) / 4
                captured = capsys.readouterr()
                assert captured.out == str(result) + '\n'
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
