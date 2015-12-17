#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, qApp, QDialog, QMessageBox
from PyQt4 import uic

import pyqtgraph as pg
import time
import scipy.io  # FIXME: to be removed

import search_kicks.core as skcore
import search_kicks.tools as sktools
from search_kicks.ui import dialogs
from search_kicks.ui.graphics import (FourPlotsTAGraphics,
                                      OrbitGraphics)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class MainWindow(QMainWindow):
    """MainWindow implements the window to communicate with the user.
       It is written with PyQt4
    """

    time_analysis = dict({'BPMx': 0,
                          'BPMy': 0,
                          'CMx': 0,
                          'CMy': 0,
                          'Fs': 0,
                          'BPM_names': 0
                          })
    orbit = dict({'orbit': 0,
                  'phase': 0,
                  'tune': 0
                  })
    activeBPMs = dict({'BPMx': 0,
                       'BPMy': 0
                       })
    phases = dict({'BPMx': 0,
                   'BPMy': 0
                   })
    tunes = dict({'BPMx': 0,
                  'BPMy': 0
                  })

    reference_orbit = 0
    mode = 0

    def __init__(self, pyml, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('search_kicks/ui/main_window.ui', self)
        self.setWindowTitle(
            qApp.applicationName() + " v" + qApp.applicationVersion()
            )
        self.action_orbit_save.setEnabled(False)
        self.action_timeanalys_save.setEnabled(False)

        self.pyml = pyml

        self.activeBPMs['BPMx'] = pyml.getActiveIdx('BPMx')
        self.activeBPMs['BPMy'] = pyml.getActiveIdx('BPMy')

        # FIXME: Hardcoded here, to be removed
        phases_mat = scipy.io.loadmat('phases.mat')
        self.phases['BPMx'] = phases_mat['PhaseX'][:, 0]
        self.phases['BPMy'] = phases_mat['PhaseZ'][:, 0]
        self.tunes['BPMx'] = 17.8509864542659
        self.tunes['BPMy'] = 6.74232980750181

        self.__add_message("Application started")

    # Slots
    @pyqtSlot()
    def on_execute_btn_clicked(self):
        if self.mode == Mode.orbit:
            kick_phase, sin_coeff = skcore.get_kick(self.orbit['orbit'],
                                                    self.orbit['phase'],
                                                    self.orbit['tune'])

            sinus_signal, phase_th = skcore.build_sinus(kick_phase,
                                                        self.orbit['tune'],
                                                        sin_coeff)
            self.main_graphics_layout.addSignal(phase_th, sinus_signal*3)
            self.main_graphics_layout.addLine(x=kick_phase)

        elif self.mode == Mode.time_analysis:
            start, end = self.main_graphics_layout.get_region()
            BPMs = dict()
            BPMs['BPMx'] = self.time_analysis['BPMx'][self.activeBPMs['BPMx']]
            BPMs['BPMy'] = self.time_analysis['BPMy'][self.activeBPMs['BPMy']]

            dialog = dialogs.PickFrequencyDialog(BPMs,
                                                 self.time_analysis['Fs'],
                                                 )
            if dialog.exec_() == QDialog.Accepted:
                frequency = dialog.get_frequency()
                print(frequency)



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
            BPM = dict()
            BPM['BPMx'], BPM['BPMy'], CMx, CMy, \
                BPMs_names, freq = sktools.IO.load_timeanalys(filename)
            dialog = dialogs.PickOrbitDialog(BPM['BPMx'], BPM['BPMy'],
                                             CMx, CMy, freq)
            if dialog.exec_() == QDialog.Accepted:
                chosen_sample = dialog.get_sample()
                family = dialog.get_family()

                if BPM[family].shape[0] == 128:
                    self.orbit['orbit'] = \
                        BPM[family][self.activeBPMs[family],chosen_sample]\
                        .transpose()
                else:
                    self.orbit['orbit'] = \
                        BPM[family][:,chosen_sample]\
                        .transpose()
                self.orbit['phase'] = self.phases[family]
                self.orbit['tune'] = self.tunes[family]
                self.__set_orbit_plot()
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

            self.time_analysis['BPMx'], \
                self.time_analysis['BPMy'], \
                self.time_analysis['CMx'], \
                self.time_analysis['CMy'], \
                self.time_analysis['BPMs_names'], \
                self.time_analysis['Fs'] = \
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

            begin, end = self.main_grahics_layout.get_region()

            if begin >= end:
                QMessageBox.critical(self,
                                     "Selection error",
                                     "The data you selected are non existent. "
                                     "Please proceed again."
                                     )
            else:
                sktools.IO.save_timeanalys(
                    filename,
                    extension,
                    self.time_analysis['BPMx'][:, begin:end],
                    self.time_analysis['BPMy'][:, begin:end],
                    self.time_analysis['CMx'][:, begin:end],
                    self.time_analysis['CMy'][:, begin:end]
                    )

                self.__add_message("File saved in {}".format(filename))

    def __add_message(self, message):
        datetime = time.strftime("[%Y/%m/%d %H:%M:%S]")
        self.message_area.addItem(datetime + "\t " + message)
        self.statusBar().showMessage(message)

    def __set_time_analysis_plot(self):
        self.main_graphics_layout.setParent(None)
        self.main_graphics_layout = FourPlotsTAGraphics(
            self.time_analysis['BPMx'],
            self.time_analysis['BPMy'],
            self.time_analysis['CMx'],
            self.time_analysis['CMy'],
            self.time_analysis['Fs'])
        self.mainsplitter.insertWidget(0, self.main_graphics_layout)

    def __set_orbit_plot(self):
        self.main_graphics_layout.setParent(None)
        self.main_graphics_layout = OrbitGraphics(self.orbit)
        self.mainsplitter.insertWidget(0, self.main_graphics_layout)

    def __set_mode(self, work_type, source, family=''):
        self.mode = work_type
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
                                                "orbit ({})".format(family))
            elif source == Mode.archiver:
                self.current_mode_label.setText("Search kick from Archiver")
            elif source == Mode.from_time_data:
                self.current_mode_label.setText("Search kick from time data "
                                                "({})".format(family))


class Mode:
    none, time_analysis, orbit = range(3)
    none, from_file, online, from_time_data, archiver = range(5)
