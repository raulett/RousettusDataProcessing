from PyQt5.QtWidgets import QDialog

from ...UI.DataProcessing.Spectrum_data_import_ui import Ui_Import_spectrum_widget
from ....tools.Configurable import Configurable
from .ImportSourceDataModel import ImportSourceDataModel
from .SpectrumImportHandle.DatImportWidgetHandle import DatImportWidgetHandle
from .import_handler_changed import import_handler_changed


class SpectrumImportWindowHandle(Ui_Import_spectrum_widget, QDialog, Configurable):
    section_name = 'import_spectrum'

    def __init__(self, main_window=None):
        super(SpectrumImportWindowHandle, self).__init__()
        self.main_window = main_window
        self.import_handler_changed = import_handler_changed
        self.setupUi(self)
        self.current_import_widget = self.main_import_widget
        self.ds_combobox.setModel(ImportSourceDataModel([DatImportWidgetHandle]))
        self.init_gui()

    def init_gui(self):
        self.ds_combobox.currentIndexChanged.connect(lambda: self.import_handler_changed(self))
        self.import_handler_changed(self)

    def load_config(self):
        pass

    def store_config(self):
        pass
