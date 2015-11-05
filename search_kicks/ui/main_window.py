#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, qApp, QDialog
from PyQt4 import uic

import numpy as np
import pyqtgraph as pg
import scipy.io
import time

from search_kicks import core
from search_kicks.ui import dialogs
from search_kicks.ui.time_analysis_graphics import TimeAnalysisGraphics

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class MainWindow(QMainWindow):
    """MainWindow implements the window to communicate with the user.
       It is written with PyQt4
    """

    BPMx, BPMy, CMx, CMy = [0, 0, 0, 0]
    reference_orbit = 0

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('search_kicks/ui/main_window.ui', self)
        self.setWindowTitle(
            qApp.applicationName() + " v" + qApp.applicationVersion()
            )

        self.__add_message("Application started")


    def __get_orbit_data(self):

        return self.orbit, self.phase, self.tune

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
            filename = dialog.get_filename()
            extension = filename.split('.')[-1]

            loaded = False
            if extension == "mat":
                data = scipy.io.loadmat(filename)
                self.BPMx = data['difforbitX']
                self.BPMy = data['difforbitY']
                self.CMx = data['CMx']
                self.CMy = data['CMy']
                loaded = True
            else:
                Exception("Nothing was imported")
            if loaded:
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
            filename = dialog.get_filename()
            extension = dialog.get_file_extension()
            filename = filename.split('.')[:-1].join() + '.' + extension

            saved = True
            if extension == "mat":
                scipy.io.savemat(filename, {'orbit': self.orbit})
            elif extension == "txt":
                np.savetxt(filename, {'orbit': self.orbit})
            elif extension == "hdf5":
                NotImplementedError()
            else:
                Exception("Nothing was saved")
                saved = False
            if saved:
                self.__add_message("File saved in " + filename)

    @pyqtSlot(bool)
    def on_action_timeanalys_load_fofb_triggered(self, checked=False):
        self.current_mode_label.setText("Time analysis from FOFB")
        self.__add_message("Data loaded from FOFB")

    @pyqtSlot(bool)
    def on_action_timeanalys_load_file_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            extension = filename.split('.')[-1]

            loaded = False
            if extension == "mat":
                data = scipy.io.loadmat(filename)
                sample_nb = data['difforbitX'].shape[1]
                BPMx_nb = data['difforbitX'][0, 0].shape[0]
                BPMy_nb = data['difforbitY'][0, 0].shape[0]
                CMx_nb = data['CMx'][0, 0].shape[0]
                CMy_nb = data['CMy'][0, 0].shape[0]

                self.BPMx = np.zeros((BPMx_nb, sample_nb))
                self.BPMy = np.zeros((BPMy_nb, sample_nb))
                self.CMx = np.zeros((CMx_nb, sample_nb))
                self.CMy = np.zeros((CMy_nb, sample_nb))

                for i in range(sample_nb):
                    for j in range(BPMx_nb):
                        self.BPMx[j, i] = data['difforbitX'][0, i][j, 0]
                    for j in range(BPMy_nb):
                        self.BPMy[j, i] = data['difforbitY'][0, i][j, 0]
                    for j in range(CMx_nb):
                        self.CMx[j, i] = data['CMx'][0, i][j, 0]
                    for j in range(CMy_nb):
                        self.CMy[j, i] = data['CMy'][0, i][j, 0]
                        loaded = True
            else:
                Exception("Nothing was imported")
            if loaded:

                main_graphics_layout = TimeAnalysisGraphics(self.BPMx,
                                                            self.BPMy,
                                                            self.CMx,
                                                            self.CMy)

                self.mainsplitter.widget(0).setParent(None)
                self.mainsplitter.insertWidget(0, main_graphics_layout)
                self.current_mode_label.setText("Time analysis from file")
                self.__add_message("Data loaded from file " + filename)

    @pyqtSlot(bool)
    def on_action_timeanalys_save_triggered(self, checked=False):
        dialog = dialogs.SaveFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.__add_message("File saved in XXX")
