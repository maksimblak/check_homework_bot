from unittest import mock
# import lab7_12
from math import sqrt

task = 12
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_12(capsys, logger):
    input_data = ['2', '3', '9']

    for data in input_data:
        n = int(data)
        try:
            with mock.patch('builtins.input', lambda: data):
                # lab7_12.app()
                result = (n - 20) / sqrt(n ** 3)
                captured = capsys.readouterr()
                assert captured.out == str(result) + '\n'
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
