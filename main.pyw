import UserInterface
from configparser import ConfigParser

config_file = "config/settings.ini"
config = ConfigParser()
config.read(config_file)

if __name__ == '__main__':
    UserInterface.confirm_start()




