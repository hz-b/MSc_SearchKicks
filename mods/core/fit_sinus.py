#!/usr/bin/env python.
# -*- coding: utf-8 -*-

from math import atan2, pi
import numpy as np
from numpy import cos, sin
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt


def fit_sinus(signal, x_array, freq, offset_opt=True, plot=False):
    """
        The function to fit with is
        y = a + b1*cos(d*t) + b2*sin(d*t)
          = a + b*sin(c+d.*t)
    """

    # In order for the function to work we should have columns (because of the
    # matrix multiplication) in the Signal and the Xarray, let's check it
    if signal.shape[0] == 1:
        signal = signal.T
    if x_array.shape[0] == 1:
        x_array = x_array.T

    # check errors
    if x_array.shape[0] != signal.shape[0]:
        ValueError('Arguments 1 and 2 must have the same length')
    if x_array.shape[1] != 1 or signal.shape[1] != 1:
        ValueError('Arguments 1 and 2 must be (n,1)-arrays')
    if not np.isscalar(freq):
        TypeError('Argument 3 must be a scalar')
    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        TypeError('Arguments 4 and 5 must be booleans')

    if offset_opt:
        # set constant term
        constant = np.ones(x_array.shape)
    else:
        constant = np.zeros(x_array.shape)

    # Solve the system equation
    eq_matrix = np.concatenate((
                                    constant,
                                    sin(freq*x_array),
                                    cos(freq*x_array)
                                ), 1)
    abc, residual, _, _ = np.linalg.lstsq(eq_matrix, signal)
    offset = abc[0]
    strength = np.linalg.norm(abc[1:3])
    # atan2 keeps the information of the sign of the b1 and b2
    phase_shift = atan2(abc[2], abc[1])

    print(strength)
    print(phase_shift)

    print(10*2*pi*x_array)
    print(offset+strength*sin(10*2*pi*x_array + phase_shift))
    if plot:
        plt.figure()
        plt.figure(1)
        y = offset + strength*sin(10*2*pi*x_array + phase_shift)

        plt.plot(x_array, signal, '-r')
        plt.plot(x_array, y, '-b')

        plt.grid(True)
        plt.show(block=False)

    return offset, strength, phase_shift


if __name__ == "__main__":
    signal = np.random.random([20, 1])
    x_array = np.array([np.arange(1, 21)]).T/10
    freq = 5
    offset, strength, phase_shift = fit_sinus(signal, x_array, freq,
                                              True, True)
