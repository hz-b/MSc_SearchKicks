#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal, QString, Qt
from PyQt4 import QtGui

import time
import numpy as np

from search_kicks.ui.graphics import (FourPlotsPickGraphics,
                                      TwoPlotsGraphics,
                                      TwoPlotsPickGraphics)

import search_kicks.tools as sktools
import search_kicks.core as skcore


class DialogWithButtons(QtGui.QDialog):
    """ Custom dialog providing Accepted/Rejected buttons """
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


class MetaFileDialog(DialogWithButtons):
    """ Custom dialog with fileEdit """
    _filename = ""

    def __init__(self, parent=None):
        DialogWithButtons.__init__(self, parent)
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
    """ Extended QLineEdit that emits a `pressed` signal on click """
    pressed = pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)

    def mousePressEvent(self, event):
        self.pressed.emit()


class PickOrbitDialog(DialogWithButtons):
    """ Dialog composed of 4 plot with a value selection tool and a QComboBox
        to select the family too analyze.
    """
    def __init__(self, BPMx, BPMy, CMx, CMy, freq, parent=None):
        DialogWithButtons.__init__(self, parent)

        self.setWindowTitle("Pick an orbit")
        self.form_layout = QtGui.QFormLayout()
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


class PickFrequencyDialog(DialogWithButtons):
    """ Dialog composed of two plots with a value selection tool connected to a
        QDoubleSpinBox.
    """
    def __init__(self, BPM, fs, parent=None):
        DialogWithButtons.__init__(self, parent)

        self.setWindowTitle("Pick a frequency")
        self.form_layout = QtGui.QFormLayout()
        self.freq_picker = TwoPlotsPickGraphics(BPM, fs)
        self.form_layout.addRow(self.freq_picker)
        self.freq_edit = QtGui.QDoubleSpinBox()
        self.freq_edit.setDecimals(6)
        self.form_layout.addRow("Frequency", self.freq_edit)
        self.main_layout.insertLayout(0, self.form_layout)

        self.freq_picker.frequency_changed.connect(self._on_freq_picker_frequency_changed)
        self.freq_edit.valueChanged.connect(self._on_freq_edit_valueChanged)

        self.freq_edit.setValue(self.get_frequency())

    def get_frequency(self):
        return self.freq_picker.get_frequency()

    @pyqtSlot(float)
    def _on_freq_picker_frequency_changed(self, value):
        self.freq_edit.setValue(value)

    @pyqtSlot(float)
    def _on_freq_edit_valueChanged(self, value):
        self.freq_picker.set_frequency(value)


class ShowSinCosDialog(QtGui.QDialog):
    """ Dialog cmposed of two plots that show a sine+cosine which phase can be
        changed.
    """
    maxval = 100
    def __init__(self, valuesX, valuesY, position, phases, tunes, f,
                 parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.valuesX = np.array([valuesX[0], valuesX[1]])
        self.valuesY = np.array([valuesY[0], valuesY[1]])
        self.new_valuesX = self.valuesX
        self.new_valuesY = self.valuesY
        self.phases = phases
        self.tunes = tunes

        self.setWindowTitle("Sine / Cosine for f="+str(f)+"Hz")
        self.form_layout = QtGui.QFormLayout(self)
        self.two_plots = TwoPlotsGraphics(self.valuesX, self.valuesY, position)
        self.form_layout.addRow(self.two_plots)
        self.slider = QtGui.QSlider(Qt.Horizontal)
        self.slider.setRange(-self.maxval, self.maxval)
        self.slider.setSliderPosition(0)
        self.slider_edit = QtGui.QDoubleSpinBox()
        self.slider_edit.setRange(-180, 180)
        self.form_layout.addRow(self.slider_edit, self.slider)

        self.kick_btn = QtGui.QPushButton("Get kick!")
        self.form_layout.addRow(self.kick_btn)

        self.slider.valueChanged.connect(self._on_slider_valueChanged)
        self.slider_edit.valueChanged.connect(self._on_slider_edit_valueChanged)
        self.kick_btn.clicked.connect(self._on_kick_btn_clicked)

    @pyqtSlot(float)
    def _on_slider_valueChanged(self, value):
        v = value/float(self.maxval)*180
        self.slider_edit.setValue(v)
        self._update_graph_phase(v)

    @pyqtSlot(float)
    def _on_slider_edit_valueChanged(self, value):
        self.slider.setValue(int(round(value*self.maxval/180.)))

    @pyqtSlot()
    def _on_kick_btn_clicked(self):
        kick_phX, _ = skcore.get_kick(self.new_valuesX[0,:],
                                      self.phases['BPMx'],
                                      self.tunes['BPMx'])
        kick_phY, _ = skcore.get_kick(self.new_valuesY[0,:],
                                      self.phases['BPMy'],
                                      self.tunes['BPMy'])

        self.two_plots.add_line(kick_phX, 0)
        self.two_plots.add_line(kick_phY, 1)

    def _update_graph_phase(self, angle_deg):
        valuesX = np.copy(self.valuesX)
        valuesY = np.copy(self.valuesY)
        valuesX[0,:], valuesX[1,:] = sktools.maths.rotate(
            self.valuesX[0,:], self.valuesX[1,:], angle_deg, 'deg'
            )
        valuesY[0,:], valuesY[1,:] = sktools.maths.rotate(
            self.valuesY[0,:], self.valuesY[1,:], angle_deg, 'deg'
            )

        self.two_plots.update_values(valuesX, valuesY)
        self.new_valuesX = valuesX
        self.new_valuesY = valuesY
