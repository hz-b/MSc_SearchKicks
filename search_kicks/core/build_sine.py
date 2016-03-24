# -*- coding: utf-8 -*-

import numpy as np


def build_sine(kick_phase, tune, sin_coefficients, phase=None):
    """ Build a sine with a kich at kick_phase

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
        sine_signal : np.array
            Signal build
        phase_th : np.array
            Phase build with a linspace

    """
    if phase is None:
        phase_tmp = np.linspace(0, tune*2*np.pi, 5000)
        phase_tmp = phase_tmp[:-1]  # The last point is the same as the first one
    else:
        phase_tmp = phase % tune*2*np.pi
#        kick_id = np.where((phase-kick_phase) >= 0)[0][0]
#        phase_tmp = np.concatenate((phase[kick_id:], phase[:kick_id]+tune*2*np.pi))
       # print(phase_tmp)

    b = sin_coefficients[0]
    c = sin_coefficients[1]

    sine_tmp = np.concatenate((b*np.sin(phase_tmp + kick_phase + c),
                               b*np.sin(phase_tmp + kick_phase + c)))

    phase_exp = np.concatenate((phase_tmp-2*np.pi*tune,
                                phase_tmp))+kick_phase

    valid_ids = np.logical_and(phase_exp >= 0, phase_exp <= tune*2*np.pi)

    phase_th = phase_exp[valid_ids]
    sine_signal = sine_tmp[valid_ids]

    return sine_signal, phase_th
