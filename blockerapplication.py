from main import config
import json

def read_file():
    with open('blockerfiles/blockedapplications.json', 'r') as file:
        data = json.load(file)
    return data

def blocked_APPS():
    return read_file()

def delete_block(appname):
    data = read_file()

    if appname in data: data.remove(appname)

    json_data = json.dumps(data)
    with open('blockerfiles/blockedapplications.json', 'w') as file:
        file.write(json_data)


def add_block(appname):
    data = read_file()

    if appname not in data: data.append(appname)

    json_data = json.dumps(data)
    with open('blockerfiles/blockedapplications.json', 'w') as file:
        file.write(json_data)



