#!/usr/bin/env python.
# -*- coding: utf-8 -*-

from math import atan2
import numpy as np
from numpy import cos, sin
import matplotlib.pyplot as plt


def fit_sinus(signal, phase, offset_opt=True, plot=False):
    """ Find a sinus that fits with the signal.

        The funtion to fit with is
        y = a + b1*cos(d*t) + b2*sin(d*t)
          = a + b*sin(d*t + c)

        Parameters
        ----------
        signal : np.array
            Signal to be approximated.
        Phase : np.array
            Argument of the sinus. in `a + b*sin(c+d*t)` it would be `d*t`
        offset_opt : bool, optional.
            If False, the fit function is `b*sin(c + phase)`, else it is
            is `a + b*sin(c + phase)`. Default to True.
        plot : bool, optional.
            If True, plot the signal and the calculated sinus together.
            Default to False.

        Returns
        -------
        offset : float
            The `a` in `a + b*sin(c + phase)`. If offset_opt is False, it is 0.
        amplitude : float
            The `b` in `a + b*sin(c + phase)`.
        phase_shift : float
            The `c` in `a + b*sin(c + phase)`.

    """

    # In order for the function to work we should have columns (because of the
    # matrix multiplication) in the Signal and the Xarray, let's check it
    if signal.ndim == 1:
        signal = signal[np.newaxis].T
    if phase.ndim == 1:
        phase = phase[np.newaxis].T
    if signal.shape[0] == 1:
        signal = signal.T
    if phase.shape[0] == 1:
        phase = phase.T

    # check errors
    if phase.shape[0] != signal.shape[0]:
        ValueError('Arguments 1 and 2 must have the same length')
    if phase.shape[1] != 1 or signal.shape[1] != 1:
        ValueError('Arguments 1 and 2 must be (n,1)-arrays')
    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        TypeError('Arguments 3 and 4 must be booleans')

    if offset_opt:
        # set constant term
        constant = np.ones(phase.shape)
    else:
        constant = np.zeros(phase.shape)

    # Solve the system equation
    eq_matrix = np.concatenate(
        (constant, sin(phase), cos(phase)),
        1
        )
    abc, residual, _, _ = np.linalg.lstsq(eq_matrix, signal)
    offset = abc[0, 0]
    amplitude = np.linalg.norm(abc[1:3, 0])
    # atan2 keeps the information of the sign of the b1 and b2
    phase_shift = atan2(abc[2, 0], abc[1, 0])

    if plot:
        plt.figure()
        y = offset + amplitude*sin(phase + phase_shift)
        plt.plot(phase, signal, '-r')
        plt.plot(phase, y, '-b')

        plt.grid(True)

    return offset, amplitude, phase_shift
