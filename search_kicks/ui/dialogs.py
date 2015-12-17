#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal, QString, Qt
from PyQt4 import QtGui

import time

from search_kicks.ui.graphics import (FourPlotsPickGraphics,
                                      TwoPlotsPickGraphics)


class MyDialog(QtGui.QDialog):
    _filename = ""

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowTitle("Title")
        self.main_layout = QtGui.QVBoxLayout(self)

        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
            )

        self.main_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


class MetaFileDialog(MyDialog):
    _filename = ""

    def __init__(self, parent=None):
        MyDialog.__init__(self, parent)
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        self.form_layout = QtGui.QFormLayout()

        self.file_edit = LineEditFocus(self)
        self.file_edit.pressed.connect(self.on_file_edit_pressed)
        self.form_layout.addRow("Label", self.file_edit)

        self.main_layout.insertLayout(0, self.form_layout)

        self.file_edit.textChanged.connect(self.__update_accept_btn)

    def get_filename(self):
        return str(self._filename)

    @pyqtSlot()
    def on_file_edit_pressed(self):
        pass

    def __update_accept_btn(self):
        if self.file_edit.text().isEmpty():
            self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)


class LoadFileDialog(MetaFileDialog):
    def __init__(self, parent=None):
        MetaFileDialog.__init__(self, parent)

        self.setWindowTitle("Load File")

        self.form_layout.labelForField(self.file_edit).setText("Load File")

    @pyqtSlot()
    def on_file_edit_pressed(self):
        self._filename = str(
            QtGui.QFileDialog.getOpenFileName(self, "Open File", "",
                                              "Data files (*.mat *.hdf5 *.txt)"
                                              )
            )
        self.file_edit.setText(self._filename)


class SaveFileDialog(MetaFileDialog):
    _file_extension = ""

    def __init__(self, parent=None):
        MetaFileDialog.__init__(self, parent)

        self.setWindowTitle("Save File")

        self.form_layout.labelForField(self.file_edit).setText("Save as")
        self.type_edit = QtGui.QComboBox()
        self.type_edit.addItem(".mat")
        self.type_edit.addItem(".hdf5")
        self.form_layout.insertRow(0, "File type", self.type_edit)

        self._file_extension = self.type_edit.currentText()[1:]

    def get_file_extension(self):
        return str(self._file_extension)

    @pyqtSlot()
    def on_file_edit_pressed(self):
        file_default = time.strftime("%Y-%m-%d_%H-%M-%S")+"_untitled"
        file_default += self.type_edit.currentText()

        self._filename = QtGui.QFileDialog.getSaveFileName(
            self, "Save As", file_default, "Data files (*.mat *.hdf5 *.txt)"
            )
        self.file_edit.setText(self._filename)

    @pyqtSlot(QString)
    def on_type_edit_activated(self, text):
        self._file_extension = text[1:]  # remove the '.'


class LoadOrbitDialog(LoadFileDialog):
    def __init__(self, parent=None):
        LoadFileDialog.__init__(self, parent)
        self.reference_edit = QtGui.QCheckBox()
        self.form_layout.addRow("Set as reference", self.reference_edit)


class SaveOrbitDialog(SaveFileDialog):
    def __init__(self, parent=None):
        SaveFileDialog.__init__(self, parent)
        self.type_edit.addItem(".txt")


class LineEditFocus(QtGui.QLineEdit):
    pressed = pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)

    def mousePressEvent(self, event):
        self.pressed.emit()


class PickOrbitDialog(MyDialog):
    def __init__(self, BPMx, BPMy, CMx, CMy, freq, parent=None):
        MyDialog.__init__(self, parent)

        self.setWindowTitle("Pick an orbit")
        self.form_layout = QtGui.QFormLayout(self)
        self.sample_picker = FourPlotsPickGraphics(BPMx, BPMy, CMx, CMy, freq)
        self.form_layout.addRow(self.sample_picker)
        self.family_edit = QtGui.QComboBox()
        self.family_edit.addItem('BPMx')
        self.family_edit.addItem('BPMy')
        self.form_layout.addRow("Family to pick", self.family_edit)

        self.main_layout.insertLayout(0, self.form_layout)

    def get_sample(self):
        return self.sample_picker.get_sample()

    def get_family(self):
        return str(self.family_edit.currentText())


class PickFrequencyDialog(MyDialog):
    def __init__(self, BPM, fs, parent=None):
        MyDialog.__init__(self, parent)

        self.setWindowTitle("Pick a frequency")
        self.form_layout = QtGui.QFormLayout(self)
        self.freq_picker = TwoPlotsPickGraphics(BPM, fs)
        self.form_layout.addRow(self.freq_picker)
        self.freq_edit = QtGui.QDoubleSpinBox()
        self.freq_edit.setDecimals(6)
        self.form_layout.addRow("Frequency", self.freq_edit)
        self.main_layout.insertLayout(0, self.form_layout)

        self.freq_picker.frequency_changed.connect(self.change_frequency)
        self.freq_edit.valueChanged.connect(self.freq_value_changed)

        self.freq_edit.setValue(self.get_frequency())

    def get_frequency(self):
        return self.freq_picker.get_frequency()

    @pyqtSlot(float)
    def change_frequency(self, value):
        self.freq_edit.setValue(value)

    @pyqtSlot(float)
    def freq_value_changed(self, value):
        self.freq_picker.set_frequency(value)