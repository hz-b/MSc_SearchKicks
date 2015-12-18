#!/usr/bin/env python.
# -*- coding: utf-8 -*-

from math import atan2
import numpy as np
from numpy import cos, sin
import matplotlib.pyplot as plt


def fit_sine(signal, phase, method, offset_opt=True, plot=False):
    """ Find a sine that fits with the signal.

        The funtion to fit with is
        y = a + b1*cos(d*t) + b2*sin(d*t)
          = a + b*sin(d*t + c)

        It internally calls fit_sin_cos(signal, phase, offset_opt, False)

        Parameters
        ----------
        signal : np.array
            Signal to be approximated.
        phase : np.array
            Argument of the sine. in `a + b*sin(c+d*t)` it would be `d*t`
        method: string
            Which method to use: 'inv' or 'sum'
        offset_opt : bool, optional.
            If False, the fit function is `b*sin(c + phase)`, else it is
            is `a + b*sin(c + phase)`. Default to True.
        plot : bool, optional.
            If True, plot the signal and the calculated sine together.
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

    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        raise TypeError('Arguments 4 and 5 must be booleans')
    if method not in ['inv', 'sum']:
        raise ValueError("Argument 3 must be 'inv' or 'sum'")

    offset, amp_sin, amp_cos = fit_sin_cos(signal, phase, method,
                                           offset_opt, False)

    amplitude = np.linalg.norm([amp_sin, amp_cos])
    # atan2 keeps the information of the sign of the b1 and b2
    phase_shift = atan2(amp_cos, amp_sin)

    if plot:
        plt.figure()
        y = offset + amplitude*sin(phase + phase_shift)
        plt.plot(phase, signal, '+r')
        plt.plot(phase, y, '-b')

        plt.grid(True)

    return offset, amplitude, phase_shift


def fit_sin_cos(signal, phase, method, offset_opt=True, plot=False):
    """ Find a sum of sine and cosine that fits with the signal.

        The funtion to fit with is
        `y = a + b1*cos(d*t) + b2*sin(d*t)`

        Parameters
        ----------
        signal : np.array
            Signal to be approximated.
        phase : np.array
            Argument of the sine. in `a + b*sin(c+d*t)` it would be `d*t`
        method: string
            Which method to use: 'inv' or 'sum'
        offset_opt : bool, optional.
            If False, the fit function is `b*sin(c + phase)`, else it is
            is `a + b*sin(c + phase)`. Default to True.
        plot : bool, optional.
            If True, plot the signal and the calculated sine together.
            Default to False.

        Returns
        -------
        offset : float
            The `a` in `a + b1*sin(phase) + b2*cos(phase)`.
            If offset_opt is False, it is 0.
        amp_sin : float
            The `b1` in `a + b1*sin(phase) + b2*cos(phase)`.
        amp_cos : float
            The `b2` in `a + b1*sin(phase) + b2*cos(phase)`.

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
        raise ValueError('Arguments 1 and 2 must have the same length')
    if phase.shape[1] != 1 or signal.shape[1] != 1:
        raise ValueError('Arguments 1 and 2 must be (n,1)-arrays')
    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        raise TypeError('Arguments 4 and 5 must be booleans')
    if method not in ['inv', 'sum']:
        raise ValueError("Argument 3 must be 'inv' or 'sum'")

    offset, amp_sin, amp_cos = 0, 0, 0
    if method == "inv":
        offset, amp_sin, amp_cos = _fit_with_inversion(signal, phase,
                                                       offset_opt)
    elif method == "sum":
        offset, amp_sin, amp_cos = _fit_with_sum(signal, phase,
                                                 offset_opt)

    if plot:
        plt.figure()
        y = offset + amp_sin*sin(phase) + amp_cos*cos(phase)
        plt.plot(phase, signal, '+r')
        plt.plot(phase, y, '-b')

        plt.grid(True)

    return offset, amp_sin, amp_cos


def _fit_with_sum(signal, phase, offset_opt):

    N = signal.size
    ssin = sin(phase)
    scos = cos(phase)

    if offset_opt:
        offset = sum(signal)[0]/N
    else:
        offset = 0.

    amp_sin = sum(ssin*signal)[0]*2/N
    amp_cos = sum(scos*signal)[0]*2/N

    return offset, amp_sin, amp_cos


def _fit_with_inversion(signal, phase, offset_opt):

    # set constant term
    if offset_opt:
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
    amp_sin = abc[1, 0]
    amp_cos = abc[2, 0]

    return offset, amp_sin, amp_cos
