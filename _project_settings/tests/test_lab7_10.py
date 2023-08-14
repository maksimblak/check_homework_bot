from unittest import mock
# import lab7_10
from math import sqrt

task = 10
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_10(capsys, logger):
    input_data = ['2', '3', '9']

    for data in input_data:
        try:
            n = int(data)
            with mock.patch('builtins.input', lambda: data):
                # lab7_10.app()
                captured = capsys.readouterr()
                result = (sqrt(n + sqrt(n ** n)) / 7)
                assert captured.out == str(result) + '\n'
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
