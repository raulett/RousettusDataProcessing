from ...UI.DataProcessing.GNSS_import_window_ui import Ui_Import_GNSS_widget
from .GpxImportWidgetHandle import GpxImportWidgetHandle
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton
from ....tools.Configurable import Configurable
from PyQt5.QtCore import QAbstractListModel, Qt

import os


class ImportSourceDataModel(QAbstractListModel):
    def __init__(self, data):
        super(ImportSourceDataModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()].section_name
        if role == Qt.UserRole:
            return self._data[index.row()]


class GnssImportWindowHandle(Ui_Import_GNSS_widget, QDialog, Configurable):
    section_name = 'import_gnss'

    def __init__(self, main_window=None):
        super(GnssImportWindowHandle, self).__init__()
        print(os.path.abspath(__file__), 1)
        self.main_window = main_window
        self.setupUi(self)
        self.current_import_widget = self.main_import_widget
        self.ds_combobox.setModel(ImportSourceDataModel([GpxImportWidgetHandle]))
        self.ds_combobox.currentIndexChanged.connect(self.import_handler_changed)
        self.init_gui()

    def init_gui(self):
        self.import_handler_changed()

    def import_handler_changed(self):
        if self.ds_combobox.currentIndex() >= 0:
            new_widget_class = self.ds_combobox.currentData()
            index = self.horizontalLayout.indexOf(self.current_import_widget)
            new_widget = new_widget_class()
            self.current_import_widget.deleteLater()
            self.groupBox.layout().insertWidget(index, new_widget)
            self.current_import_widget = new_widget

    def load_config(self):
        pass

    def store_config(self):
        pass
