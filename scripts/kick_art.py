#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")
sys.path.append(__my_dir+"/../../PyML")

import scipy.io
import numpy as np
import search_kicks.core as skcore
import search_kicks.tools as sktools
import PyML
import matplotlib.pyplot as plt

DEFAULT_DATA = '../search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-57-56_vert10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-39-01-ohne_10Hz.mat'
#AXIS = 'x'
AXIS = 'y'

# Hardcoded constants
tuneX = 17.8509864542659
tuneY = 6.74232980750181
# -*- coding: utf-8 -*-

import numpy as np
from numpy import sin, pi
import matplotlib.pyplot as plt

from search_kicks.tools.maths import fit_sine
from search_kicks.core import build_sine


def get_kick(orbit, phase, tune, plot=False):
    """ Find the kick in the orbit.

        Parameters
        ----------
        orbit : np.array
            Orbit.
        phase : np.array
            Phase.
        tune : float
            The orbit tune.
        plot : bool, optional.
            If True, plot the orbit with the kick position, else don't.
            Default to False.

        Returns
        -------
        kick_phase : float
            The phase where the kick was found.
        sin_coefficients : [a, b]
            a and b so that the sine is a*sin(b+phase)

    """
    bpm_nb = orbit.size
    best_rms = 0

    # duplicate the signal to find the sine between the kick and its duplicate
    signal_exp = np.concatenate((orbit, orbit))
    phase_exp = np.concatenate((phase, phase + tune*2*pi))

    idx = []
    rms = []
    cont = []

    kick_tab = []
    # shift the sine between each BPM and its duplicate and find the best
    # match
    for i in range(bpm_nb):

        signal_t = signal_exp[i:i+bpm_nb+1]
        phase_t = phase_exp[i:i+bpm_nb+1]

        _, b, c = fit_sine(signal_t, phase_t, 'inv', False)
        sin_coefficients = [b, c]

        if i == 0:
            phase_previous = phase_exp[bpm_nb-1]
            phase_next = phase_exp[bpm_nb+1]
        else:
            phase_previous = phase_exp[i-1]
            phase_next = phase_exp[i+1]
        interval = np.linspace(phase_previous, phase_next, 100000)

        # Continuity condition
        if np.min(abs(b*sin(interval+c) - b*sin(interval+c+2*pi*tune))) > 1e-4:
            continue
        idx_min = np.argmin(
            abs(b*sin(interval + c) - b*sin(interval+c+2*pi*tune))
            )
        kick_phase = interval[idx_min] % phase_exp[bpm_nb]
        kick_tab.append(kick_phase)
        # function
        sine_signal, phase_th = build_sine(kick_phase,
                                           tune,
                                           [b, c],
                                           phase_t
                                           )
        sine_signal2, _ = build_sine(kick_phase,
                                           tune,
                                           [b, c],
                                           )

        # calculate the RMS. the best fit means that the kick is between
        # the BPMs idx and idx+1
        rms.append(sum(pow(sine_signal-signal_t, 2)))
        #print(rms)
        print(i)
        idx.append(i)
        cont.append(np.min(abs(b*sin(interval + c) - b*sin(interval+c+2*pi*tune))))
        print(cont[-1])
        print('rms {}'.format(idx[np.argmin(rms)]))
        plt.figure()
        plt.plot(np.arange(sine_signal2.size)/float(sine_signal2.size)*107, sine_signal2)
        plt.plot(orbit)


    kick_phase = kick_tab[np.argmin(rms)]
    if plot:
        plt.figure()
        plt.plot(phase/(2*pi), orbit, '+')
        plt.xlabel(r'phase / $2 \pi$')
        plt.axvline(kick_phase/(2*pi), -2, 2)

        sine_signal, phase_th = build_sine(kick_phase,
                                           tune,
                                           sin_coefficients
                                           )

        plt.plot(phase_th/(2*pi), sine_signal)



        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(np.arange(sine_signal.size)/float(sine_signal.size)*107, sine_signal)
        plt.plot(orbit)
        for idx1 in idx:
            plt.axvline(idx1, -2, 2)

        plt.subplot(3,1,2)
        plt.plot(idx,rms)
        plt.subplot(3,1,3)
        plt.plot(idx,cont)
    return kick_phase, sin_coefficients


if __name__=='__main__':
    plt.close('all')

    tune = tuneY
    kick_phase = 2*np.pi*3.18
    phase_tmp = np.linspace(0, tune*2*np.pi, 5000)
    phase_tmp = phase_tmp[:-1]
    sine_tmp = np.concatenate((np.sin(phase_tmp + kick_phase),
                               -np.sin(phase_tmp + kick_phase)))

    phase_exp = np.concatenate((phase_tmp-2*np.pi*tune,
                                phase_tmp))+kick_phase

    valid_ids = np.logical_and(phase_exp >= 0, phase_exp <= tune*2*np.pi)

    phase_th = phase_exp[valid_ids]
    sine_signal = sine_tmp[valid_ids]
    plt.figure()
    plt.plot(phase_th,sine_signal)


if __name__=='d':
    if len(sys.argv) == 1:
        cidx = 30
    else:
        cidx = int(sys.argv[1])

    plt.close('all')
    pml = PyML.PyML()
    pml.setao(pml.loadFromExtern('../../PyML/config/bessyIIinit.py', 'ao'))

    active_bpmsx = pml.getActiveIdx('BPMx')
    active_bpmsy = pml.getActiveIdx('BPMy')

    sx = pml.getfamilydata('BPMx', 'Pos')
    sy = pml.getfamilydata('BPMy', 'Pos')

    cx = pml.getfamilydata('HCM', 'Pos')[pml.getActiveIdx('HCM')]
    cy = pml.getfamilydata('VCM', 'Pos')[pml.getActiveIdx('VCM')]

    namesX = pml.getfamilydata('BPMx', 'CommonNames')
    namesY = pml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.IO.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpmsx, :]
    Smat_yy = Smat_yy[active_bpmsy, :]

    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    if AXIS == 'y':
        pos_cor = cy
        pos = sy[active_bpmsy]
        Smat = Smat_yy
        phase = phaseY
        tune = tuneY
        names = namesY[active_bpmsy]
    elif AXIS == 'x':
        pos_cor = cx
        pos = sx[active_bpmsx]
        Smat = Smat_xx
        phase = phaseX
        tune = tuneX
        names = namesX[active_bpmsx]

    corr = np.zeros(Smat.shape[1])
    corr[cidx] = 1
    values = np.dot(Smat,corr)
    S_inv = sktools.maths.inverse_with_svd(Smat, 32)

    r1 = np.dot(S_inv, values)

    plt.figure('CMs')
    plt.plot(pos_cor, r1)
    plt.title('Correctors')

    # Kick
    kicka1, coeffa1 = get_kick(np.array(values), phase, tune, True)

    kik1 = np.argmin(abs(phase-kicka1))

    plt.figure('Orbits + kick')
    plt.plot(pos, values, '-g')
    plt.axvline(pos[kik1], -2, 2)

    if pos[kik1] == pos_cor[cidx]:
        text = names[kik1] + ' Good job!'
    else:
        text = '{} found, d={}'.format(names[kik1],abs(pos_cor[cidx]-pos[kik1]))
    print(text)
    print(np.argmin(abs(pos-pos_cor[cidx])))
    plt.show()
