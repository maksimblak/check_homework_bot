# import lab7_18
from unittest import mock
from math import sqrt, sin

task = 18
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_18(capsys, logger):
    input_data = ['2', '3', '9']

    for data in input_data:
        n = int(data)
        try:
            with mock.patch('builtins.input', lambda: data):
                # lab7_18.app()
                result = sqrt(21 + sqrt(3 ** n) / (3 / sin(n)))
                captured = capsys.readouterr()
                assert captured.out == str(result) + '\n'
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
