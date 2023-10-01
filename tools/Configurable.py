import configparser
from abc import abstractmethod, ABC


class Configurable:
    section_name: str = NotImplemented

    def __init__(self):
        self.config = None

    # load config function
    @abstractmethod
    def load_config(self):
        pass

    # store config
    @abstractmethod
    def store_config(self):
        pass

    def set_config(self, config: configparser.ConfigParser):
        self.config = config
        return self
