import json
import os


def _load(config_file):
    with open(os.getcwd() + os.path.sep +  config_file, 'r') as opened_file:
        return json.load(opened_file)


class Config(object):
    def __init__(self, config_file):
        self._state = _load(config_file)

    def get_value(self, name):
        value = os.getenv(self._to_environ_varname(name))
        if not value:
            value = self._state[name]
        return value

    @staticmethod
    def _to_environ_varname(string):
        return string.upper().replace('-', '_')
