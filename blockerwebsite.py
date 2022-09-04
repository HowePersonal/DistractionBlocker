import json

def read_file():
    with open('blockerfiles/blockedsites.json', 'r') as file:
        data = json.load(file)
    return data

def blocked_WEB():
    blocked_web = []
    for line in read_file()["sites"]:
        blocked_web.append(line.strip())
    return blocked_web

def delete_block(webname):
    data = read_file()
    if "www." in webname:
        data['sites'].remove(webname)
        data['sites'].remove(webname[4:])
    elif "www." not in webname:
        data['sites'].remove(webname)
        data['sites'].remove("www." + webname)

    json_data = json.dumps(data)
    with open('blockerfiles/blockedsites.json', 'w') as file:
        file.write(json_data)

def add_block(webname):
    data = read_file()
    if "www." == webname[:4]:
        data['sites'].append(webname)
        data['sites'].append(webname[4:])
    elif "www." != webname[:4]:
        data['sites'].append(webname)
        data['sites'].append("www." + webname)

    json_data = json.dumps(data)
    with open('blockerfiles/blockedsites.json', 'w') as file:
        file.write(json_data)
