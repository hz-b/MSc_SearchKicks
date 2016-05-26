#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os, sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from scipy import signal, optimize

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


def ze_func(values, t, fs, ref_freq, title):
    def func(t, a, b, c, f):
        return a + b*np.cos(2*np.pi*f*t)+c*np.sin(2*np.pi*f*t)

    asin, acos = sktools.maths.extract_sin_cos(values, fs, ref_freq)
    plt.figure()
    plt.subplot(211)
    plt.title(title)
    plt.plot(pos, asin)
    plt.plot(pos, acos)
    plt.legend(['sin', 'cos'])

    N = values.shape[0]
    offs = np.zeros(N)
    ampc = np.zeros(N)
    amps = np.zeros(N)
    freq = np.zeros(N)
    for idx in range(values.shape[0]):
        y = values[idx,:]
        res, _ \
            = optimize.curve_fit(func, t, y,
                                 [np.mean(y), acos[idx], asin[idx], ref_freq])

        [offs[idx], ampc[idx], amps[idx], freq[idx]] = res

    plt.subplot(212)
    plt.plot(pos, amps)
    plt.plot(pos, ampc)
    plt.legend(['sin', 'cos'])

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



    sample_nb = values.shape[1]
    Nmax = sample_nb

    t = np.arange(sample_nb)/fs
    p0 = np.random.random() * 2*np.pi
    tenHz = np.sin(2*np.pi*10*t + p0)

    ze_func(values[:,:Nmax], t[:Nmax], fs, ref_freq, 'No filter')

    b = signal.firwin(70, [6, 14], pass_zero=False, nyq=150/2)
    w,H = signal.freqz(b)
    plt.figure()
    plt.subplot(211)
    plt.plot(w*fs/2/np.pi, 20*np.log10(abs(H)))
    plt.subplot(212)
    plt.plot(w*fs/2/np.pi, np.unwrap(np.angle(H)))
    values_f = signal.lfilter(b, 1, values, axis=1)
    ze_func(values_f[:,:Nmax], t[:Nmax], fs, ref_freq, 'with filter')

    plt.figure()
    idx = 60
    plt.plot(t[100:Nmax],values[idx,100:Nmax]-np.mean(values[idx,100:Nmax]))
    plt.plot(t[100:Nmax],values_f[idx,100:Nmax]-np.mean(values_f[idx,100:Nmax]))

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
