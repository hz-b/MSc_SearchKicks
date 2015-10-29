#!/usr/bin/env python.
# -*- coding: utf-8 -*-

from math import atan2
import numpy as np
from numpy import cos, sin
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt


def fit_sinus(signal, x_array, offset_opt=True, plot=False):
    """
        The function to fit with is
        y = a + b1*cos(d*t) + b2*sin(d*t)
          = a + b*sin(c+d*t)
    """

    # In order for the function to work we should have columns (because of the
    # matrix multiplication) in the Signal and the Xarray, let's check it
    if signal.ndim == 1:
        signal = signal[np.newaxis].T
    if x_array.ndim == 1:
        x_array = x_array[np.newaxis].T
    if signal.shape[0] == 1:
        signal = signal.T
    if x_array.shape[0] == 1:
        x_array = x_array.T

    # check errors
    if x_array.shape[0] != signal.shape[0]:
        ValueError('Arguments 1 and 2 must have the same length')
    if x_array.shape[1] != 1 or signal.shape[1] != 1:
        ValueError('Arguments 1 and 2 must be (n,1)-arrays')
    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        TypeError('Arguments 3 and 4 must be booleans')

    if offset_opt:
        # set constant term
        constant = np.ones(x_array.shape)
    else:
        constant = np.zeros(x_array.shape)

    # Solve the system equation
    eq_matrix = np.concatenate(
        (constant, sin(x_array), cos(x_array)),
        1
        )
    abc, residual, _, _ = np.linalg.lstsq(eq_matrix, signal)
    offset = abc[0, 0]
    amplitude = np.linalg.norm(abc[1:3, 0])
    # atan2 keeps the information of the sign of the b1 and b2
    phase_shift = atan2(abc[2, 0], abc[1, 0])

    if plot:
        plt.figure()
        y = offset + amplitude*sin(x_array + phase_shift)
        plt.plot(x_array, signal, '-r')
        plt.plot(x_array, y, '-b')

        plt.grid(True)

    return offset, amplitude, phase_shift


if __name__ == "__main__":
    x_array = 2*np.pi*np.arange(1, 21).T/10
    signal = sin(x_array)+np.random.random(x_array.size)
    freq = 5
    offset, strength, phase_shift = fit_sinus(signal, x_array, True, True)
