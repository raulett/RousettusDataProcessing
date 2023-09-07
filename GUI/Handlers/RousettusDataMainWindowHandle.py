import os
import configparser

from qgis.PyQt.QtWidgets import QMainWindow, QDialog, QWidget
from qgis.core import *
from qgis.core import QgsProject
from qgis.core import QgsMessageLog

from ...GUI.UI.mainWindow_ui import Ui_MainWindow
from ...tools.get_current_project_name import get_current_project_name
from ...tools.Configurable import Configurable

from ...GUI.Handlers.Help.AboutHandle import AboutHandle
from ...GUI.Handlers.DataProcessingHandlers.GnssImportWindowHandle import GnssImportWindowHandle


class RousettusDataMainWindowHandle(Ui_MainWindow, QMainWindow, Configurable):
    debug = 1
    section_name = 'rousettus_main'

    def __init__(self, parent=None):
        """Constructor."""
        super(RousettusDataMainWindowHandle, self).__init__(parent)
        self.prj_full_path = None
        self.prj_name = None
        self.current_project_path = None
        """Enable and disable functions"""
        self.tab_exist_flags = {}
        self.setupUi(self)
        self.profile_generate_tab = None

        # todo debug project name

        # инициализация конфига
        self.plugin_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-1])
        self.rousettus_config_file = os.path.join(self.plugin_path, 'config.ini')
        self.rousettus_config = configparser.ConfigParser()
        self.load_config()

        self.initGui()

        # Минимизация окна
        # self.setWindowState(self.windowState() | Qt.WindowMinimized)

        # add events handler
        # TODO Борода не работает qgis.core.QgsProject.instance().readProject.connect(self.get_current_project_name)
        QgsProject.instance().readProject.connect(self.prj_changed)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.close_tab(index))
        self.actionAbout_Rousettus.triggered.connect(self.show_about)
        self.actionImport.triggered.connect(lambda: self.add_tab(GnssImportWindowHandle, "Import GNSS Data"))

    def initGui(self):
        # print('Main window init gui')
        # print('main window before get current path')
        self.prj_name, self.current_project_path, self.prj_full_path = get_current_project_name()
        # print('main window prj name {}, current path {}, prj_full_path {}'.format(self.prj_name,
        #                                                                           self.current_project_path,
        #                                                                           self.prj_full_path))
        self.label_prj_name.setText(self.prj_name)
        self.label_prj_name.setToolTip(self.prj_name)
        width = self.label_prj_name.fontMetrics().boundingRect(self.label_prj_name.text()).width()
        self.label_prj_name.setFixedWidth(width + 5)

        self.label_prj_path.setText(self.current_project_path)
        self.label_prj_path.setToolTip(self.current_project_path)

    def show_about(self):
        about_dialog = AboutHandle(self)
        about_dialog.show()

    # Add tabs functions
    # TODO make general function for adding tab (call signal name = "user" button.clicked.connect(
    #  lambda: calluser(name)))
    def add_tab(self, tab_class, tab_name):
        section_name = tab_class.section_name
        if self.debug:
            print("current tab_exist_flags = {}".format(self.tab_exist_flags))
        if self.tab_exist_flags.get(section_name, 0):
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i).section_name == tab_class.section_name:
                    self.tabWidget.setCurrentWidget(self.tabWidget.setCurrentIndex(i))
                    break
        else:
            tab_widget = tab_class(main_window=self)
            if isinstance(tab_widget, Configurable):
                tab_widget.set_config(self.rousettus_config)
            self.tabWidget.addTab(tab_widget, tab_name)
            self.tab_exist_flags[section_name] = 1
            self.tabWidget.setCurrentWidget(tab_widget)
            if 'TABS' not in self.rousettus_config:
                self.rousettus_config['TABS'] = {}
            if section_name:
                self.rousettus_config['TABS'][section_name] = str(True)

    def close_tab(self, current_index):
        if self.debug:
            print("closing wiget is {}, profile generate type is {}".format(self.tabWidget.tabText(current_index),
                                                                            type(
                                                                                self.tabWidget.tabText(current_index))))
        self.tab_exist_flags['{}'.format(self.tabWidget.widget(current_index).section_name)] = 0
        if isinstance(self.tabWidget.widget(current_index), Configurable):
            self.rousettus_config['TABS'][self.tabWidget.currentWidget().section_name] = str(False)
            self.tabWidget.widget(current_index).store_config()
        self.tabWidget.widget(current_index).close()
        self.tabWidget.removeTab(current_index)
        if self.debug:
            print("close_tab func, after delete = {}".format(self.tab_exist_flags))
        self.store_config()
        QgsProject.instance().write()

    # slot for project changed signal
    def prj_changed(self):
        self.initGui()
        tab_widget_count = self.tabWidget.count()
        for i in range(tab_widget_count):
            self.tabWidget.widget(i).init_gui()

        if (len(self.current_project_path.strip()) != 0):
            QgsMessageLog.logMessage("{}. {}".format('main', "project {} loaded".format(self.prj_name)),
                                     "Rousettus_Tool",
                                     level=Qgis.Info)

    # Config store and load
    # load config function
    def load_config(self):
        self.rousettus_config.read(self.rousettus_config_file)
        # TODO Добавить загрузку табов
        # if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("profile_generate",
        #                                                                                 fallback=False):
        #     self.add_profile_generate_tab()
        # if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("flight_plan",
        #                                                                                 fallback=False):
        #     self.add_flight_generate_tab()
        # if 'TABS' in self.rousettus_config and self.rousettus_config['TABS'].getboolean("route_plan", fallback=False):
        #     self.add_route_plan_tab()

    # store config
    def store_config(self):
        for tab_index in range(self.tabWidget.count()):
            self.tabWidget.widget(tab_index).store_config()
        with open(self.rousettus_config_file, 'w') as config_file:
            self.rousettus_config.write(config_file)
        # if self.debug:
        #     print('config sections: ', self.rousettus_config.sections())

    def closeEvent(self, *args, **kwargs):
        # print('close call')
        self.store_config()
        QgsProject.instance().write()
