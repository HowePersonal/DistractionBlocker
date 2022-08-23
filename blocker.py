def blocked_IPS():
    blocked_ip = {}
    for line in open('C:/Windows/System32/drivers/etc/hosts'):
        if ("#" not in line and not line.isspace()):
            split_ip = line.split()
            blocked_ip[split_ip[0]] = split_ip[1]
    return blocked_ip