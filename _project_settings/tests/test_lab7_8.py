from unittest import mock

# import lab7_8

task = 8
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_8(capsys, logger):
    input_data = [
        '1 4 9 8 12 7 4 81 23',
        '-9 -2 -1 9 8 3 9 2 -18'
        '1 2 3 4 5 1 1 2 3 1',
    ]

    for data in input_data:

        try:
            with mock.patch('builtins.input', return_value=data):
                # lab7_8.app()
                captured = capsys.readouterr()
                my_list = list(map(int, data.split()))
                result = my_list[0] + my_list[-1]
                assert captured.out == str(result) + "\n"
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
