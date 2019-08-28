import json


class Configuration(object):
    file_path = 'config/config.json'
    config = {}

    @staticmethod
    def load():
        with open(Configuration.file_path) as config_file:
            print("Loading configuration file.")
            Configuration.config = json.load(config_file)
