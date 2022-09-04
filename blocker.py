from main import config, config_file
import blockerapplication
import notifypy
import json
import time
import os

def start_appblock():
    notification = notifypy.Notify()
    notification.title = "Application Blocked"

    while True:
        for item in blockerapplication.read_file():
            if os.system(f'tasklist | find "{item.strip()}"') == 0:
                os.system(f"taskkill /im {item.strip()} /f")
                notification.message = f"{item.strip()} is active on the block list"
                notification.send()
            time.sleep(1)
        time.sleep(2)


def add_block(listNum, day, start, end):
    with open('blockerfiles/blocks.json', 'r') as file:
        data = json.load(file)

    if listNum not in data[day]: data[day][listNum] = []
    data[day][listNum].append(start)
    data[day][listNum].append(end)

    json_data = json.dumps(data)
    with open('blockerfiles/blocks.json', 'w') as file:
        file.write(json_data)


