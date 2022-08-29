import os

def read_file():
    with open('C:/Windows/System32/drivers/etc/hosts', 'r') as file:
        lines = file.readlines()
    return lines

def close_browsers():
    #if os.system('tasklist | find "msedge.exe"') == 0: os.system("taskkill /im msedge.exe /f")
    if os.system('tasklist | find "chrome.exe"') == 0: os.system("taskkill /im chrome.exe /f")
    if os.system('tasklist | find "firefox.exe"') == 0: os.system("taskkill /im firefox.exe /f")
    if os.system('tasklist | find "opera.exe"') == 0: os.system("taskkill /im opera.exe /f")
    if os.system('tasklist | find "brave.exe"') == 0: os.system("taskkill /im brave.exe /f")

def blocked_IPS():
    blocked_ip = {}
    for line in read_file():
        if "#" not in line and not line.isspace() and "www" not in line:
            split_ip = line.split()
            blocked_ip[split_ip[1]] = split_ip[0]
    return blocked_ip

def delete_block(hostname):
    lines = read_file()
    with open('C:/Windows/System32/drivers/etc/hosts', 'w') as file:
        for line in lines:
            if hostname not in line:
                file.write(line)

def add_block(hostname):
    with open('C:/Windows/System32/drivers/etc/hosts', 'a') as file:
        if "www." in hostname:
            file.write("0.0.0.0" + "    " + hostname + "\n")
            file.write("0.0.0.0" + "    " + hostname[3:] + "\n")
        elif "www." not in hostname:
            file.write("0.0.0.0" + "    " + hostname + "\n")
            file.write("0.0.0.0" + "    " + "www." + hostname + "\n")
        file.write("::1     " + hostname + "\n\n")




