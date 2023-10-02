from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QDialog, QToolTip

from ....UI.DataProcessing.AddEnWindowDialog_ui import Ui_AddEnWindowDialog


class AddEnWindowDialogHandle(Ui_AddEnWindowDialog, QDialog):
    win_parameter_sgnl = pyqtSignal(dict)

    def __init__(self):
        super(AddEnWindowDialogHandle, self).__init__()
        self.setupUi(self)
        self.add_button.clicked.connect(self.accept_button_handle)
        self.cancel_button.clicked.connect(self.close)

    def accept_button_handle(self):
        if (len(self.win_name_line.text()) > 0
                and len(self.subwin_name_line.text()) > 0
                and self.lhb_spinbox.value() < self.rhb_spinbox.value()):
            self.win_parameter_sgnl.emit({"w_name": self.win_name_line.text(),
                                          "subw_name": self.subwin_name_line.text(),
                                          "lhb": self.lhb_spinbox.value(),
                                          "rhb": self.rhb_spinbox.value()})
            self.close()
        else:
            QToolTip.setFont(QFont('Arial', 10))
            QToolTip.showText(QCursor.pos(),
                              '''<p align="left">Window and Subwindow  names should be filled.
                              Right border should be larger than the left one.</p>''')
