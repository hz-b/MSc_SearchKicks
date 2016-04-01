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

    ttt = []
    aaa = []
    # shift the sine between each BPM and its duplicate and find the best
    # match
    for i in range(bpm_nb):
        signal_t = signal_exp[i:i+bpm_nb]
        phase_t = phase_exp[i:i+bpm_nb]

        _, b, c = fit_sine(signal_t, phase_t, 'inv', False)

        y = b*sin(c + phase_t)

        # calculate the RMS. the best fit means that the kick is between
        # the BPMs idx and idx+1
        rms = sum(pow(y-signal_t, 2))
        if rms < best_rms or i == 0:
            best_rms = rms
            i_best = i
            sin_coefficients = [b, c]

    # we want to find the phase between the BPM i and i+1 where
    # sin(phase) = sin(phase - 2pi*tune).
    # It's easier to look in the first part of the phase_exp and then
    # add 2*pi*tune
    if i_best == 0:
        phase_previous = phase_exp[bpm_nb]-pi/2.0
        phase_next = phase_exp[bpm_nb]+pi/2.0
    else:
        phase_previous = phase_exp[i_best]-pi/2.0
        phase_next = phase_exp[i_best]+pi/2.0

#        interval = np.linspace(phase_previous, phase_next, 1000)
    interval = np.linspace(phase_previous, phase_next, 100000)
    b, c = sin_coefficients
    idx_min = np.argmin(
        abs(b*sin(interval + c) - b*sin(interval+c+2*pi*tune))
        )
    kick_phase = interval[idx_min] % phase_exp[bpm_nb]

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

    return kick_phase, sin_coefficients
