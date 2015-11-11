#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot

import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class FourPlotsGraphics(pg.GraphicsLayoutWidget):
    def __init__(self, BPMx, BPMy, CMx, CMy, parent=None):
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

        for i in range(CMx_nb):
            CMx_plots.addItem(
                pg.PlotDataItem(self.CMx[i, :], pen=(i, CMx_nb))
                )
        for i in range(CMy_nb):
            CMy_plots.addItem(
                pg.PlotDataItem(self.CMy[i, :], pen=(i, CMy_nb))
                )
        for i in range(BPMx_nb):
            BPMx_plots.addItem(
                pg.PlotDataItem(self.BPMx[i, :], pen=(i, BPMx_nb))
                )
        for i in range(BPMy_nb):
            BPMy_plots.addItem(
                pg.PlotDataItem(self.BPMy[i, :], pen=(i, BPMy_nb))
                )
        # autorange only after plots are added
        BPMx_plots.autoRange()
        BPMy_plots.autoRange()
        CMx_plots.autoRange()
        CMy_plots.autoRange()


class FourPlotsTAGraphics(FourPlotsGraphics):
    rgn = []

    def __init__(self, BPMx, BPMy, CMx, CMy, parent=None):
        FourPlotsGraphics.__init__(self, BPMx, BPMy, CMx, CMy, parent)

        sample_nb = self.BPMx.shape[1]

        for i in range(2):
            for j in range(2):
                self.rgn.append(pg.LinearRegionItem(values=[sample_nb/5.,
                                                            sample_nb/3.],
                                                    bounds=[0, sample_nb]
                                                    )
                                )
                self.getItem(i, j).addItem(self.rgn[-1])
                self.rgn[-1].sigRegionChanged.connect(
                    self.__on_region_changed
                    )

    @pyqtSlot()
    def __on_region_changed(self):
        r = self.sender().getRegion()
        for i in range(len(self.rgn)):
            for j in range(2):
                self.rgn[i].setRegion(r)


class FourPlotsPickGraphics(FourPlotsGraphics):
    inf_line = []

    def __init__(self, BPMx, BPMy, CMx, CMy, parent=None):
        FourPlotsGraphics.__init__(self, BPMx, BPMy, CMx, CMy, parent)

        sample_nb = self.BPMx.shape[1]

        for i in range(2):
            for j in range(2):
                self.inf_line.append(pg.InfiniteLine(pos=sample_nb/2.,
                                                     movable=True,
                                                     bounds=[0, sample_nb]
                                                     )
                                     )
                self.getItem(i, j).addItem(self.inf_line[-1])
                self.inf_line[-1].sigPositionChanged.connect(
                    self.__on_position_changed
                    )

    def get_sample(self):
        return int(round(self.inf_line[0].value()))

    @pyqtSlot()
    def __on_position_changed(self):
        v = round(self.sender().value())
        for i in range(len(self.inf_line)):
            self.inf_line[i].setValue(v)


class OrbitGraphics(pg.GraphicsLayoutWidget):
    def __init__(self, BPM, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        self.BPM = BPM

        orbit_plot = self.addPlot(0)
        orbit_plot.addItem(pg.PlotDataItem(self.BPM, pen=(0,0,255)))
