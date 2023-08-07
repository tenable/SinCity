from builder.templating import to_terraform_json


def test_to_terraform_json():
    obj = {"abc": "this is nice", "def-ghi": "is this working"}
    output = to_terraform_json(obj)
    assert output == '{\n  abc: "this is nice",\n  def-ghi: "is this working"\n}'


def test_to_terraform_json_with_no_brackets():
    obj = {"abc": "this is nice", "def-ghi": "is this working"}
    output = to_terraform_json(obj, 2, True)
    assert output == 'abc: "this is nice",\n  def-ghi: "is this working"'
