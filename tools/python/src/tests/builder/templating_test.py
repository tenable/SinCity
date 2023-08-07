from builder.templating import get_nested_object
import pytest


@pytest.fixture
def sample_dict():
    return {
        "foo": {
            "bar": [
                {"baz": 1},
                {"baz": 2},
                {"baz": 3}
            ]
        },
        "qux": "quux"
    }


def test_get_nested_object(sample_dict):
    assert get_nested_object(sample_dict, "foo.bar[0].baz") == 1
    assert get_nested_object(sample_dict, "foo.bar[1].baz") == 2
    assert get_nested_object(sample_dict, "foo.bar[2].baz") == 3
    assert get_nested_object(sample_dict, "qux") == "quux"
    assert get_nested_object(sample_dict, "nonexistent.key") is None
    assert get_nested_object(sample_dict, "foo.bar[3].baz") is None
    assert get_nested_object(sample_dict, "foo.bar[0]") == {"baz": 1}
    assert get_nested_object(sample_dict, "foo.bar") == [
        {"baz": 1},
        {"baz": 2},
        {"baz": 3}
    ]
