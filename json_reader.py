import json


def json_read(path):
    json_file = open(path, 'r')
    json_data = json_file.read()
    return json.loads(json_data)