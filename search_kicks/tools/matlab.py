#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functions to load/save particular files structures from/in .mat format.
"""

import numpy as np
import scipy.io


def load_timeanalys(filename):
    data = scipy.io.loadmat(filename)

    # Check that the file is well formatted
    if ('BPMx' not in data) and ('BPMy' not in data) \
            and ('CMx' not in data) and ('CMx' not in data):
        raise Exception("File is not well formated")

    sample_nb = data['difforbitX'].shape[1]

    if data['difforbitY'].shape[1] != sample_nb \
            and data['CMx'].shape[1] != sample_nb \
            and data['CMy'].shape[1] != sample_nb:
        raise Exception("File is not well formated")

    BPMx_nb = data['difforbitX'][0, 0].shape[0]
    BPMy_nb = data['difforbitY'][0, 0].shape[0]
    CMx_nb = data['CMx'][0, 0].shape[0]
    CMy_nb = data['CMy'][0, 0].shape[0]

    BPMx = np.zeros((BPMx_nb, sample_nb))
    BPMy = np.zeros((BPMy_nb, sample_nb))
    CMx = np.zeros((CMx_nb, sample_nb))
    CMy = np.zeros((CMy_nb, sample_nb))

    for i in range(sample_nb):
        for j in range(BPMx_nb):
            BPMx[j, i] = data['difforbitX'][0, i][j, 0]
        for j in range(BPMy_nb):
            BPMy[j, i] = data['difforbitY'][0, i][j, 0]
        for j in range(CMx_nb):
            CMx[j, i] = data['CMx'][0, i][j, 0]
        for j in range(CMy_nb):
            CMy[j, i] = data['CMy'][0, i][j, 0]

    if 'Freq' in data:
        freq = float(data['Freq'][0])
    else:
        freq = None

    if 'bpms' in data:
        BPMs_names = data['bpms']
    else:
        BPMs_names = None

    return BPMx, BPMy, CMx, CMy, BPMs_names, freq


def save_timeanalys(filename, BPMx, BPMy, CMx, CMy):

    sample_nb = BPMx.shape[1]

    # Check that the data are well formatted
    if BPMy.shape[1] != sample_nb \
            and CMx.shape[1].shape[1] != sample_nb \
            and CMy.shape[1] != sample_nb:
        raise Exception("Data are not well formatted (must have the same "
                        "number of samples, ie. elements per row)")

    data = {'difforbitX': np.empty((1, sample_nb), dtype=object),
            'difforbitY': np.empty((1, sample_nb), dtype=object),
            'CMx': np.empty((1, sample_nb), dtype=object),
            'CMy': np.empty((1, sample_nb), dtype=object)
            }
    for i in range(sample_nb):
        data['difforbitX'][0, i] = BPMx[:, i, np.newaxis]
        data['difforbitY'][0, i] = BPMy[:, i, np.newaxis]
        data['CMx'][0, i] = CMx[:, i, np.newaxis]
        data['CMy'][0, i] = CMy[:, i, np.newaxis]

    scipy.io.savemat(filename, data)

    return True


def load_orbit(filename):
    data = scipy.io.loadmat(filename)

    # Check that the file is well formatted
    if ('orbit' not in data) and ('phase' not in data) \
            and ('tune' not in data):
        raise Exception("File is not well formated")

    if data['orbit'].shape != data['phase'].shape:
        raise Exception("File is not well formated")

    return data['orbit'], data['phase'], data['tune']


def save_orbit(filename, orbit, phase, tune):

    # Check that the file is well formatted
    if orbit.length != phase.length:
        raise Exception("Data are not well formatted (must have the same "
                        "length")

    scipy.io.savemat(filename, {'orbit': orbit})
    return True


def load_Smat(filename):
    smat = scipy.io.loadmat(filename)

    if 'Rmat' not in smat:
        raise Exception("Cannot find Rmat structure. Check the file you "
                        "provided.")

    Smat_xx = smat['Rmat'][0, 0]['Data']
    Smat_yy = smat['Rmat'][1, 1]['Data']

    return Smat_xx, Smat_yy
