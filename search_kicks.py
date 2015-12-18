#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
import matplotlib
matplotlib.use("Qt4Agg")
from search_kicks import ui

import PyML


__author__ = "Olivier CHURLAUD"
__version__ = "0.1.0"
__maintainer__ = ""
__email__ = "olivier.churlaud@helmholtz-berlin.de"
__status__ = "Development"

app = QtGui.QApplication(sys.argv)
app.setApplicationName("SearchKicks")
app.setApplicationVersion("0.1.0")
app.setWindowIcon(QtGui.QIcon("search_kicks/ui/bessy.gif"))

pyml = PyML.PyML()
pyml.setao(pyml.loadFromExtern('external/bessyIIinit.py', 'ao'))

main_window = ui.MainWindow(pyml)

main_window.show()
sys.exit(app.exec_())
