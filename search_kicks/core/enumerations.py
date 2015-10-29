#!/usr/bin/env python.
# -*- coding: utf-8 -*-

__author__ = "Olivier CHURLAUD"
__version__ = "0.1.0"
__maintainer__ = ""
__email__ = "olivier.churlaud@helmholtz-berlin.de"
__status__ = "Development"


class OrbitSourceItems:
    current_orbit, time_signal, load_orbit = range(3)
class DataSourceItems:
    text_entry, file_entry = range(2)
class AxisItems:
    x, y = range(2)