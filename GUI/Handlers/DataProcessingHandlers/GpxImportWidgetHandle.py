import os.path
import time
import typing
from datetime import datetime
from functools import reduce
from threading import Thread
from queue import Queue

import qgis
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QFileDialog, QHeaderView, QDialog, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QAbstractListModel, QThread, pyqtSignal, QMutex, \
    QRunnable, QThreadPool
from qgis.core import QgsFeature, QgsPoint

from ....tools.Configurable import Configurable
from ....tools.constants import datetime_format, default_datetime
from ...UI.DataProcessing.import_gpx_widget_ui import Ui_gpx_import_form
from ....lib.gpxpy import gpxpy
from ....tools.VectorLayerSaverGPKG.GpsLayerSaverGPKG import GpsLayerSaverGPKG


class GpxFileListModel(QAbstractTableModel):
    element_added = pyqtSignal(int)
    adding_process_finished = pyqtSignal()
    change_process_finished = pyqtSignal()

    def __init__(self, parent=None):
        super(GpxFileListModel, self).__init__()
        self.mutex = QMutex()
        self.parent = parent
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

    def get_count_data(self, geometry_type):
        return self._features_count[geometry_type]

    def add_files(self):
        print("call_add_files")
        files = QFileDialog.getOpenFileNames(parent=None, caption="Open GPX files",
                                             directory="", filter="GPX files (*.gpx)")[0]
        self._total_add_elements_count = len(files)
        self._added_elements_count = 0
        for file in files:
            gpx_worker = GpxFilesAddWorker(file, self.parent)
            gpx_worker.finished.connect(self.append_data)
            gpx_worker.parse_gpx()
            gpx_worker.start()

    def append_data(self, result_dict):
        if result_dict.get("Filepath", 0) not in [data.get("Filepath", None) for data in self._data]:
            self.beginResetModel()
            self._data.append(result_dict)
            self.endResetModel()
            self.dataChanged.emit(self.index(0, 0), self.index(
                self.rowCount() - 1, self.columnCount() - 1))
        self._added_elements_count += 1
        current_progress = int(self._added_elements_count / self._total_add_elements_count * 100)
        self._features_count["waypoints"] += result_dict.get("w_points", 0)
        self._features_count["segment_points"] += result_dict.get('s_points', 0)
        self._features_count["route_points"] += result_dict.get("r_points", 0)
        self.element_added.emit(current_progress)
        if current_progress == 100:
            self.beginResetModel()
            self._data.sort(key=lambda a: datetime.strptime(a.get('start_flight', default_datetime) if a.get(
                'start_flight', default_datetime) is not ('None' or None) else default_datetime, datetime_format))
            self.endResetModel()
            self.adding_process_finished.emit()
            self.change_process_finished.emit()

    def remove_data(self, indexes):
        new_data = []
        for i, element in enumerate(self._data):
            if i not in indexes:
                new_data.append(element)
            else:
                self._features_count["waypoints"] -= element["w_points"]
                self._features_count["segment_points"] -= element['s_points']
                self._features_count["route_points"] -= element["r_points"]
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
        self.change_process_finished.emit()

    def clear_data(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    def check_time_sequence(self):
        b_time = time.time() * 1000
        self.beginResetModel()
        prev_element = None
        if len(self._data) < 2:
            return
        for i, element in enumerate(self._data):
            if element.get('start_flight', None) is ('None' or None):
                element['success'] = False
                continue
            if prev_element is None:
                prev_element = element
                continue
            if i == len(self._data) - 1:
                prev_right_lim = datetime.strptime(prev_element.get('end_flight'), datetime_format)
                current_left_lim = datetime.strptime(element.get('start_flight'), datetime_format)
                if prev_right_lim > current_left_lim:
                    element['success'] = False
                continue
            if ((datetime.strptime(prev_element.get('end_flight'), datetime_format) >
                 datetime.strptime(element.get('start_flight'), datetime_format)) or
                    (datetime.strptime(element.get('end_flight'), datetime_format) >
                     datetime.strptime(self._data[i + 1].get('start_flight'), datetime_format))):
                element['success'] = False
                continue
            else:
                prev_element = element
        self.endResetModel()
        print("end check_time_sequence, time: ", time.time() * 1000 - b_time)

    def get_data(self):
        return self._data


class GpxFilesAddWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, filename, parent):
        super().__init__(parent)
        self.filename = filename
        self.gpx_data = None
        self._features_count = {}

    def parse_gpx(self):
        try:
            with open(self.filename, 'r') as gpx_file:
                # self.mutex.lock()
                self.gpx_data = gpxpy.parse(gpx_file)
                # self.mutex.unlock()
        except FileNotFoundError as e:
            print("error read file: ", e)

    def run(self):
        self._features_count["success"] = True
        wp_points = [wpoint.time for wpoint in self.gpx_data.waypoints if wpoint.time is not None]
        try:
            rp_points = [point.time for point in [route.points for route in self.gpx_data.routes]
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
                                                              for track in self.gpx_data.tracks])])
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
        self._features_count["w_points"] = len(wp_points)
        self._features_count['s_points'] = len(sp_points)
        self._features_count['r_points'] = len(rp_points)
        self._features_count['Filename'] = os.path.basename(self.filename)
        self._features_count['Filepath'] = self.filename
        self.finished.emit(self._features_count)


