#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog, QFileDialog, qApp
from PyQt4 import QtGui
from PyQt4 import uic


class MetaFileDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Load File")
        self.form_layout = QtGui.QFormLayout(self)

        self.file_edit = QtGui.QLineEdit()
        self.reference_edit = QtGui.QCheckBox()
        self.form_layout.addRow("Load File", self.file_edit)
        self.form_layout.addRow("Set as reference", self.reference_edit)
