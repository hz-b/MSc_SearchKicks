#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Load/save particular files structures. This module relies on functions
    specific to the file type (Matlab, plaintext, hdf5) which are in the
    corresponding submodules.
"""

from . import matlab
from . import plaintext


def load_timeanalys(filename):
    extension = filename.split('.')[-1]
    if extension == "mat":
        return matlab.load_timeanalys(filename)
    else:
        __notImplemented(extension)


def save_timeanalys(filename, extension, BPMx, BPMy, CMx, CMy):
    if filename.split('.')[-1] in ['mat', 'hdf5']:
        filename = "".join(filename.split('.')[:-1])
    filename += '.' + extension

    if extension == "mat":
        return matlab.save_timeanalys(filename, BPMx, BPMy, CMx, CMy)
    else:
        __notImplemented(extension)


def load_orbit(filename):
    extension = filename.split('.')[-1]
    if extension == "mat":
        return matlab.load_orbit(filename)
    elif extension == "txt":
        return plaintext.load_orbit(filename)
    else:
        __notImplemented(extension)


def save_orbit(filename, extension, orbit):
    if filename.split('.')[-1] in ['mat', 'txt', 'hdf5']:
        filename = "".join(filename.split('.')[:-1])
    filename += '.' + extension

    if extension == "mat":
        return matlab.save_orbit(filename, orbit)
    elif extension == "txt":
        return plaintext.save_orbit(filename, orbit)
    elif extension == "hdf5":
        raise NotImplementedError()
    else:
        __notImplemented(extension)


def load_Smat(filename):
    extension = filename.split('.')[-1]
    if extension == "mat":
        return matlab.load_Smat(filename)
    else:
        __notImplemented(extension)


def __notImplemented(extension):
    raise Exception("Extension is '" + extension + "'. This is not implemented.");

