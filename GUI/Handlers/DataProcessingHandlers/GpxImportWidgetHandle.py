from ....tools.Configurable import Configurable
from ...UI.DataProcessing.import_gpx_widget_ui import Ui_gpx_import_form
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex


class GpxFileListModel(QAbstractTableModel):
    def __init__(self):
        super(GpxFileListModel, self).__init__()
        self._data = []
        self._headers = ['Filename', 'Filepath']

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

class GpxImportWidgetHandle(Ui_gpx_import_form, QWidget, Configurable):
    section_name = 'import_gpx'

    def __init__(self, main_window=None):
        super(GpxImportWidgetHandle, self).__init__(main_window)
        self.main_window = main_window
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        pass

    def load_config(self):
        pass

    def store_config(self):
        pass
