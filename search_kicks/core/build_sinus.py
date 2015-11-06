# -*- coding: utf-8 -*-

import numpy as np


def build_sinus(kick_phase, tune, sin_coefficients):
    """ Build a sinus with a kich at kick_phase

        Parameters
        ----------
        kick_phase : np.array
            Phase position where the kick happens
        tune : float
            Tune of the signal
        sin_coefficients : np.array or list
            First element is the amplitude, second the phase_shift

        Returns
        -------
        sinus_signal : np.array
            Signal build
        phase_th : np.array
            Phase build ( = linspace(0, tune*2*np.pi, 1000) )

    """
    phase_th = np.linspace(0, tune*2*np.pi, 1000)
    kick_id = np.argmin(abs(phase_th - kick_phase))
    b = sin_coefficients[0]
    c = sin_coefficients[1]
    sinus_signal = np.concatenate(
        (
            b*np.sin(phase_th[:kick_id] + c + 2*np.pi*tune),
            b*np.sin(phase_th[kick_id:] + c)
        ))

    return sinus_signal, phase_th
