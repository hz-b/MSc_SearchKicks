#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")

import numpy as np
import scipy
import matplotlib.pyplot as plt
import PyML
import search_kicks.core as skcore
import search_kicks.tools as sktools

import time


DEFAULT_DATA = '../search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'

SOURCE_DISTURB = 10
T_MAX = 100
PHASE = np.pi/3
FS = 150.
F = 10
NB_SP = T_MAX*FS
tuneX = 17.8509864542659


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

def toc(t1, title):
    t_old = t1
    t1 = time.time()
    dt =  t1 - t_old
    print("{}: {} s".format(title, dt))
    return t1

if __name__=='__main__':
    t0 = time.time()
##### INIT #######
    plt.close('all')
    mml = PyML.PyML()
    mml.setao(mml.loadFromExtern('../external/bessyIIinit.py', 'ao'))

    active_bpms = mml.getActiveIdx('BPMx')

    sx = mml.getfamilydata('BPMx', 'Pos')[active_bpms]
    sy = mml.getfamilydata('BPMy', 'Pos')[active_bpms]

    namesCMx = mml.getfamilydata('HCM', 'CommonNames')
    ids = []
    for i in range(namesCMx.size):
        if namesCMx[i][0:2] == 'HS':
            ids.append(i)

    cx = mml.getfamilydata('HCM', 'Pos')[ids]
    cy = mml.getfamilydata('VCM', 'Pos')

    namesX = mml.getfamilydata('BPMx', 'CommonNames')
    namesY = mml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.IO.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpms, :]
    Smat_yy = Smat_yy[active_bpms, :]

    nb_CMx = Smat_xx.shape[1]
    nb_CMy = Smat_yy.shape[1]

    CMx = np.zeros(nb_CMx)
    CMx[SOURCE_DISTURB] = 1

    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    t1 = toc(t0, "Init")

##### CONSTANT DISTURB #######
    BPMx = np.dot(Smat_xx, CMx)

    kick, coeff = skcore.get_kick(BPMx, phaseX, tuneX, False)
    idkick = np.argmin(abs(phaseX-kick))

    print(sx[idkick], cx[SOURCE_DISTURB])

    t1 = toc(t1, "Cst disturb")
##### HARMONIC DISTURB #######
    BPMx_t = np.zeros((BPMx.size, NB_SP))
    t = np.arange(NB_SP)/FS

    for i in range(BPMx.size):
        BPMx_t[i,:] = BPMx[i]*np.sin(F*2*np.pi*t+PHASE)
    t2 = toc(t1, "Harmonic disturb init")

    A, B = sktools.maths.extract_sin_cos(BPMx_t, FS, F, 'sum')
    t2 = toc(t2, "Harmonic disturb, sum")

    b1, b2 = sktools.maths.extract_sin_cos(BPMx_t, FS, F, 'fft')
    t2 = toc(t2, "Harmonic disturb, fft")

    plt.figure("sin/cos")
    plt.subplot(2,1,1)
    plt.plot(sx, A)
    plt.plot(sx, B)
    plt.legend(['sin','cos'])
    plt.title('With sums of cos/sin')

    plt.subplot(2,1,2)
    plt.plot(sx, b1)
    plt.plot(sx, b2)
    plt.legend(['sin','cos'])
    plt.title('With fft')

    phase = phases_mat['PhaseX'][:, 0]

    kick1a, kick2a = do_get_kick(b1, b2, phase, tuneX, sx, 'fft')
    kick1b, kick2b = do_get_kick(A, B, phase, tuneX, sx, 'sin_cos')
    idkick = np.argmin(abs(phaseX-kick1a))

    print(sx[idkick], cx[SOURCE_DISTURB])

    t1 = toc(t1, "Harmonic disturb")
##### KLT VS ROTATION #######
    a = np.array([A, B])

    [A_klt, B_klt] = sktools.maths.klt(a)

    step_size = 0.1
    A_opt, B_opt, _ = sktools.maths.optimize_rotation(A, B, step_size)

    plt.figure("Optimization")
    plt.subplot(2,1,1)
    plt.plot(sx, A_klt)
    plt.plot(sx, B_klt)
    plt.legend(['sin','cos'])
    plt.title('KLT')

    plt.subplot(2,1,2)
    plt.plot(sx, A_opt)
    plt.plot(sx, B_opt)
    plt.legend(['sin','cos'])
    plt.title('Rotations')

    t1 = toc(t1, "KLT/Rotat")
##### CORRECTION #######
    S_inv = sktools.maths.inverse_with_svd(Smat_xx, 10)
    r1 = np.dot(S_inv, A_klt)

    plt.figure('CMs')
    plt.plot(cx, r1)
    plt.title('Correctors')

    t1 = toc(t1, "Correction")

    _ = toc(t0, "GLOBAL")
