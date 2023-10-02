from ....UI.DataProcessing.GNSS_import_window_ui import Ui_Import_GNSS_widget
from .GpxImportWidgetHandle import GpxImportWidgetHandle
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton
from .....tools.Configurable import Configurable
from ..ImportSourceDataModel import ImportSourceDataModel
from ..import_handler_changed import import_handler_changed

import os


class GnssImportWindowHandle(Ui_Import_GNSS_widget, QDialog, Configurable):
    section_name = 'import_gnss'

    def __init__(self, main_window=None):
        super(GnssImportWindowHandle, self).__init__()
        self.main_window = main_window
        self.import_handler_changed = import_handler_changed
        self.setupUi(self)
        self.current_import_widget = self.main_import_widget
        self.ds_combobox.setModel(ImportSourceDataModel([GpxImportWidgetHandle]))
        self.init_gui()

    def init_gui(self):
        self.ds_combobox.currentIndexChanged.connect(lambda: self.import_handler_changed(self))
        self.import_handler_changed(self)

    def load_config(self):
        pass

    def store_config(self):
        pass
