#!/usr/bin/env python.
# -*- coding: utf-8 -*-

import time

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow, qApp
from PyQt4 import uic

from mods.core.enumerations import OrbitSourceItems, DataSourceItems, AxisItems


class MainWindow(QMainWindow):
    """MainWindow implements the window to communicate with the user.
       It is written with PyQt4
    """

    # Signals
    execute_clicked = pyqtSignal()
    settings_clicked = pyqtSignal(int, int, int)

    # Attributes
    properties = dict({'axis': 0,
                       'frequency': 0,
                       'data_source': 0,
                       'orbit_source': 0})

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('mods/ui/main_window.ui', self)
        self.setWindowTitle(
                qApp.applicationName() + " v" + qApp.applicationVersion())
        self.reference_orbit = 0

        self.__set_orbite_source_combo()
        self.__set_data_source_combo()
        self.__set_axis_combo()

    # Slots
    @pyqtSlot()
    def on_set_ref_btn_clicked(self):
        if self.orbite_source_combo.currentIndex() == OrbitSourceItems.current_orbit:
            current_time = time.strftime("%d %B %Y, %H:%M:%S")
            self.reference_orbit_text = "The reference orbit is the one "
            + "at {:s}".format(current_time)

        if self.orbite_source_combo.currentIndex() == OrbitSourceItems.time_signal:
            self.reference_orbit_text = "The reference orbit is the orbit "
            + "made out of the analysis of the {:d} "
            + "Hz".format(self.frequency)

        if self.orbite_source_combo.currentIndex() == OrbitSourceItems.load_orbit:
            self.reference_orbit_text = "The reference orbit is the loaded "
            + "orbit"

        self.reference_orbite_text += " (BPM{:s})".format(self.properties.axis)

    @pyqtSlot()
    def on_reset_ref_btn_clicked(self):
        self.reference_orbit_text = "The reference orbit is 0"
        self.reference_orbit = 0

    @pyqtSlot()
    def on_execute_btn_clicked(self):
        self.settings_clicked.emit()

    @pyqtSlot()
    def on_settings_btn_clicked(self):
        self.execute_clicked.emit()

    @pyqtSlot(int)
    def on_orbit_source_combo_currentIndexChanged(self, index):
        self.properties['orbit_source'] = index

    @pyqtSlot(int)
    def on_data_source_combo_currentIndexChanged(self, index):
        self.properties['data_source'] = index

    @pyqtSlot(int)
    def on_axis_combo_currentIndexChanged(self, index):
        self.properties['axis'] = index

    # Private methods
    def __set_orbite_source_combo(self):
        self.orbite_source_combo.insertItem(OrbitSourceItems.current_orbit,
                                            "Current orbit")
        self.orbite_source_combo.insertItem(OrbitSourceItems.time_signal,
                                            "Orbit out of the time signal")
        self.orbite_source_combo.insertItem(OrbitSourceItems.load_orbit,
                                            "Load orbit")

    def __set_data_source_combo(self):
        self.data_source_combo.insertItem(DataSourceItems.text_entry,
                                          "Data from text entry")
        self.data_source_combo.insertItem(DataSourceItems.file_entry,
                                          "Data from file entry")

    def __set_axis_combo(self):
        self.axis_combo.insertItem(AxisItems.x,
                                   "BPMx")
        self.axis_combo.insertItem(AxisItems.y,
                                   "BPMy")
