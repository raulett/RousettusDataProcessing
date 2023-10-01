from .....GUI.UI.DataProcessing.import_dat_spectrum_widget_ui import Ui_import_dat_spectrum_widget
from .....tools.Configurable import Configurable
from .DatFilesListModel import DatFilesListModel

from PyQt5.QtWidgets import QWidget


class DatImportWidgetHandle(Ui_import_dat_spectrum_widget, QWidget, Configurable):
    section_name = 'import_dat'

    def __init__(self, main_window):
        super(DatImportWidgetHandle, self).__init__(main_window)
        self.main_window = main_window
        self.setupUi(self)
        self.dat_files_model = DatFilesListModel(self.main_window)
        self.dat_files_table.setModel(self.dat_files_model)
        self.init_gui()

    def init_gui(self):
        self.add_dat_button.clicked.connect(self.dat_files_model.add_files)
        self.rem_dat_button.clicked.connect(lambda: self.dat_files_model.remove_data({
            index.row() for index in self.dat_files_table.selectedIndexes()}))
        self.clr_dat_button.clicked.connect(self.dat_files_model.clr_files)

    def load_config(self):
        pass

    def store_config(self):
        pass
