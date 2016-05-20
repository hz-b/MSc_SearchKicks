#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os, sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

import PyML
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")
import search_kicks.core as skcore
import search_kicks.tools as sktools

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
fs = 150 #Hz


def ze_func(values, fs, f):
    M, N = values.shape
    t = np.arange(N) / fs
    e = np.exp(1j*2*np.pi*f*t).reshape((1, N)).repeat(M, axis=0)
#    plt.plot(np.fft.fftfreq(N,t[1]), np.abs(np.fft.fft(np.real(e[0,:])))*2/N)
    a = np.sum(e*values, axis=1) * 2/N

    return (a)


def goertzel(x, fs, ref_freq):
    w0 = 2*np.pi*ref_freq
    M, N = x.shape
    t = np.arange(N).reshape((1, N)).repeat(M, axis=0) /fs
    y = np.sum(x*np.exp(1j*w0*t), axis=1)
    return np.imag(y), np.real(y)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        ref_freq = float(sys.argv[1])

    plt.close('all')
    plt.ion()
    pml = PyML.PyML()
    pml.setao(pml.loadFromExtern('../external/bessyIIinit.py', 'ao'))
    pml.loadBPMOffsets('/opt/OPI/MapperApplications/conf/Orbit/SR/RefOrbit.Dat')

    active_bpmsx = pml.getActiveIdx('BPMx')
    active_bpmsy = pml.getActiveIdx('BPMy')

    sx = pml.getfamilydata('BPMx', 'Pos')
    sy = pml.getfamilydata('BPMy', 'Pos')

    namesX = pml.getfamilydata('BPMx', 'CommonNames')
    namesY = pml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.IO.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpmsx, :]
    Smat_yy = Smat_yy[active_bpmsy, :]

    #idx = pml.family2idx('BPMx')
    #idy = pml.family2idx('BPMy')

    #offsetx = pml.getfamilydata('BPMx','Offset',None,idx)
    #offsety = pml.getfamilydata('BPMy','Offset',None,idy)

    valuesX, valuesY, _,_, names, fs = sktools.IO.load_timeanalys(DATA_FILE)
    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    if AXIS == 'y':
        pos = sy[active_bpmsy]
        Smat = Smat_yy
        phase = phaseY
        tune = tuneY
        values = valuesY[active_bpmsy, :]
        names = namesY
    elif AXIS == 'x':
        pos = sx[active_bpmsx]
        Smat = Smat_xx
        phase = phaseX
        tune = tuneX
        values = valuesX[active_bpmsx, :]
        names = namesX

    phase = pos / 250 * 2*np.pi * tune
    sample_nb = values.shape[1]

    t = np.arange(sample_nb)/fs

    l = []
    lf = []

    for i in range(75):
        tph = 2*np.pi*i*t
        test = np.sin(tph).reshape((1, sample_nb))
        a, b = sktools.maths.extract_sin_cos(test, fs, i)
        l.append((b[0], a[0]))
    plt.title('With approx freq (top: sum, bottom: fft)')
    plt.plot(l)
    plt.xlabel('f')
    plt.ylim([-0.2, 1.2])

    tph = 2*np.pi*ref_freq*t
    test = 1*np.sin(tph)
    test = test.reshape((1, sample_nb)).repeat(phase.size, axis=0)
    test = test
    asin, acos = sktools.maths.extract_sin_cos(values, fs, ref_freq)

    plt.figure()

    plt.plot(pos, asin, 'p')
    plt.plot(pos, acos, 'p')
    plt.title('Extracted test signal (should be 1)')

    p = 2*np.pi*ref_freq*t[:2000]

    for k in range(values.shape[0]):
        _, a, b = sktools.maths.fit_sin_cos(values[k,:2000], p, False)
        asin[k] = a
        acos[k] = b

    plt.figure()
    plt.plot(pos, acos)
    plt.plot(pos, asin)
    plt.legend(['sin', 'cos'])
    plt.title('INV')


    asin, acos = sktools.maths.extract_sin_cos(values[:,:2000], fs, ref_freq)

    plt.figure()
    plt.plot(pos, acos)
    plt.plot(pos, asin)
    plt.legend(['sin', 'cos'])
    plt.title('sincos')

#    # Optimize
#    step_size = 0.1
#    asin_opt, acos_opt, _ = sktools.maths.optimize_rotation(asin,
#                                                            acos,
#                                                            step_size)
#    A = [asin, acos]
#    klt = sktools.maths.klt(A)
#
#    plt.figure("optimisaton")
#    plt.subplot(211)
#    plt.title("Rotation")
#    plt.plot(pos, asin_opt)
#    plt.plot(pos, acos_opt)
#    plt.legend(['sin', 'cos'])
#    plt.subplot(212)
#    plt.title("KLT")
#    plt.plot(pos, klt[0])
#    plt.plot(pos, klt[1])
#
#    # Correction fft
#    S_inv = sktools.maths.inverse_with_svd(Smat, 32)
#
#    # Kick fft
#    phase_kick, coeff = skcore.get_kick(np.array(asin_opt), phase, tune,
#                                        True, True)
#    kick_idx = np.argmin(abs(phase-phase_kick))
#    corr = np.dot(S_inv, asin_opt)
#
#    # Kick fft
#    phase_kick_cos, coeff = skcore.get_kick(np.array(acos_opt), phase, tune,
#                                            True, True)
#    kick_idx_cos = np.argmin(abs(phase-phase_kick_cos))
#
#    plt.figure('CMs, kick')
#    plt.subplot(211)
#    plt.plot(corr)
#    plt.title('Correctors for f = {} Hz [sin]'.format(ref_freq))
#
#    plt.subplot(212)
#    plt.plot(pos, asin_opt, '-g')
#    plt.axvline(pos[kick_idx], -2, 2)
#    plt.title('kick in sine component for f = {} Hz'.format(ref_freq))
#
#    print("sin = " + names[kick_idx])
#    corr_cos = np.dot(S_inv, acos_opt)
#
#    plt.figure('CMs, kick cos')
#    plt.subplot(211)
#    plt.plot(corr_cos)
#    plt.title('Correctors for f = {} Hz [cos]'.format(ref_freq))
#
#    plt.subplot(212)
#    plt.plot(pos, acos_opt, '-g')
#    plt.axvline(pos[kick_idx_cos], -2, 2)
#    plt.title('kick in cosine component for f = {} Hz'.format(ref_freq))
#
#    print("cos = " + names[kick_idx_cos])
    plt.show()
