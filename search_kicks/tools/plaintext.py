#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functions to load/save particular files structures from/in .txt format.
"""

import numpy as np


def load_orbit(filename):
    return np.loadtxt(filename)


def save_orbit(filename, orbit):
    np.savetxt(filename, {'orbit': orbit})
    return True
