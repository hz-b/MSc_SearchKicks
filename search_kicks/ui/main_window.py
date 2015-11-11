#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, qApp, QDialog, QMessageBox
from PyQt4 import uic

import math
import pyqtgraph as pg
import time

import search_kicks.core as skcore
import search_kicks.tools as sktools
from search_kicks.ui import dialogs
from search_kicks.ui.time_analysis_graphics import (FourPlotsTAGraphics,
                                                    OrbitGraphics)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class MainWindow(QMainWindow):
    """MainWindow implements the window to communicate with the user.
       It is written with PyQt4
    """

    BPMx, BPMy, CMx, CMy = [0, 0, 0, 0]
    reference_orbit = 0
    mode = 0

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('search_kicks/ui/main_window.ui', self)
        self.setWindowTitle(
            qApp.applicationName() + " v" + qApp.applicationVersion()
            )
        self.action_orbit_save.setEnabled(False)
        self.action_timeanalys_save.setEnabled(False)

        self.__add_message("Application started")

    # Slots
    @pyqtSlot()
    def on_execute_btn_clicked(self):
        orbit, phase, tune = self.__get_orbit_data()
        kick_phase, sin_coeff = skcore.get_kick(orbit, phase, tune)

        sinus_signal, phase_th = skcore.build_sinus(kick_phase,
                                                    tune,
                                                    sin_coeff
                                                    )

    @pyqtSlot(bool)
    def on_action_orbit_load_current_bpmx_triggered(self, checked=False):
        self.__set_mode(Mode.orbit, Mode.online, "BPMx")

    @pyqtSlot(bool)
    def on_action_orbit_load_current_bpmy_triggered(self, checked=False):
        self.__set_mode(Mode.orbit, Mode.online, "BPMy")

    @pyqtSlot(bool)
    def on_action_orbit_from_time_data_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            BPMx, BPMy, CMx, CMy = sktools.IO.load_timeanalys(filename)
            dialog = dialogs.PickOrbitDialog(BPMx, BPMy, CMx, CMy)
            if dialog.exec_() == QDialog.Accepted:
                chosen_sample = dialog.get_sample()
                family = dialog.get_family()
                BPM = (BPMx if family == 'BPMx' else BPMy).transpose()
                self.__set_orbit_plot(BPM[chosen_sample, :])
                self.__set_mode(Mode.orbit, Mode.from_time_data, family)
                self.__add_message("Orbit loaded from file {}, "
                                   "sample {}".format(filename, chosen_sample))

    @pyqtSlot(bool)
    def on_action_orbit_load_file_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            self.orbit = sktools.IO.load_orbit(filename)

            self.__set_mode(Mode.orbit, Mode.from_file)
            self.__add_message("File loaded")

    @pyqtSlot(bool)
    def on_action_orbit_load_archiver_triggered(self, checked=False):
        self.__set_mode(Mode.orbit, Mode.archiver)
        self.__add_message("Orbit loaded from the Archiver")

    @pyqtSlot(bool)
    def on_action_orbit_save_triggered(self, checked=False):
        dialog = dialogs.SaveOrbitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            extension = dialog.get_file_extension()
            sktools.IO.save_orbit(filename, extension, self.orbit)
            self.__add_message("File saved in {}".format(filename))

    @pyqtSlot(bool)
    def on_action_timeanalys_load_fofb_triggered(self, checked=False):
        self.__set_mode(Mode.time_analysis, Mode.online)
        self.__add_message("Data loaded from FOFB")

    @pyqtSlot(bool)
    def on_action_timeanalys_load_file_triggered(self, checked=False):
        dialog = dialogs.LoadFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            self.BPMx, self.BPMy, self.CMx, self.CMy = \
                sktools.IO.load_timeanalys(filename)

            self.__set_time_analysis_plot()

            self.__set_mode(Mode.time_analysis, Mode.from_file)
            self.__add_message("Data loaded from file {}".format(filename))

    @pyqtSlot(bool)
    def on_action_timeanalys_save_triggered(self, checked=False):
        dialog = dialogs.SaveFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.get_filename()
            extension = dialog.get_file_extension()

            r = self.mainsplitter.widget(0).rgn1.getRegion()
            begin = max(math.floor(r[0]), 0)
            end = min(math.floor(r[1]), self.BPMx.shape[1])

            if begin >= end:
                QMessageBox.critical(self,
                                     "Selection error",
                                     "The data you selected are non existent. "
                                     "Please proceed again."
                                     )
            else:
                sktools.IO.save_timeanalys(filename,
                                           extension,
                                           self.BPMx[:, begin:end],
                                           self.BPMy[:, begin:end],
                                           self.CMx[:, begin:end],
                                           self.CMy[:, begin:end]
                                           )

                self.__add_message("File saved in {}".format(filename))

    def __add_message(self, message):
        datetime = time.strftime("[%Y/%m/%d %H:%M:%S]")
        self.message_area.addItem(datetime + "\t " + message)
        self.statusBar().showMessage(message)

    def __get_orbit_data(self):

        return self.orbit, self.phase, self.tune

    def __set_time_analysis_plot(self):
        main_graphics_layout = FourPlotsTAGraphics(self.BPMx,
                                                   self.BPMy,
                                                   self.CMx,
                                                   self.CMy)
        self.mainsplitter.widget(0).setParent(None)
        self.mainsplitter.insertWidget(0, main_graphics_layout)

    def __set_orbit_plot(self, BPM):
        main_graphics_layout = OrbitGraphics(BPM)

        self.mainsplitter.widget(0).setParent(None)
        self.mainsplitter.insertWidget(0, main_graphics_layout)

    def __set_mode(self, work_type, source, bpm=''):
        if work_type == Mode.time_analysis:
            self.action_orbit_save.setEnabled(False)
            self.action_timeanalys_save.setEnabled(True)
            if source == Mode.from_file:
                self.current_mode_label.setText("Time analysis from file")
            elif source == Mode.online:
                self.current_mode_label.setText("Time analysis from FOFB")
        elif work_type == Mode.orbit:
            self.action_orbit_save.setEnabled(True)
            self.action_timeanalys_save.setEnabled(False)
            if source == Mode.from_file:
                self.current_mode_label.setText("Search kick from file")
            elif source == Mode.online:
                self.current_mode_label.setText("Search kick from current "
                                                "orbit ({})".format(bpm))
            elif source == Mode.archiver:
                self.current_mode_label.setText("Search kick from Archiver")
            elif source == Mode.from_time_data:
                self.current_mode_label.setText("Search kick from time data "
                                                "({})".format(bpm))


class Mode:
    none, time_analysis, orbit = range(3)
    none, from_file, online, from_time_data, archiver = range(5)
