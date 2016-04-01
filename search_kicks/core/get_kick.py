# -*- coding: utf-8 -*-

import numpy as np
from numpy import sin, pi
import matplotlib.pyplot as plt

from search_kicks.tools.maths import fit_sine
from search_kicks.core import build_sine


def get_kick(orbit, phase, tune, plot=False, error_curves=False):
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
    rms_tab = []
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
        rms_tab.append(rms)
        if rms < best_rms or i == 0:
            best_rms = rms
            sin_coefficients = [b, c]
            if i == 0:
                i_best = bpm_nb
            else:
                i_best = i

    # Search between the previous and the next 1/4 period
    phase_previous = phase_exp[i_best]-pi/2.0
    phase_next = phase_exp[i_best]+pi/2.0

    n_lspace = 10000

    interval = np.linspace(phase_previous, phase_next, n_lspace)
    b, c = sin_coefficients
    idx_min = np.argmin(
        abs(b*sin(interval + c) - b*sin(interval + c+2*pi*tune))
        )

    # Here is the kick
    kick_phase = interval[idx_min] % phase_exp[bpm_nb]

    if error_curves:
        transl = bpm_nb//2 - i_best
        rms_tab = np.roll(rms_tab,transl)
        offset = 2*pi
        interval_rel = np.linspace(-offset, +offset, n_lspace)
        interval = interval_rel+phase_exp[i_best]
        b, c = sin_coefficients

        plt.figure('skcore::get_kick -- Error curves [{}]'.format(len(plt.get_fignums())) )
        plt.subplot(2,1,1)
        plt.title('1- Sine Fit')
        plt.plot(range(-len(rms_tab)//2, len(rms_tab)//2),rms_tab)
        plt.ylabel('RMS')
        plt.xlabel('Distance from chosen one (in indexes)')
        plt.grid()

        plt.subplot(2,1,2)
        plt.title('2- Find kick')
        plt.plot(
            interval_rel, abs(b*sin(interval + c) - b*sin(interval+c+2*pi*tune))
            )
        tick_vals = []
        tick_labels = []
        amp_max = int(offset // pi)
        for x in range(-amp_max, amp_max+1):
            if x == 0:
                tick_labels.append('0')
                tick_vals.append(0)
            elif x == 1:
                tick_labels.append(r'$\pi$')
                tick_vals.append(pi)
            elif x == -1:
                tick_labels.append(r'$-\pi$')
                tick_vals.append(-pi)
            else:
                tick_labels.append(r'$'+str(x)+'\pi$')
                tick_vals.append(x*pi)

        plt.xticks(tick_vals, tick_labels)
        plt.ylabel('Size of curve jump')
        plt.xlabel('Position of kick (relative to initial one) ')
        plt.tight_layout()



    if plot:
        plt.figure('skcore::get_kick -- Orbit plot [{}]'.format(len(plt.get_fignums())) )
        plt.plot(phase/(2*pi), orbit, '+')
        sine_signal, phase_th = build_sine(kick_phase,
                                           tune,
                                           sin_coefficients
                                           )
        plt.plot(phase_th/(2*pi), sine_signal)
        plt.axvline(kick_phase/(2*pi), -2, 2)
        plt.xlabel(r'phase / $2 \pi$')
        plt.legend(['Real orbit', 'Reconstructed sine'])
    return kick_phase, sin_coefficients
