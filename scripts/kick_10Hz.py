#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")

import scipy.io
import numpy as np
import search_kicks.core as skcore
import search_kicks.tools as sktools
import PyML
import matplotlib.pyplot as plt
import cmath

DEFAULT_DATA = '../search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'
DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-57-56_vert10Hz.mat'
#DATA_FILE = '../_data/FastBPMData_2015-10-26_06-54-42horz10Hz.mat'

# Hardcoded constants
tuneX = 17.8509864542659
tuneY = 6.74232980750181
ref_freq = 10#9.979248046875

def function_sin_cos(ref_freq, values, fs, ph):
    A = []
    B = []
    t = np.arange(values[1,:].size)/fs

    phase_sin = t*ref_freq
    for k in active_bpms:
        _, A_t, B_t = skcore.fit_sin_cos(values[k, :], phase_sin, 'sum', False)
        A.append(A_t)
        B.append(B_t)

    plt.figure("sin/cos")
    plt.plot(ph,A)
    plt.plot(ph,B)

    return A,B


def function_fft(ref_freq, values, fs, pos):
    sp_nb = values.shape[1]

    t = np.divide(np.arange(sp_nb), fs*np.ones(sp_nb))
    f = np.fft.fftfreq(t.shape[-1], 1/fs)
    freq_idx=np.argmin(np.abs(ref_freq - f))
    print('+++++++++')
    print(f[freq_idx])
    print('+++++++++')

    b1 = []
    b2 = []

    for k in active_bpms:
        fftxk = np.fft.fft(values[k, :])[freq_idx]#*rot*amp
        b1.append(fftxk.real)
        b2.append(fftxk.imag)

    plt.figure("sin/cos fft")
    plt.plot(pos,b1)
    plt.plot(pos,b2)

    return b1, b2


def do_svd(A,B,Smat,title):
    U, s, V = np.linalg.svd(Smat, full_matrices=False)
    # S_mat = U * diag(s) * V
    idmax = 20
    Sred = np.diag(np.ones(idmax)/s[:idmax])
    Ured = U[:,:idmax]
    Vred = V[:idmax,:]

    S_inv = np.dot(Vred.conj().T, np.dot(Sred, Ured.conj().T))
    r1 = np.dot(S_inv, A)
    r2 = np.dot(S_inv, B)


    plt.figure('CMs with '+title)
    plt.plot(abs(r1))
    plt.plot(abs(r2))
    plt.legend(['sin', 'cos'])


def do_get_kick(A, B, phase, tune, pos, title):

    kicka1, coeffa1 = skcore.get_kick(np.array(A), phase, tune, False)
    kicka2, coeffa2 = skcore.get_kick(np.array(B), phase, tune, False)

    kik1 = np.argmin(abs(phase-kicka1))
    kik2 = np.argmin(abs(phase-kicka2))

    plt.figure('Orbits + kick with '+title)
    plt.subplot(2, 1, 1)
    plt.plot(pos, A, '-g')
    plt.axvline(pos[kik1], -2, 2)
    plt.title('sine')

    plt.subplot(2, 1, 2)
    plt.plot(pos, B, '-g')
    plt.axvline(pos[kik2], -2, 2)
    plt.title('cosine')

    return kik1, kik2


if __name__=='__main__':
    plt.close('all')
    mml = PyML.PyML()
    mml.setao(mml.loadFromExtern('../external/bessyIIinit.py', 'ao'))

    active_bpms = mml.getActiveIdx('BPMx')

    sx = mml.getfamilydata('BPMx', 'Pos')
    sy = mml.getfamilydata('BPMy', 'Pos')

    namesX = mml.getfamilydata('BPMx', 'CommonNames')
    namesY = mml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.IO.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpms, :]
    Smat_yy = Smat_yy[active_bpms, :]

    valuesX, valuesY, _, _, _, fs = sktools.IO.load_timeanalys(DATA_FILE)

    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    pos = sy[active_bpms]
    Smat = Smat_yy
    phase = phaseY
    tune = tuneY
    values = valuesY
    names = namesY

    sp_nb = values.shape[1]

    A, B = function_sin_cos(ref_freq, values, fs, pos)
    b1, b2 = skcore.extract_cos_sin_withfft(values[active_bpms], fs, ref_freq)
    plt.figure("sin/cos fft")
    plt.plot(pos, b1)
    plt.plot(pos, b2)

    do_svd(A,B, Smat, 'sin_cos')
    do_svd(b1,b2, Smat, 'fft')

    kik1, kik2 = do_get_kick(b1, b2, phase, tune, pos, 'fft')
    kik1b, kik2b =do_get_kick(A, B, phase, tune, pos, 'sin_cos')

    print(names[active_bpms][kik1], names[active_bpms][kik2])
    print(names[active_bpms][kik1b], names[active_bpms][kik2b])