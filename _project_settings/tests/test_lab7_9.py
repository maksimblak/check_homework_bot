from unittest import mock
#import lab7_9

task = 9
error_text = 'Неправильный результат или проблема в считывании значений'


def test_lab7_9(capsys, logger):
    input_data = [
        '1 4 9 8 12 7 4 81 23',
        '9 -2 -1 9 8 3 9 2 -18'
        '1 2 3 4 5 1 1 2 3 1',
    ]

    for data in input_data:

        try:
            with mock.patch('builtins.input', return_value=data):
                #lab7_9.app()
                my_list = list(map(int, data.split()))
                middle = len(my_list) // 2
                result = my_list[1] * my_list[middle]
                captured = capsys.readouterr()
                assert captured.out == str(result) + "\n"
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')