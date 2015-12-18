#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot, pyqtSignal

import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class FourPlotsGraphics(pg.GraphicsLayoutWidget):
    def __init__(self, BPMx, BPMy, CMx, CMy, freq, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        self.BPMx = BPMx
        self.BPMy = BPMy
        self.CMx = CMx
        self.CMy = CMy

        BPMx_nb = self.BPMx.shape[0]
        BPMy_nb = self.BPMy.shape[0]
        CMx_nb = self.CMx.shape[0]
        CMy_nb = self.CMy.shape[0]

        CMx_plots = self.addPlot(0, 0)
        CMy_plots = self.addPlot(0, 1)
        BPMx_plots = self.addPlot(1, 0)
        BPMy_plots = self.addPlot(1, 1)

        CMx_plots.disableAutoRange()
        CMy_plots.disableAutoRange()
        BPMx_plots.disableAutoRange()
        BPMy_plots.disableAutoRange()

        self.t = pg.numpy.arange(self.BPMx.shape[1]);
        if freq is not None:
            self.t = self.t/freq

        for i in range(CMx_nb):
            CMx_plots.addItem(
                pg.PlotDataItem(self.t, self.CMx[i, :], pen=(i, CMx_nb))
                )
        for i in range(CMy_nb):
            CMy_plots.addItem(
                pg.PlotDataItem(self.t, self.CMy[i, :], pen=(i, CMy_nb))
                )
        for i in range(BPMx_nb):
            BPMx_plots.addItem(
                pg.PlotDataItem(self.t, self.BPMx[i, :], pen=(i, BPMx_nb))
                )
        for i in range(BPMy_nb):
            BPMy_plots.addItem(
                pg.PlotDataItem(self.t, self.BPMy[i, :], pen=(i, BPMy_nb))
                )

        BPMx_plots.setLabel('bottom', text='time', units='s')
        BPMy_plots.setLabel('bottom', text='time', units='s')
        CMx_plots.setLabel('bottom', text='time', units='s')
        CMy_plots.setLabel('bottom', text='time', units='s')

        # autorange only after plots are added
        BPMx_plots.autoRange()
        BPMy_plots.autoRange()
        CMx_plots.autoRange()
        CMy_plots.autoRange()


class FourPlotsTAGraphics(FourPlotsGraphics):
    def __init__(self, BPMx, BPMy, CMx, CMy, freq, parent=None):
        FourPlotsGraphics.__init__(self, BPMx, BPMy, CMx, CMy, freq, parent)

        max_value = max(self.t)
        self.rgn = []
        for i in range(2):
            for j in range(2):
                self.rgn.append(pg.LinearRegionItem(values=[0.,
                                                            max_value],
                                                    bounds=[0, max_value]
                                                    )
                                )
                self.getItem(i, j).addItem(self.rgn[-1])
                self.rgn[-1].sigRegionChanged.connect(
                    self.__on_region_changed
                    )

    def get_region(self):
        r = self.rgn[0].getRegion()
        begin = max(int(r[0]), 0)
        end = min(int(r[1]), max(self.t))

        begin_sp = pg.numpy.argmin(self.t - begin)
        end_sp = pg.numpy.argmin(self.t - end)

        return begin_sp, end_sp

    @pyqtSlot()
    def __on_region_changed(self):
        r = self.sender().getRegion()
        for i in range(len(self.rgn)):
            for j in range(2):
                self.rgn[i].setRegion(r)


class FourPlotsPickGraphics(FourPlotsGraphics):
    def __init__(self, BPMx, BPMy, CMx, CMy, freq, parent=None):
        FourPlotsGraphics.__init__(self, BPMx, BPMy, CMx, CMy, freq, parent)

        max_value = max(self.t)
        self.inf_line = []

        for i in range(2):
            for j in range(2):
                self.inf_line.append(pg.InfiniteLine(pos=max_value/2.,
                                                     movable=True,
                                                     bounds=[0, max_value]
                                                     )
                                     )
                self.getItem(i, j).addItem(self.inf_line[-1])
                self.inf_line[-1].sigPositionChanged.connect(
                    self.__on_position_changed
                    )

    def get_sample(self):
        return pg.numpy.argmin(abs(self.t - self.inf_line[0].value()))

    @pyqtSlot()
    def __on_position_changed(self):
        v = self.sender().value()
        for i in range(len(self.inf_line)):
            self.inf_line[i].setValue(v)

class TwoPlotsGraphics(pg.GraphicsLayoutWidget):
    xlabel = 'Position'
    units_label = 'm'

    def __init__(self, values00, values10, x, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        self.values00 = values00
        self.values10 = values10
        self.x = x

        self._plot_all()


    def _plot_all(self):
        plot00 = self.addPlot(0, 0)
        plot10 = self.addPlot(1, 0)

        plot00.disableAutoRange()
        plot10.disableAutoRange()

        values00_nb = self.values00.shape[0]
        values10_nb = self.values10.shape[0]

        for i in range(values00_nb):
            plot00.addItem(
                pg.PlotDataItem(self.x,
                                self.values00[i,:],
                                pen=(i, values00_nb)
                                )
                )
        for i in range(values10_nb):
            plot10.addItem(
                pg.PlotDataItem(self.x,
                                self.values10[i,:],
                                pen=(i, values10_nb))
                )

        plot00.setLabel('bottom', text=self.xlabel, units=self.units_label)
        plot10.setLabel('bottom', text=self.xlabel, units=self.units_label)

        # autorange only after plots are added
        plot00.autoRange()
        plot10.autoRange()

    def updateValues(self, values00, values10):
        self.values00 = values00
        self.values10 = values10
        self.removeItem(self.getItem(0, 0))
        self.removeItem(self.getItem(1, 0))
        self._plot_all()


class TwoPlotsPickGraphics(TwoPlotsGraphics):

    frequency_changed = pyqtSignal(float)

    def __init__(self, BPMs, fs, parent=None):
        values00, values10, freqs = self._prepare_values(BPMs['BPMx'],
                                                         BPMs['BPMy'],
                                                         fs)
        self.xlabel = 'Frequency'
        self.units_label = 'Hz'
        TwoPlotsGraphics.__init__(self, values00, values10, freqs, parent)

        max_value = max(freqs)
        self.inf_line = []
        for i in range(2):
            self.inf_line.append(pg.InfiniteLine(pos=max_value/2.,
                                                 movable=True,
                                                 bounds=[0, max_value],
                                                 pen=pg.mkPen(color='k',
                                                              width=3)
                                                 )
                                 )
            self.getItem(i, 0).addItem(self.inf_line[-1])
            self.inf_line[-1].sigPositionChanged.connect(
                self.__on_position_changed
                )

    def get_frequency(self):
        return self.inf_line[0].value()

    def set_frequency(self, value):
        return self.inf_line[0].setValue(value)

    @pyqtSlot()
    def __on_position_changed(self):
        v = self.sender().value()
        for i in range(len(self.inf_line)):
            self.inf_line[i].setValue(v)
        self.frequency_changed.emit(v)

    def _prepare_values(self, input00, input01, fs):
        fftx = pg.numpy.fft.fft(input00, axis=1)
        values00 = pg.numpy.abs(fftx[:,:fftx.shape[1]/2])
        values00[:, 0] = 0

        fftx = pg.numpy.fft.fft(input01, axis=1)
        values10 = pg.numpy.abs(fftx[:,:fftx.shape[1]/2])
        values10[:, 0] = 0

        freqs = pg.numpy.fft.fftfreq(input00.shape[1], 1/fs)
        freqs = freqs[:freqs.size/2]

        return values00, values10, freqs


class OrbitGraphics(pg.GraphicsLayoutWidget):
    def __init__(self, orbit, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        self.orbit = orbit['orbit']
        self.phase = orbit['phase']

        orbit_plot = self.addPlot(0, 0)
        orbit_plot.addItem(pg.PlotDataItem(x=self.phase,
                                           y=self.orbit,
                                           pen=(0, 0, 255)))

    def addSignal(self, phase_th, sine_signal):
        orbit_plot = self.getItem(0, 0)
        orbit_plot.addItem(pg.PlotDataItem(x=phase_th,
                                           y=sine_signal,
                                           pen=(255, 0, 255)))

    def addLine(self, x):
        orbit_plot = self.getItem(0, 0)
        orbit_plot.addLine(x=x, pen=(255,0,0))