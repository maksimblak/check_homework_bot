# import lab7_17
from unittest import mock
from math import sqrt, cos

task = 17
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_17(capsys, logger):
    input_data = ['2', '3', '9']

    for data in input_data:
        n = int(data)
        try:
            with mock.patch('builtins.input', lambda: data):
                # lab7_17.app()
                result = (10 + 2 * cos(n)) / (5 - sqrt(n ** 5))
                captured = capsys.readouterr()
                assert captured.out == str(result) + '\n'
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
