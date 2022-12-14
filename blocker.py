from main import config, config_file
from datetime import datetime
import blockerapplication
import notifypy
import json
import time
import os

def start_block():
    notification = notifypy.Notify()
    notification.title = "Application Blocked"
    while True:
        time.sleep(1)
        if should_block():
            for item in blockerapplication.read_file():
                if os.system(f'tasklist | find "{item.strip()}"') == 0:
                    os.system(f"taskkill /im {item.strip()} /f")
                    notification.message = f"{item.strip()} is active on the block list"
                    notification.send()
                time.sleep(1)
            time.sleep(2)
        else:
            time.sleep(5)





def read_blocks():
    with open('blockerfiles/blocks.json', 'r') as file:
        data = json.load(file)
    return data

def should_block():
    config.read(config_file)

    if config['blocker']['block'] == 'on':
        return True
    elif config['blocker']['scheduledblock'] == 'on':
        if should_scheduledblock(): return True
    return False

def should_scheduledblock():
    data = read_blocks()
    user_day = datetime.today().strftime('%A')
    time_now = datetime.now().strftime("%H:%M:%S")
    for times in data[user_day].values():
        start_time = times[0]
        end_time = times[1]
        if start_time < time_now and end_time > time_now:
            return True

def should_lockscheduledblock():
    config.read(config_file)

    if config['blocker']['scheduledblock'] == 'on' and config['blocker']['lockscheduledblock'] == 'on':
        return True
    return False

def should_lockTaskManager():
    config.read(config_file)

    if config['blocker']['locktaskmanager'] == 'on':
        return True
    return False


def add_block(day, items):
    data = read_blocks()
    data[day] = {}
    listNum = 1
    for row, time in items:
        data[day][listNum] = []
        data[day][listNum].append(time[0].time().toString())
        data[day][listNum].append(time[1].time().toString())
        listNum += 1

    json_data = json.dumps(data)
    with open('blockerfiles/blocks.json', 'w') as file:
        file.write(json_data)

def remove_block(listNum, day):
    data = read_blocks()
    del data[day][str(listNum)]
    json_data = json.dumps(data)
    with open('blockerfiles/blocks.json', 'w') as file:
        file.write(json_data)


date_to_value = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

