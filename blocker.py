

def blocked_IPS():
    blocked_ip = {}
    for line in open('C:/Windows/System32/drivers/etc/hosts', 'r'):
        if "#" not in line and not line.isspace():
            split_ip = line.split()
            blocked_ip[split_ip[1]] = split_ip[0]
    return blocked_ip

def delete_block(hostname):
    with open('C:/Windows/System32/drivers/etc/hosts', 'r') as file:
        lines = file.readlines()
    with open('C:/Windows/System32/drivers/etc/hosts', 'w') as file:
        for line in lines:
            if hostname not in line:
                file.write(line)

def add_block(hostname):
    with open('C:/Windows/System32/drivers/etc/hosts', 'a') as file:
        if "www." in hostname:
            file.write("0.0.0.0" + "    " + hostname[3:] + "\n")
            file.write("0.0.0.0" + "    " + hostname + "\n")
        elif "www." not in hostname:
            file.write("0.0.0.0" + "    " + hostname + "\n")
            file.write("0.0.0.0" + "    " + "www." + hostname + "\n")
        file.write("::1     " + hostname + "\n")


