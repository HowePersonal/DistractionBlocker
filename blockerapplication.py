import os

def read_file():
    with open('blockerfiles/blockedapplications', 'r') as file:
        lines = file.readlines()
    return lines

def blocked_APPS():
    blocked_app = []
    for line in read_file():
        blocked_app.append(line.strip())
    return blocked_app

def delete_block(appname):
    lines = read_file()
    with open('blockerfiles/blockedapplications', 'w') as file:
        for line in lines:
            if appname not in line:
                file.write(line)

def add_block(appname):
    with open('blockerfiles/blockedapplications', 'a') as file:
        file.write(appname)


def close_browsers():
    if os.system('tasklist | find "msedge.exe"') == 0: os.system("taskkill /im msedge.exe /f")
    if os.system('tasklist | find "chrome.exe"') == 0: os.system("taskkill /im chrome.exe /f")
    if os.system('tasklist | find "firefox.exe"') == 0: os.system("taskkill /im firefox.exe /f")
    if os.system('tasklist | find "opera.exe"') == 0: os.system("taskkill /im opera.exe /f")
    if os.system('tasklist | find "brave.exe"') == 0: os.system("taskkill /im brave.exe /f")
