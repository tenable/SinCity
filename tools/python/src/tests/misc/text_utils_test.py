from misc.text_utils import remove_extra_spaces


def test_remove_extra_spaces():
    text = remove_extra_spaces(
        'This is a string\n\n\n\n    with extra lines and spaces    ')
    assert text == 'This is a string\n\n    with extra lines and spaces'
