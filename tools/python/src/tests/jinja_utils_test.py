from misc.jinja_utils import extract_variables_from_obj


def test_extract_variables_from_obj():
    obj = {
        'variable': 'root',
        'hosts': {
            'variable': 'hosts',
            'a': {
                'variable': 'a_host',
                'name': 'a'
            }
        },
        'key_pair': {
            'variable': 'keypair',
            'secret': 'This is a secret'
        }
    }

    output = extract_variables_from_obj(obj)
    assert output == {"root": {"variable": "root", "hosts": {"variable": "hosts", "a": {"variable": "a_host", "name": "a"}}, "key_pair": {"variable": "keypair", "secret": "This is a secret"}}, "hosts": {
        "variable": "hosts", "a": {"variable": "a_host", "name": "a"}, "key": "hosts"}, "a_host": {"variable": "a_host", "name": "a", "key": "a"}, "keypair": {"variable": "keypair", "secret": "This is a secret", "key": "key_pair"}}
