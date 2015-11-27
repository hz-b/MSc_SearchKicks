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
            Phase build with a linspace

    """

    phase_tmp = np.linspace(kick_phase, kick_phase+tune*2*np.pi, 5000)
    phase_tmp = phase_tmp[:-1]  # The last point is the same as the first one

    b = sin_coefficients[0]
    c = sin_coefficients[1]

#    phase_th = np.linspace(0, 2*np.pi*tune, 1000)
#    sinus_signal = np.concatenate(
#        (
#            b*np.sin(phase_th[:kick_id] + c),
#            b*np.sin(2*phase_th[kick_id]-phase_th[kick_id:] + c)
#        ))

    sinus_tmp = np.concatenate((b*np.sin(phase_tmp + c),
                                b*np.sin(phase_tmp + c)))

    phase_exp = np.concatenate((phase_tmp-2*np.pi*tune,
                                phase_tmp))

    valid_ids = np.logical_and(phase_exp >= 0, phase_exp <= tune*2*np.pi)

    phase_th = phase_exp[valid_ids]
    sinus_signal = sinus_tmp[valid_ids]

    return sinus_signal, phase_th
