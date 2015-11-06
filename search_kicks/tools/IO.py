#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functions to call from other moduls to load/save particular files
    structures. This modul relies on functions specific to the file type
    (Matlab, plaintext, hdf5)
"""

from . import matlab
from . import plaintext


def load_timeanalys(filename):
    extension = filename.split('.')[-1]
    if extension == "mat":
        return matlab.load_timeanalys(filename)


def save_timeanalys(filename, extension, BPMx, BPMy, CMx, CMy):
    if filename.split('.')[-1] in ['mat', 'hdf5']:
        filename = "".join(filename.split('.')[:-1])
    filename += '.' + extension

    if extension == "mat":
        return matlab.save_timeanalys(filename, BPMx, BPMy, CMx, CMy)


def load_orbit(filename):
    extension = filename.split('.')[-1]
    if extension == "mat":
        return matlab.load_orbit(filename)
    elif extension == "txt":
        return plaintext.load_orbit(filename)


def save_orbit(filename, extension, orbit):
    if filename.split('.')[-1] in ['mat', 'txt', 'hdf5']:
        filename = "".join(filename.split('.')[:-1])
    filename += '.' + extension

    if extension == "mat":
        return matlab.save_orbit(filename, orbit)
    elif extension == "txt":
        return plaintext.save_orbit(filename, orbit)
    elif extension == "hdf5":
        NotImplementedError()
