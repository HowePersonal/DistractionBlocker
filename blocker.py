with open('C:/Windows/System32/drivers/etc/hosts', 'r') as file:
    lines = file.readlines()

def blocked_IPS():
    blocked_ip = {}
    for line in lines:
        if "#" not in line and not line.isspace():
            split_ip = line.split()
            blocked_ip[split_ip[1]] = split_ip[0]
    return blocked_ip

def delete_block(hostname):
    with open('C:/Windows/System32/drivers/etc/hosts', 'w') as file:
        for line in lines:
            if hostname not in line:
                file.write(line)

def add_block(hostname):
    with open('C:/Windows/System32/drivers/etc/hosts', 'a') as file:
        file.write("0.0.0.0" + "           " + hostname + "\n")

