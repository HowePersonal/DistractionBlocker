import blockerapplication
import notifypy
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



