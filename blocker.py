import blockerapplication
import time
import os

def start_appblock():
    while True:
        for item in blockerapplication.read_file():
            if os.system(f'tasklist | find "{item.strip()}"') == 0: os.system(f"taskkill /im {item.strip()} /f")
            time.sleep(1)



