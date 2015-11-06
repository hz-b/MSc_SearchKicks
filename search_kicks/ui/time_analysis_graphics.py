#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSlot

import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class TimeAnalysisGraphics(pg.GraphicsLayoutWidget):
    def __init__(self, BPMx, BPMy, CMx, CMy, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)
        self.BPMx = BPMx
        self.BPMy = BPMy
        self.CMx = CMx
        self.CMy = CMy

        sample_nb = self.BPMx.shape[1]
        BPMx_nb = self.BPMx.shape[0]
        BPMy_nb = self.BPMy.shape[0]
        CMx_nb = self.CMx.shape[0]
        CMy_nb = self.CMy.shape[0]

        CMx_plots = self.addPlot(0, 0)
        CMx_plots.disableAutoRange()
        self.rgn2 = pg.LinearRegionItem([sample_nb/5., sample_nb/3.])
        CMx_plots.addItem(self.rgn2)

        CMy_plots = self.addPlot(0, 1)
        CMy_plots.disableAutoRange()
        self.rgn4 = pg.LinearRegionItem([sample_nb/5., sample_nb/3.])
        CMy_plots.addItem(self.rgn4)

        BPMx_plots = self.addPlot(1, 0)
        BPMx_plots.disableAutoRange()
        self.rgn1 = pg.LinearRegionItem([sample_nb/5., sample_nb/3.])
        BPMx_plots.addItem(self.rgn1)

        BPMy_plots = self.addPlot(1, 1)
        BPMy_plots.disableAutoRange()
        self.rgn3 = pg.LinearRegionItem([sample_nb/5., sample_nb/3.])
        BPMy_plots.addItem(self.rgn3)

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

        self.rgn1.sigRegionChanged.connect(self.__on_change_rgn)
        self.rgn2.sigRegionChanged.connect(self.__on_change_rgn)
        self.rgn3.sigRegionChanged.connect(self.__on_change_rgn)
        self.rgn4.sigRegionChanged.connect(self.__on_change_rgn)

    @pyqtSlot()
    def __on_change_rgn(self):
        r = self.sender().getRegion()
        self.rgn1.setRegion(r)
        self.rgn2.setRegion(r)
        self.rgn3.setRegion(r)
        self.rgn4.setRegion(r)
