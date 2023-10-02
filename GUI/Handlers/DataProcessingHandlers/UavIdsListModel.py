from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt

from ....tools.VectorLayerSaverGPKG.GpsLayerSaverGPKG import GpsLayerSaverGPKG


class UavIdsListModel(QAbstractListModel):
    def __init__(self, gps_layer_saver: GpsLayerSaverGPKG):
        super(UavIdsListModel, self).__init__()
        self._layer_saver = gps_layer_saver
        self._data = []
        self._data_changed_handle()
        self._data_provider = gps_layer_saver.get_layer().dataProvider()
        self._data_provider.dataChanged.connect(self._data_changed_handle)

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.UserRole:
            return self._data[index.row()]
        if role == Qt.EditRole:
            return self._data[index.row()]

    def _data_changed_handle(self):
        self.beginResetModel()
        self._data = list(self._layer_saver.get_layer().uniqueValues(
            self._layer_saver.get_layer().fields().indexFromName(self._layer_saver.get_uav_id_fieldname())))
        if len(self._data) == 0:
            self._data.append('UAV ID')
        self.endResetModel()
