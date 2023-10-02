# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\YandexDisk\Work\ProjectsRepositories\20230821_RousettusDataProcessing\RousettusDataProcessing\GUI\UI\DataProcessing\import_dat_spectrum_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_import_dat_spectrum_widget(object):
    def setupUi(self, import_dat_spectrum_widget):
        import_dat_spectrum_widget.setObjectName("import_dat_spectrum_widget")
        import_dat_spectrum_widget.resize(661, 613)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(import_dat_spectrum_widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox = QtWidgets.QGroupBox(import_dat_spectrum_widget)
        self.groupBox.setMinimumSize(QtCore.QSize(260, 260))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_dat_button = QtWidgets.QPushButton(self.groupBox)
        self.add_dat_button.setMinimumSize(QtCore.QSize(50, 0))
        self.add_dat_button.setMaximumSize(QtCore.QSize(60, 16777215))
        self.add_dat_button.setObjectName("add_dat_button")
        self.horizontalLayout.addWidget(self.add_dat_button)
        self.rem_dat_button = QtWidgets.QPushButton(self.groupBox)
        self.rem_dat_button.setMinimumSize(QtCore.QSize(50, 0))
        self.rem_dat_button.setMaximumSize(QtCore.QSize(60, 16777215))
        self.rem_dat_button.setObjectName("rem_dat_button")
        self.horizontalLayout.addWidget(self.rem_dat_button)
        self.clr_dat_button = QtWidgets.QPushButton(self.groupBox)
        self.clr_dat_button.setMinimumSize(QtCore.QSize(50, 0))
        self.clr_dat_button.setMaximumSize(QtCore.QSize(60, 16777215))
        self.clr_dat_button.setObjectName("clr_dat_button")
        self.horizontalLayout.addWidget(self.clr_dat_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(180, 0))
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.dat_filename_struct_combobox = QtWidgets.QComboBox(self.groupBox)
        self.dat_filename_struct_combobox.setMinimumSize(QtCore.QSize(180, 0))
        self.dat_filename_struct_combobox.setEditable(True)
        self.dat_filename_struct_combobox.setObjectName("dat_filename_struct_combobox")
        self.verticalLayout.addWidget(self.dat_filename_struct_combobox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dat_files_table = QtWidgets.QTableView(self.groupBox)
        self.dat_files_table.setObjectName("dat_files_table")
        self.dat_files_table.horizontalHeader().setCascadingSectionResizes(False)
        self.dat_files_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.dat_files_table)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.timelag_double_spin_box = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.timelag_double_spin_box.setMinimumSize(QtCore.QSize(65, 0))
        self.timelag_double_spin_box.setDecimals(1)
        self.timelag_double_spin_box.setMinimum(-999999.0)
        self.timelag_double_spin_box.setMaximum(999999.0)
        self.timelag_double_spin_box.setSingleStep(0.5)
        self.timelag_double_spin_box.setObjectName("timelag_double_spin_box")
        self.horizontalLayout_5.addWidget(self.timelag_double_spin_box)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(import_dat_spectrum_widget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(260, 260))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.device_combo_box = QtWidgets.QComboBox(self.groupBox_3)
        self.device_combo_box.setMinimumSize(QtCore.QSize(120, 0))
        self.device_combo_box.setMaximumSize(QtCore.QSize(200, 16777215))
        self.device_combo_box.setEditable(True)
        self.device_combo_box.setObjectName("device_combo_box")
        self.horizontalLayout_3.addWidget(self.device_combo_box)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.calibration_curve_label = QtWidgets.QLabel(self.groupBox_3)
        self.calibration_curve_label.setObjectName("calibration_curve_label")
        self.verticalLayout_3.addWidget(self.calibration_curve_label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox.setDecimals(4)
        self.doubleSpinBox.setMinimum(-9999999.0)
        self.doubleSpinBox.setMaximum(9999999.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_2.setDecimals(4)
        self.doubleSpinBox_2.setMinimum(-9999999.0)
        self.doubleSpinBox_2.setMaximum(9999999.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_2)
        self.horizontalLayout_4.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_en_win = QtWidgets.QPushButton(self.groupBox_3)
        self.add_en_win.setMinimumSize(QtCore.QSize(50, 0))
        self.add_en_win.setMaximumSize(QtCore.QSize(100, 16777215))
        self.add_en_win.setObjectName("add_en_win")
        self.horizontalLayout_2.addWidget(self.add_en_win)
        self.rem_en_win = QtWidgets.QPushButton(self.groupBox_3)
        self.rem_en_win.setMinimumSize(QtCore.QSize(50, 0))
        self.rem_en_win.setMaximumSize(QtCore.QSize(100, 16777215))
        self.rem_en_win.setObjectName("rem_en_win")
        self.horizontalLayout_2.addWidget(self.rem_en_win)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.en_windows_table_view = QtWidgets.QTableView(self.groupBox_3)
        self.en_windows_table_view.setObjectName("en_windows_table_view")
        self.verticalLayout_3.addWidget(self.en_windows_table_view)
        self.horizontalLayout_8.addWidget(self.groupBox_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(import_dat_spectrum_widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.UAV_ID_label = QtWidgets.QLabel(self.groupBox_2)
        self.UAV_ID_label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.UAV_ID_label.setObjectName("UAV_ID_label")
        self.horizontalLayout_6.addWidget(self.UAV_ID_label)
        self.uav_id_comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.uav_id_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.uav_id_comboBox.setEditable(False)
        self.uav_id_comboBox.setCurrentText("")
        self.uav_id_comboBox.setObjectName("uav_id_comboBox")
        self.horizontalLayout_6.addWidget(self.uav_id_comboBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.features_count_label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.features_count_label.sizePolicy().hasHeightForWidth())
        self.features_count_label.setSizePolicy(sizePolicy)
        self.features_count_label.setMinimumSize(QtCore.QSize(240, 0))
        self.features_count_label.setObjectName("features_count_label")
        self.verticalLayout_4.addWidget(self.features_count_label)
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.pushButton_4 = QtWidgets.QPushButton(import_dat_spectrum_widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_7.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(import_dat_spectrum_widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_7.addWidget(self.pushButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.retranslateUi(import_dat_spectrum_widget)
        QtCore.QMetaObject.connectSlotsByName(import_dat_spectrum_widget)

    def retranslateUi(self, import_dat_spectrum_widget):
        _translate = QtCore.QCoreApplication.translate
        import_dat_spectrum_widget.setWindowTitle(_translate("import_dat_spectrum_widget", "import_dat_spectrum_widget"))
        self.groupBox.setTitle(_translate("import_dat_spectrum_widget", "add DAT files"))
        self.add_dat_button.setText(_translate("import_dat_spectrum_widget", "Add"))
        self.rem_dat_button.setText(_translate("import_dat_spectrum_widget", "Remove"))
        self.clr_dat_button.setText(_translate("import_dat_spectrum_widget", "Clear"))
        self.label_6.setText(_translate("import_dat_spectrum_widget", "Filename structure"))
        self.label_2.setText(_translate("import_dat_spectrum_widget", "Timelag"))
        self.timelag_double_spin_box.setSuffix(_translate("import_dat_spectrum_widget", "s"))
        self.groupBox_3.setTitle(_translate("import_dat_spectrum_widget", "Energy windows"))
        self.label_3.setText(_translate("import_dat_spectrum_widget", "Device"))
        self.calibration_curve_label.setText(_translate("import_dat_spectrum_widget", "Calibration line:"))
        self.label_4.setText(_translate("import_dat_spectrum_widget", "K = "))
        self.label_5.setText(_translate("import_dat_spectrum_widget", "B ="))
        self.add_en_win.setText(_translate("import_dat_spectrum_widget", "Add window"))
        self.rem_en_win.setText(_translate("import_dat_spectrum_widget", "Remove window"))
        self.groupBox_2.setTitle(_translate("import_dat_spectrum_widget", "Choose GNSS Data"))
        self.label.setText(_translate("import_dat_spectrum_widget", "GNSS data from gps_data layer"))
        self.UAV_ID_label.setText(_translate("import_dat_spectrum_widget", "UAV ID"))
        self.uav_id_comboBox.setToolTip(_translate("import_dat_spectrum_widget", "enter UAV ID"))
        self.features_count_label.setText(_translate("import_dat_spectrum_widget", "There is: 0 GNSS points."))
        self.pushButton_4.setText(_translate("import_dat_spectrum_widget", "Import"))
        self.pushButton.setText(_translate("import_dat_spectrum_widget", "Show preview"))
