import os.path
import typing
from datetime import datetime
from functools import reduce

from PyQt5.QtGui import QColor

from ....tools.Configurable import Configurable
from ....tools.constants import datetime_format, default_datetime
from ...UI.DataProcessing.import_gpx_widget_ui import Ui_gpx_import_form
from PyQt5.QtWidgets import QWidget, QFileDialog, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QAbstractListModel, QThread, pyqtSignal
from ....lib.gpxpy import gpxpy


class GpxFileListModel(QAbstractTableModel):
    element_added = pyqtSignal(int)
    adding_process_finished = pyqtSignal()

    def __init__(self):
        super(GpxFileListModel, self).__init__()
        self._added_elements_count = None
        self._total_add_elements_count = None
        self._data = []
        self._headers = ['Filename', 'start_flight', 'end_flight', 'w_points',
                         "s_points", "r_points", 'Filepath']
        self._features_count = {"waypoints": 0, "segment_points": 0, "route_points": 0}

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        column_name = self._headers[index.column()]
        if role == Qt.DisplayRole:
            return self._data[index.row()].get(column_name, "None")
        if role == Qt.ToolTipRole:
            return self._data[index.row()].get(column_name, "None")
        if role == Qt.BackgroundRole:
            if self._data[index.row()].get('success', False):
                return QColor('#ffffff')
            else:
                return QColor('#ff0000')
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return section

    def add_files(self):
        files = QFileDialog.getOpenFileNames(parent=None, caption="Open GPX files",
                                             directory="", filter="GPX files (*.gpx)")[0]
        self._total_add_elements_count = len(files)
        self._added_elements_count = 0
        for file in files:
            gpx_worker = self.GpxFilesAddWorker(file, self)
            gpx_worker.finished.connect(self.append_data)
            gpx_worker.run()

    def append_data(self, result_dict):
        if result_dict.get("Filepath", 0) not in [data.get("Filepath", None) for data in self._data]:
            self.beginResetModel()
            self._data.append(result_dict)
            self.endResetModel()
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))
        self._added_elements_count += 1
        current_progress = int(self._added_elements_count / self._total_add_elements_count * 100)
        self.element_added.emit(current_progress)
        if current_progress == 100:
            self.beginResetModel()
            self._data.sort(key=lambda a: datetime.strptime(a.get('start_flight', default_datetime)
                                                            if a.get('start_flight', default_datetime) is not ('None'
                                                               or None) else default_datetime, datetime_format))
            self.endResetModel()
            self.adding_process_finished.emit()

    def remove_data(self, indexes):
        new_data = []
        for i, element in enumerate(self._data):
            if i not in indexes:
                new_data.append(element)
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def clear_data(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    class GpxFilesAddWorker(QThread):
        finished = pyqtSignal(dict)

        def __init__(self, filename, parent):
            super().__init__(parent)
            self.filename = filename
            self._features_count = {}

        def run(self):
            try:
                with open(self.filename, 'r') as gpx_file:
                    self._features_count["success"] = True
                    gpx_data = gpxpy.parse(gpx_file)
                    wp_points = [wpoint.time for wpoint in gpx_data.waypoints if wpoint.time is not None]
                    try:
                        rp_points = [point.time for point in [route.points for route in gpx_data.routes]
                                     if point.time is not None]
                    except TypeError:
                        rp_points = []
                    try:
                        sp_points = [point.time for point in reduce(lambda a, b: a.extend(b) if (a or b) else [],
                                                                    [segment.points for segment in
                                                                     reduce(
                                                                         lambda a, b: a.extend(b) if (a or b) else [],
                                                                         [track.segments if len(
                                                                             track.segments) > 0 else []
                                                                          for track in gpx_data.tracks])])
                                     if point.time is not None]
                    except TypeError:
                        sp_points = []
                    first_rec_time, last_rec_time = None, None
                    if len(rp_points) > 0:
                        first_rec_time, last_rec_time = rp_points[0], rp_points[-1]
                    elif len(wp_points) > 0:
                        first_rec_time, last_rec_time = wp_points[0], wp_points[-1]
                    elif len(sp_points) > 0:
                        first_rec_time, last_rec_time = sp_points[0], sp_points[-1]

                    self._features_count['start_flight'] = first_rec_time.strftime(
                        datetime_format)[:-4] if isinstance(first_rec_time, datetime) else 'None'
                    self._features_count['end_flight'] = last_rec_time.strftime(
                        datetime_format)[:-4] if isinstance(last_rec_time, datetime) else 'None'
                    self._features_count["w_points"] = len(gpx_data.waypoints)
                    self._features_count['s_points'] = sum([sum([len(segment.points)
                                                                 for segment in track.segments])
                                                            for track in gpx_data.tracks])
                    self._features_count['r_points'] = sum([len(
                        route.points) for route in gpx_data.routes])
            except FileNotFoundError:
                self._features_count["success"] = False
            self._features_count['Filename'] = os.path.basename(self.filename)
            self._features_count['Filepath'] = self.filename
            self.finished.emit(self._features_count)


class GpxFeatureTypes(QAbstractListModel):
    def __init__(self):
        super(GpxFeatureTypes, self).__init__()
        self._data = []

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()].section_name
        if role == Qt.UserRole:
            return self._data[index.row()]


class GpxImportWidgetHandle(Ui_gpx_import_form, QWidget, Configurable):
    section_name = 'import_gpx'

    def __init__(self, main_window=None):
        super(GpxImportWidgetHandle, self).__init__(main_window)
        self.main_window = main_window
        self.setupUi(self)
        self.files_model = GpxFileListModel()
        self.fileTableView.setModel(self.files_model)
        self.init_gui()

    def init_gui(self):
        self.fileTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.files_add_button.clicked.connect(self.add_files)
        self.files_rem_button.clicked.connect(self.remove_table_raws)
        self.files_clr_button.clicked.connect(self.files_model.clear_data)
        self.files_model.element_added.connect(lambda a: self.main_window.progressBar.setValue(a))

    def add_files(self):
        # todo switch interface elements
        self.files_model.add_files()

    def check_time_sequence(self):
        pass

    def remove_table_raws(self):
        selected_rows = {index.row() for index in self.fileTableView.selectedIndexes()}
        self.files_model.remove_data(selected_rows)

    def load_config(self):
        pass

    def store_config(self):
        pass
