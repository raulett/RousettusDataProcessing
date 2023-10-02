import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from .DeviceListModel import SpectrumDevice


class EnWindowsTableModel(QAbstractTableModel):
    def __init__(self, device: SpectrumDevice):
        super(EnWindowsTableModel, self).__init__()
        self._data = device

    def set_data(self, device: SpectrumDevice):
        self.beginResetModel()
        self._data = device
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data.en_windows)

    def columnCount(self, parent=QModelIndex()):
        if len(self._data.en_windows) > 0:
            return len(list(self._data.en_windows[0].keys()))

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        column_name = list(self._data.en_windows[0].keys())[index.column()]
        if role == Qt.DisplayRole:
            return self._data.en_windows[index.row()].get(column_name, None)
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return list(self._data.en_windows[0].keys())[section]
            else:
                return section

    def remove_data(self, indexes):
        new_data = []
        for i, element in enumerate(self._data.en_windows):
            if i not in indexes:
                new_data.append(element)
        self.beginResetModel()
        self._data.en_windows = new_data
        self.endResetModel()
