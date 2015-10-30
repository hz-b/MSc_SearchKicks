#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QApplication
import matplotlib
matplotlib.use("Qt4Agg")
from search_kicks import ui


__author__ = "Olivier CHURLAUD"
__version__ = "0.1.0"
__maintainer__ = ""
__email__ = "olivier.churlaud@helmholtz-berlin.de"
__status__ = "Development"

app = QApplication(sys.argv)
app.setApplicationName("SearchKick")
app.setApplicationVersion("0.1.0")

main_window = ui.MainWindow()

main_window.show()
sys.exit(app.exec_())
