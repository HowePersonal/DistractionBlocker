def open_host():
    for line in open('C:/Windows/System32/drivers/etc/hosts'):
        if ("#" not in line and not line.isspace()):
            print(line)
open_host()