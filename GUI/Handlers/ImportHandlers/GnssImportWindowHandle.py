from PyQt5.QtWidgets import QDialog

from tools.Configurable import Configurable

from GUI.UI.DataProcessing.GNSS_import_window_ui import Ui_Import_GNSS_widget


class FlightPlanningHandle(Ui_Import_GNSS_widget, QDialog, Configurable):
    section_name = "import_gnss_data"

    def __init__(self, main_window=None):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        pass

    def load_config(self):
        pass

    def store_config(self):
        pass
