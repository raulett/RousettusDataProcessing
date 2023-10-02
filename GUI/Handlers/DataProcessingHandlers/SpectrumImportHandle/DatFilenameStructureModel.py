from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt


class DatFilenameStructureModel(QAbstractListModel):
    def __init__(self):
        super(DatFilenameStructureModel, self).__init__()
        self._data = []
        self.init_list()

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.UserRole:
            return self._data[index.row()]
        if role == Qt.EditRole:
            return self._data[index.row()]
        return None

    def init_list(self):
        self._data.append(r".*_?(\d{8})_(\d{6})_(\d+).dat")
