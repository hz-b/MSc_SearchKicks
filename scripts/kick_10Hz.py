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


DEFAULT_DATA = '../search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'
DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-57-56_vert10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-39-01-ohne_10Hz.mat'
#AXIS = 'x'
AXIS = 'y'

# Hardcoded constants
tuneX = 17.8509864542659
tuneY = 6.74232980750181
ref_freq = 10#9.979248046875


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

    if AXIS == 'y':
        pos = sy[active_bpms]
        Smat = Smat_yy
        phase = phaseY
        tune = tuneY
        values = valuesY[active_bpms, :]
        names = namesY[active_bpms]
    elif AXIS == 'x':
        pos = sx[active_bpms]
        Smat = Smat_xx
        phase = phaseX
        tune = tuneX
        values = valuesX[active_bpms, :]
        names = namesX[active_bpms]

    sp_nb = values.shape[1]

    # Extract sin cos
    A, B = sktools.maths.extract_sin_cos(values, fs, ref_freq, 'sum')
    b1, b2 = sktools.maths.extract_sin_cos(values, fs, ref_freq, 'fft')

    plt.figure("sin/cos")
    plt.subplot(2,1,1)
    plt.plot(pos, A)
    plt.plot(pos, B)
    plt.legend(['sin','cos'])
    plt.title('With sums of cos/sin')

    plt.subplot(2,1,2)
    plt.plot(pos, b1)
    plt.plot(pos, b2)
    plt.legend(['sin','cos'])
    plt.title('With fft')

    # Optimize
    step_size = 0.1
    b1_opt, b2_opt, _ = sktools.maths.optimize_rotation(b1, b2, step_size)
    a = [b1,b2]
    klt = sktools.maths.klt(a)

    plt.figure("optimisaton")
    plt.subplot(2,1,1)
    plt.title("Rotation")
    plt.plot(pos, b1_opt)
    plt.plot(pos, b2_opt)
    plt.subplot(2,1,2)
    plt.title("KLT")
    plt.plot(pos, klt[0])
    plt.plot(pos, klt[1])

    # Correction fft
    S_inv = sktools.maths.inverse_with_svd(Smat_xx, 10)

    r1 = np.dot(S_inv, b1_opt)
    r2 = np.dot(S_inv, b2_opt)

    plt.figure('CMs, fft')
    plt.plot(r1)
    plt.plot(r2)
    plt.title('Correctors, fft')

    # Kick fft
    kicka1, coeffa1 = skcore.get_kick(np.array(b1_opt), phase, tune, False)
    kicka2, coeffa2 = skcore.get_kick(np.array(b2_opt), phase, tune, False)

    kik1 = np.argmin(abs(phase-kicka1))
    kik2 = np.argmin(abs(phase-kicka2))

    plt.figure('Orbits + kick, fft')
    plt.subplot(2, 1, 1)
    plt.plot(pos, b1_opt, '-g')
    plt.axvline(pos[kik1], -2, 2)
    plt.title('sine')

    plt.subplot(2, 1, 2)
    plt.plot(pos, b2_opt, '-g')
    plt.axvline(pos[kik2], -2, 2)
    plt.title('cosine')

    # Correction sum
    a = [A,B]
    [A_opt, B_opt] = sktools.maths.klt(a)
    S_inv = sktools.maths.inverse_with_svd(Smat_xx, 10)

    cor1 = np.dot(S_inv, A_opt)
    cor2 = np.dot(S_inv, B_opt)

    plt.figure('CMs, sum')
    plt.plot(cor1)
    plt.plot(cor2)
    plt.title('Correctors, sum')

    # Kick sum
    kickA, coeffa1 = skcore.get_kick(np.array(A_opt), phase, tune, False)
    kickB, coeffa2 = skcore.get_kick(np.array(B_opt), phase, tune, False)

    kik1 = np.argmin(abs(phase-kickA))
    kik2 = np.argmin(abs(phase-kickB))

    plt.figure('Orbits + kick, sum')
    plt.subplot(2, 1, 1)
    plt.plot(pos, A_opt, '-g')
    plt.axvline(pos[kik1], -2, 2)
    plt.title('sine')

    plt.subplot(2, 1, 2)
    plt.plot(pos, B_opt, '-g')
    plt.axvline(pos[kik2], -2, 2)
    plt.title('cosine')
    print(names[kik1], names[kik2])