class GpxGeometriesTypesList(QAbstractListModel):
    def __init__(self, files_list_model: GpxFileListModel):
        super(GpxGeometriesTypesList, self).__init__()
        self._data = ["waypoints", "segment_points", "route_points"]
        self.files_list_model = files_list_model

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.UserRole:
            return self.files_list_model.get_count_data(self._data[index.row()])

    def get_max_element_index(self):
        return max(range(len(self._data)),
                   key=lambda i: self.files_list_model.get_count_data(self._data.__getitem__(i)))


class UavIdsListModel(QAbstractListModel):
    def __init__(self, gps_layer_saver: GpsLayerSaverGPKG):
        super(UavIdsListModel, self).__init__()
        self._layer_saver = gps_layer_saver
        self._data = []
        self._data_changed_handle()
        self._data_provider = gps_layer_saver.get_layer().dataProvider()
        # todo rem debug
        print("UavIdsListModel data: ", self._data)
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
        print("UavIdsListModel _data_changed_handle data: ", self._data, "len: ", len(self._data))
        if len(self._data) == 0:
            self._data.append('UAV ID')
        self.endResetModel()


class GpxImportWidgetHandle(Ui_gpx_import_form, QWidget, Configurable):
    section_name = 'import_gpx'

    def __init__(self, main_window=None):
        super(GpxImportWidgetHandle, self).__init__(main_window)
        self.uav_id_model = None
        self.gps_layer_saver = None
        self.main_window = main_window
        self.setupUi(self)
        self.files_model = GpxFileListModel(self)
        self.fileTableView.setModel(self.files_model)
        self.feature_type_model = GpxGeometriesTypesList(self.files_model)
        self.feature_type_comboBox.setModel(self.feature_type_model)
        self.gps_layer_saver = GpsLayerSaverGPKG(self.main_window)
        self.renew_uav_id_model()
        self.init_gui()

    def init_gui(self):
        self.fileTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.files_add_button.clicked.connect(self.files_model.add_files)
        self.files_rem_button.clicked.connect(lambda: self.files_model.remove_data({
            index.row() for index in self.fileTableView.selectedIndexes()}))
        self.files_clr_button.clicked.connect(self.files_model.clear_data)
        self.files_model.element_added.connect(lambda a: self.main_window.progressBar.setValue(a))
        self.import_gpx_button.clicked.connect(self.import_files_data)
        self.files_model.adding_process_finished.connect(self.files_model.check_time_sequence)
        self.feature_type_comboBox.currentIndexChanged.connect(lambda: self.features_count_label.setText(
            "There is: {} geometries with time data.".format(self.feature_type_comboBox.currentData())))
        self.files_model.change_process_finished.connect(lambda: self.features_count_label.setText(
            "There is: {} geometries with time data.".format(self.feature_type_comboBox.currentData())))
        self.files_model.change_process_finished.connect(self.set_maximum_geometry_type)
        self.gps_layer_saver.get_layer().committedFeaturesRemoved.connect(self.renew_uav_id_model)

    def import_files_data(self):
        model_data = self.files_model.get_data()
        filenames = [record.get("Filepath", None) for record in model_data if record.get('success', False)]
        worker = GpxFilesImportToLayerWorker(filenames, self, self.gps_layer_saver,
                                             self.feature_type_comboBox.currentIndex(),
                                             self.uav_id_comboBox.currentText())
        worker.file_loaded.connect(lambda a: self.main_window.progressBar.setValue(a))
        worker.added_points.connect(self.points_added_message)
        worker.finished.connect(self.renew_uav_id_model)
        worker.run()

    def set_maximum_geometry_type(self):
        self.feature_type_comboBox.setCurrentIndex(self.feature_type_model.get_max_element_index())

    def points_added_message(self, total_added_points, total_ignored_points):
        msg = QMessageBox()
        msg.setWindowTitle("Points adding finished")
        msg.setText(f"{total_added_points} was added.\n {total_ignored_points} duplicates was ignored.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def renew_uav_id_model(self):
        print("catched renew_uav_id_model event")
        self.uav_id_model = UavIdsListModel(self.gps_layer_saver)
        self.uav_id_comboBox.setModel(self.uav_id_model)
        self.uav_id_comboBox.repaint()

    def load_config(self):
        pass

    def store_config(self):
        pass


class GpxFilesImportToLayerWorker(QThread):
    finished = pyqtSignal()
    added_points = pyqtSignal(int, int)
    file_loaded = pyqtSignal(int)

    def __init__(self, filenames: list, parent, vector_layer_saver: GpsLayerSaverGPKG, geometry_type, uav_id):
        super().__init__(parent)
        self.filenames = filenames
        self.layer_saver = vector_layer_saver
        self.mutex = QMutex()
        self.geometry_type = geometry_type
        self.uav_id = uav_id

    def run(self):
        progress_counter = 0
        total_count = len(self.filenames)
        print("run GpxFilesImportToLayerWorker, uav_id: ", self.uav_id)
        self.file_loaded.emit(int(progress_counter/total_count * 100))
        total_added_points = 0
        total_ignored_points = 0
        for filename in self.filenames:
            with open(filename, 'r') as file:
                print(file)
                self.mutex.lock()
                gpx_file = gpxpy.parse(file)
                self.mutex.unlock()
            field_scheme = self.layer_saver.get_layer().fields()
            feature_list = []
            print("len(gpx_file.tracks): ", len(gpx_file.tracks))
            print(self.geometry_type)
            print(self.uav_id)
            if self.geometry_type == 0:  # waypoints
                points = [wpoint for wpoint in gpx_file.waypoints if wpoint.time is not None]
            elif self.geometry_type == 1:  # segment_points
                print("enter segment points condition")
                try:
                    print("try segment points condition done")
                    # print([track.segments if len(track.segments) > 0 else [] for track in gpx_file.tracks])
                    points = [point for point in reduce(lambda a, b: a.extend(b) if (a or b) else [],
                                                        [segment.points for segment in
                                                         reduce(
                                                             lambda a, b: a.extend(b) if (a or b) else [],
                                                             [track.segments if len(
                                                                 track.segments) > 0 else []
                                                              for track in gpx_file.tracks])])
                              if point.time is not None]

                except TypeError:
                    print("segment points condition exception")
                    points = []
            else:  # route_Points
                print("enter route_Points condition done")
                try:
                    points = [point for point in [route.points for route in gpx_file.routes]
                              if point.time is not None]
                except TypeError:
                    points = []
            print("len of points", len(points))
            point_times = []
            ignored_points_count = 0
            for point in points:
                point_time = str(point.time)
                if point_time in point_times:
                    ignored_points_count += 1
                    continue
                else:
                    point_times.append(point_time)
                feature = QgsFeature()
                feature.setFields(field_scheme)
                feature.setAttribute('DATETIME', point_time)
                feature.setAttribute('LON', point.longitude)
                feature.setAttribute('LAT', point.latitude)
                feature.setAttribute('ALT', point.elevation)
                feature.setAttribute('UAV_ID', self.uav_id)
                feature.setAttribute('IS_SERVICE', False)
                feature.setAttribute('FILENAME', filename)
                feature.setGeometry(QgsPoint(point.longitude, point.latitude, point.elevation))
                feature_list.append(feature)
                # print("feat.attr(DATETIME): ", feature.attribute('DATETIME'))
            print("len of feat_list", len(feature_list))
            added_points, ignored_points = self.layer_saver.add_features_to_layer(feature_list, filename, self.uav_id)
            total_added_points += added_points
            total_ignored_points += ignored_points_count + ignored_points
            progress_counter += 1
            self.file_loaded.emit(int(progress_counter/total_count * 100))
        self.added_points.emit(total_added_points, total_ignored_points)
        self.finished.emit()
