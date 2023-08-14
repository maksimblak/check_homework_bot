from unittest import mock

# import lab7_6

task = 6
error_text = 'Неправильное деление'


def test_lab7_4(capsys, logger):
    input_data = [
        27,
        65,
        61,
    ]

    for data in input_data:
        try:

            # lab7_6.app()

            captured = capsys.readouterr()
            val2, val1 = list(map(int, data))

            assert captured.out == str(data % 3) + "\n"
            logger.add_successful_task(task)

        except AssertionError as aerr:
            logger.add_fail_task(task, error_text)

        except Exception as ex:
            logger.add_fail_task(task, 'Что-то пошло не так... Оо')
