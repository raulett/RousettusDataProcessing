from qgis.core import QgsFeatureRequest, QgsFeatureIterator

from .....GUI.UI.DataProcessing.import_dat_spectrum_widget_ui import Ui_import_dat_spectrum_widget
from .....tools.ConfigurableJson import ConfigurableJson
from ..UavIdsListModel import UavIdsListModel
from .DatFilesListModel import DatFilesListModel
from .DatFilenameStructureModel import DatFilenameStructureModel
from .....tools.VectorLayerSaverGPKG.GpsLayerSaverGPKG import GpsLayerSaverGPKG
from .AddEnWindowDialogHandle import AddEnWindowDialogHandle
from .DeviceListModel import DeviceListModel, SpectrumDevice
from .EnWindowsTableModel import EnWindowsTableModel

from PyQt5.QtWidgets import QWidget


class DatImportWidgetHandle(Ui_import_dat_spectrum_widget, QWidget, ConfigurableJson):
    section_name = 'import_dat'

    def __init__(self, main_window):
        super(DatImportWidgetHandle, self).__init__(main_window)
        self.en_win_dialog = None
        self.main_window = main_window
        self.setupUi(self)
        # init gps layer saver
        self.gps_layer_saver = GpsLayerSaverGPKG(self.main_window)
        # init dat files name structure combobox.
        self.dat_filename_struct_model = DatFilenameStructureModel()
        self.dat_filename_struct_combobox.setModel(self.dat_filename_struct_model)

        self.dat_files_model = DatFilesListModel(self.main_window)
        self.dat_files_model.set_filename_pattern(self.dat_filename_struct_combobox.currentData())
        self.dat_files_table.setModel(self.dat_files_model)

        self.uav_id_model = UavIdsListModel(self.gps_layer_saver)
        self.uav_id_comboBox.setModel(self.uav_id_model)

        self.spectrum_device_model = DeviceListModel()
        self.device_combo_box.setModel(self.spectrum_device_model)

        self.en_win_table_model = EnWindowsTableModel(self.device_combo_box.currentData())
        self.en_windows_table_view.setModel(self.en_win_table_model)
        self.en_windows_table_view.resizeColumnsToContents()
        self.init_gui()

    def init_gui(self):
        self.add_dat_button.clicked.connect(self.dat_files_model.add_files)
        self.rem_dat_button.clicked.connect(lambda: self.dat_files_model.remove_data({
            index.row() for index in self.dat_files_table.selectedIndexes()}))
        self.clr_dat_button.clicked.connect(self.dat_files_model.clr_files)
        self.dat_filename_struct_combobox.currentTextChanged.connect(lambda: self.dat_files_model.set_filename_pattern(
            self.dat_filename_struct_combobox.currentData()))
        self.add_en_win.clicked.connect(self.show_add_en_win_dialog)
        self.rem_en_win.clicked.connect(lambda: self.en_win_table_model.remove_data(
            [index.row() for index in self.en_windows_table_view.selectedIndexes()]))
        self.features_count_label.setText(f"There is: {len(list(self.get_gps_features()))} GNSS points.")
        self.uav_id_comboBox.currentTextChanged.connect(lambda: self.features_count_label.setText(
            f"There is: {len(list(self.get_gps_features()))} GNSS points."))

    def show_add_en_win_dialog(self):
        self.en_win_dialog = AddEnWindowDialogHandle()
        self.en_win_dialog.win_parameter_sgnl.connect(self.update_en_windows_model)
        self.en_win_dialog.show()

    def update_en_windows_model(self, subwindow_dict: dict):
        print("update_en_windows_model: ", subwindow_dict)
        self.en_win_table_model.beginResetModel()
        self.device_combo_box.currentData().add_subwindow(
            subwindow_dict['w_name'], subwindow_dict['subw_name'], subwindow_dict['lhb'], subwindow_dict['rhb'])
        self.en_win_table_model.endResetModel()
        self.en_win_dialog = None

    def get_gps_features(self) -> QgsFeatureIterator:
        layer = self.gps_layer_saver.get_layer()
        request = QgsFeatureRequest().setFilterExpression(f'"UAV_ID" = \'{self.uav_id_comboBox.currentText()}\'')
        return layer.getFeatures(request)

    def load_config(self):
        pass

    def get_config(self):
        pass
