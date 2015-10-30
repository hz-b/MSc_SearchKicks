#!/usr/bin/env python.
# -*- coding: utf-8 -*-

import numpy as np
from numpy import sin, pi
import matplotlib.pyplot as plt

from fit_sinus import fit_sinus


def get_kick(orbit, phase, tune, plot=False):
    """
        Find the kick in the orbit.

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
            kick_phase :
    """
    bpm_nb = orbit.size
    best_rms = 0

    # duplicate the signal to find the sinus between the kick and its duplicate
    signal_exp = np.concatenate((orbit, orbit))
    phase_exp = np.concatenate((phase, phase + tune*2*pi))

    # shift the sinus between each BPM and its duplicate and find the best
    # match
    for i in range(bpm_nb):
        signal_t = signal_exp[i:i+bpm_nb]
        phase_t = phase_exp[i:i+bpm_nb]

        _, b, c = fit_sinus(signal_t, phase_t, False)

        y = b*sin(c + phase_t)

        # calculate the RMS. the best fit means that the kick is between
        # the BPMs idx and idx+1
        rms = sum(pow(y-signal_t, 2))
        if rms < best_rms or i == 0:
            best_rms = rms

            sin_coefficients = [b, c]
            # find the phase between the BPM i-1 and i where
            # sin(phase) = sin(phase -2pi*tune).
            # It's easier to look in the first part of the phase_exp and then
            # add 2*pi*tune
            phase_previous = phase_exp[i]
            phase_next = phase_exp[i+1]
            interval = np.linspace(phase_previous, phase_next, 1000)
            idx_min = np.argmin(
                abs(b*sin(interval + c) - b*sin(interval+c-2*pi*tune))
                )
            kick_phase = interval[idx_min]

    if plot:
        plt.figure()
        plt.plot(phase/2/pi, orbit, '-')
        plt.xlabel(r'phase / $2 \pi$')
        plt.axvline(kick_phase/2/pi, -2, 2)

        phase_th = np.linspace(0, tune*2*pi, 1000)
        kick_id = np.argmin(abs(phase_th - kick_phase))

        b = sin_coefficients[0]
        c = sin_coefficients[1]
        sinus_signal = np.concatenate(
            (
                b*sin(phase_th[:kick_id] + c + 2*pi*tune),
                b*sin(phase_th[kick_id:] + c)
            ))
        plt.plot(phase_th/2/pi, sinus_signal)

    return kick_phase


if __name__ == "__main__":
    bpm_nb = 30
    i = 13  # BPM before kick
    away_ratio = 0.2

    tune = 6.5
    phase = np.linspace(0, 2*pi*tune, bpm_nb)

    noise = 2*np.random.random(30)-1

    kick = phase[i]+(phase[i+1]-phase[i])*away_ratio
    orbit = np.concatenate((
        np.sin(phase[:i]),
        np.sin(2*(kick)-phase[i:])
        )) + noise
    print("kick set at {}".format(kick))
    print(get_kick(orbit, phase, tune, True))
