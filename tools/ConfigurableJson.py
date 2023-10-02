from abc import abstractmethod
from typing import List

from PyQt5.QtCore import QAbstractListModel


class ConfigurableJson:
    section_name: str = NotImplemented

    def __init__(self):
        self.children = []

    # load config function
    @abstractmethod
    def load_config(self):
        pass

    # store config
    @abstractmethod
    def get_config(self):
        return {self.section_name: {child.get_config for child in self.children}}

    def add_saving_children(self, children: dict):
        for child in children:
            if isinstance(child, ConfigurableJson) and child not in self.children:
                self.children.append(child)
            if isinstance(child, QAbstractListModel) and child not in self.children:
                self.children.append(child)
