from PyQt5.QtCore import QAbstractListModel, Qt


class ImportSourceDataModel(QAbstractListModel):
    def __init__(self, data: list):
        super(ImportSourceDataModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()].section_name
        if role == Qt.UserRole:
            return self._data[index.row()]