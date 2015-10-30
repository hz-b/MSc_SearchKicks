#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4 import QtGui


class MetaFileDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowTitle("Title")
        self.form_layout = QtGui.QFormLayout()

        self.file_edit = LineEditFocus(self)
        self.file_edit.pressed.connect(self.on_file_edit_pressed)
        self.form_layout.addRow("Label", self.file_edit)

        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
            )

        self.main_layout = QtGui.QVBoxLayout(self)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @pyqtSlot()
    def on_file_edit_pressed(self):
        pass


class LoadFileDialog(MetaFileDialog):
    def __init__(self, parent=None):
        MetaFileDialog.__init__(self, parent)

        self.setWindowTitle("Load File")

        self.form_layout.labelForField(self.file_edit).setText("Load File")
        self.reference_edit = QtGui.QCheckBox()
        self.form_layout.addRow("Set as reference", self.reference_edit)

    @pyqtSlot()
    def on_file_edit_pressed(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open File")
        self.file_edit.setText(file_name)


class SaveFileDialog(MetaFileDialog):
    def __init__(self, parent=None):
        MetaFileDialog.__init__(self, parent)

        self.setWindowTitle("Save File")

        self.form_layout.labelForField(self.file_edit).setText("Save as")
        self.type_edit = QtGui.QComboBox()
        self.type_edit.addItem(".mat")
        self.type_edit.addItem(".txt")
        self.type_edit.addItem(".hdf5")
        self.form_layout.addRow("File type", self.type_edit)

    @pyqtSlot()
    def on_file_edit_pressed(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As")
        self.file_edit.setText(file_name)


class LineEditFocus(QtGui.QLineEdit):
    pressed = pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)

    def mousePressEvent(self, event):
        self.pressed.emit()
