import configparser
import os

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    config.read(config_path)
    return config