from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from .....tools.ConfigurableJson import ConfigurableJson


class DeviceListModel(QAbstractListModel, ConfigurableJson):
    section_name = 'device_list_model'

    def __init__(self):
        super(DeviceListModel, self).__init__()
        self._data = []
        self.load_config()
        if len(self._data) == 0:
            new_dev = SpectrumDevice()
            new_dev.add_subwindow('INT', 'INT', 400, 2810)
            self._data.append(new_dev)

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()].dev_name
        if role == Qt.EditRole:
            return self._data[index.row()].dev_name
        if role == Qt.UserRole:
            return self._data[index.row()]
        if role == Qt.ToolTipRole:
            return (f'''{self._data[index.row()].dev_name}:\n
                    k = {self._data[index.row()].calibration_k}\n
                    b = {self._data[index.row()].calibration_b}\n
                    windows:\n
                    {self._data[index.row()].en_windows}''')
        return None

    def load_config(self):
        pass

    def get_config(self):
        pass


class SpectrumDevice(ConfigurableJson):
    section_name = 'spectrum_device'

    def __init__(self, name="Dev name"):
        super().__init__()
        self.dev_name = name
        self.calibration_k = 0
        self.calibration_b = 0
        self.en_windows = []

    def set_calibration(self, k: float = None, b: float = None):
        if k:
            self.calibration_k = k
        if b:
            self.calibration_b = b

    def set_name(self, name: str):
        self.dev_name = name

    def set_en_windows(self, en_windows: list):
        self.en_windows = en_windows

    def add_subwindow(self, win_name: str, subwin_name: str, lhb_en: float, rhb_en: float):
        self.en_windows.append({"w_name": win_name, "subw_name": subwin_name, "lhb": lhb_en, "rhb": rhb_en})

    def load_config(self):
        pass

    def get_config(self):
        pass
