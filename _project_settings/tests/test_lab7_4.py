from unittest import mock

# import lab7_4

task = 4
error_text = 'Неправильный результат'


def test_lab7_4(capsys, logger):
    input_data = [
        ['9', '3'],
        ['2', '10'],
        ['4', '6']
    ]

    for data in input_data:

        try:

            in_data = data[:]
            with mock.patch('builtins.input', lambda: in_data.pop()):
                # lab7_4.app()
                captured = capsys.readouterr()
                val2, val1 = list(map(int, data))
                assert captured.out == str((val1 * 3 + val1) / 4 - val2) + "\n"
                logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
