#!/usr/bin/env python.
# -*- coding: utf-8 -*-

import time

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow, qApp
from PyQt4 import uic

from search_kicks.core.enumerations import OrbitSourceItems, DataSourceItems, AxisItems
from search_kicks import core


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
        uic.loadUi('search_kicks/ui/main_window.ui', self)
        self.setWindowTitle(
            qApp.applicationName() + " v" + qApp.applicationVersion()
            )
        self.reference_orbit = 0


    # Slots

    @pyqtSlot()
    def on_reset_ref_btn_clicked(self):
        self.reference_orbit_text = "The reference orbit is 0"
        self.reference_orbit = 0

    @pyqtSlot()
    def on_execute_btn_clicked(self):
        orbit, phase, tune = self.getOrbitData()
        best_idx, phase_kick = core.get_kick(orbit, phase, tune)
        self.settings_clicked.emit()
