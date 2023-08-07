import os
from common import run_command


def test_run_command_successful():
    returncode = run_command('id')
    assert returncode == 0


def test_run_command_failed():
    returncode = run_command('nocommandexists')
    assert returncode != 0


def test_void():
    assert 1 == 1


# from common import replace_pattern_in_file


# def test_replace_pattern_in_file():
#     some_text = "This is a text the should=bereplaced"
#     file_path = './tmp.txt'

#     with open(file_path, 'w') as f:
#         f.write(some_text)

#     new_text = replace_pattern_in_file(
#         file_path, r'region( |)+=(.+)', 'my-replaced-text')

#     os.remove(file_path)

#     new_text == "This is a text the should=my-replaced-text"
#     assert 1==1
