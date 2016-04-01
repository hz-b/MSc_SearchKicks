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
            sin_coefficients = [b, c]
            if i == 0:
                i_best = bpm_nb
            else:
                i_best = i

    # Search in the next 1/4 period and in the previous one
    phase_previous = phase_exp[i_best]-pi/2.0
    phase_next = phase_exp[i_best]+pi/2.0

    n_lspace = 10000


    interval1 = np.linspace(phase_exp[i_best], phase_next, n_lspace)
    interval2 = np.linspace(phase_previous, phase_exp[i_best], n_lspace)
    b, c = sin_coefficients
    idx_min1 = np.argmin(
        abs(b*sin(interval1 + c) - b*sin(interval1+c+2*pi*tune))
        )
    idx_min2 = np.argmin(
        abs(b*sin(interval2 + c) - b*sin(interval2+c+2*pi*tune))
        )

    # Take the nearest, as the kick should be around the bpm found before
    if n_lspace - idx_min1 > idx_min2:
        idx_min = idx_min2
        interval = interval2
    else:
        idx_min = idx_min1
        interval = interval1

    # Here is the kick
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
