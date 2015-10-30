#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow, qApp, QDialog, QLabel
from PyQt4 import uic

import numpy as np
import time

from search_kicks import core
from search_kicks.ui import dialogs


class MainWindow(QMainWindow):
    """MainWindow implements the window to communicate with the user.
       It is written with PyQt4
    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('search_kicks/ui/main_window.ui', self)
        self.setWindowTitle(
            qApp.applicationName() + " v" + qApp.applicationVersion()
            )
        self.reference_orbit = 0
        self.__add_message("Application started")

    def __get_orbit_data(self):

        return orbit, phase, tune

    def __add_message(self, message):
        datetime = time.strftime("[%Y/%m/%d %H:%M:%S]")
        self.message_area.addItem(datetime + "\t " + message)
        self.statusBar().showMessage(message)

    # Slots
    @pyqtSlot()
    def on_execute_btn_clicked(self):
        orbit, phase, tune = self.__get_orbit_data()
        kick_phase, sin_coeff = core.get_kick(orbit, phase, tune)

        sinus_signal, phase_th = core.build_sinus(kick_phase,
                                                  tune,
                                                  sin_coeff
                                                  )

    @pyqtSlot(bool)
    def on_action_orbit_load_current_bpmx_triggered(self, checked=False):
        self.current_mode_label.setText("Search kick from current orbit "
                                        "(BPMx)")

    @pyqtSlot(bool)
    def on_action_orbit_load_current_bpmy_triggered(self, checked=False):
        self.current_mode_label.setText("Search kick from current orbit "
                                        "(BPMy)")

    @pyqtSlot(bool)
    def on_action_orbit_load_file_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_mode_label.setText("Search kick from file")
            self.__add_message("File loaded")

    @pyqtSlot(bool)
    def on_action_orbit_load_archiver_triggered(self, checked=False):
        self.current_mode_label.setText("Search kick from Archiver")
        self.__add_message("Orbit loaded from the Archiver")

    @pyqtSlot(bool)
    def on_action_orbit_save_triggered(self, checked=False):
        dialog = dialogs.SaveFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.__add_message("File saved in XXX")

    @pyqtSlot(bool)
    def on_action_timeanalys_load_fofb_triggered(self, checked=False):
        self.current_mode_label.setText("Time analysis from FOFB")
        self.__add_message("Data loaded fron FOFB")

    @pyqtSlot(bool)
    def on_action_timeanalys_load_file_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_mode_label.setText("Time analysis from file")
            self.__add_message("Data loaded fron file")

    @pyqtSlot(bool)
    def on_action_timeanalys_save_triggered(self, checked=False):
        dialog = dialogs.SaveFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.__add_message("File saved in XXX")