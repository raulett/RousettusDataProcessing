import os
import re
import typing
from datetime import datetime

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog


class DatFilesListModel(QAbstractTableModel):
    change_process_finished = pyqtSignal()

    def __init__(self, main_window=None):
        super(DatFilesListModel, self).__init__()
        self._filename_pattern = r''
        self.main_window = main_window
        self._data = {}
        self._headers = ['Files№', 'Path']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        column_name = self._headers[index.column()]
        key = list(self._data.keys())[index.row()]
        if role == Qt.DisplayRole:
            if column_name == 'Files№':
                return len(self._data[key])
            elif column_name == 'Path':
                return key
            else:
                return None
        if role == Qt.ToolTipRole:
            if column_name == 'Path':
                return key
            elif column_name == 'Files№':
                return f"{os.path.basename(self._data[key][0]) if len(self._data[key]) else None} ..."
        if role == Qt.BackgroundRole:
            if self.check_filename_for_pattern(os.path.basename(self._data[key][0])):
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
        files = QFileDialog.getOpenFileNames(parent=None, caption="Open DAT files",
                                             directory="", filter="DAT files (*.dat)")[0]
        worker = AddDatFilesWorker(files, self._data, self.main_window)
        worker.dat_files_finished.connect(self.update_data)
        worker.progress_signal.connect(lambda a: self.main_window.progressBar.setValue(a))
        worker.start()

    def remove_data(self, indexes):
        new_data = {}
        for i, element in enumerate(list(self._data.keys())):
            if i not in indexes:
                new_data[element] = self._data[element]
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def clr_files(self):
        self.beginResetModel()
        self._data = {}
        self.endResetModel()

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
        self.change_process_finished.emit()

    def set_filename_pattern(self, pattern: str):
        self._filename_pattern = pattern

    def check_filename_for_pattern(self, filename):
        find_groups = re.findall(self._filename_pattern, filename)
        print("1: ", find_groups)
        if len(find_groups) > 0:
            find_groups = find_groups[0]
        else:
            return False
        print("2: ", find_groups)
        if len(find_groups) == 3:
            try:
                filename_datetime = datetime.strptime(find_groups[0]+find_groups[1], r'%Y%m%d%H%M%S')
                exp_time = int(find_groups[2])
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False



class AddDatFilesWorker(QThread):
    dat_files_finished = pyqtSignal(dict)
    progress_signal = pyqtSignal(int)

    def __init__(self, files: list, data: dict, parent):
        super().__init__(parent)
        self.files = files
        self.data = data

    def run(self):
        current_progress = 0
        self.progress_signal.emit(current_progress)
        for i, file in enumerate(self.files):
            filepath = os.path.dirname(file)
            if filepath not in self.data.keys():
                self.data[filepath] = []
            if file not in self.data[filepath]:
                self.data[filepath].append(file)
            if int((i + 1) / len(self.files) * 100) != current_progress:
                current_progress = int((i + 1) / len(self.files) * 100)
                self.progress_signal.emit(current_progress)
        self.dat_files_finished.emit(self.data)
