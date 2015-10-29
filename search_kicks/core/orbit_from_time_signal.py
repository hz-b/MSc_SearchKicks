#!/usr/bin/env python.
# -*- coding: utf-8 -*-

import numpy as np
from numpy import sin, pi


def orbit_from_time_signal(family, BPM_data, freq, sample_freq, nb_points):
    """ Do this

        parameters
        ==========
         * freq is the frequency to fit
         * The BPM data should be an array of ~(108xSamples)

        return
        ======
         * new_data
         * big_orbit
         * mRMS
    """

    if freq <= 0:
        new_data = 0
        big_orbit = BPM_data[:][abs(freq)]
        mRMS = 0

        return new_data, big_orbit, mRMS

    sample_nb = BPM_data.shape[1]
    BPM_nb = BPM_data.shape[0]

    print("Number of samples: {:d}".format(sample_nb))
    print("Number of BPM: {:d}".format(BPM_nb))

    # Vector with the samples in time
    x_array = np.arange(0, sample_nb)/sample_freq
    # Vector with the points to have in the new signal
    x_fit = np.linspace(0, sample_nb/sample_freq, nb_points)

    fit_signals = np.zeros(BPM_nb, nb_points)

    for i in range(BPM_nb):
        a, b, c = fit_sinus(BPM_data[i][:], x_array, freq, True)

        # first we fit the sinus with the offset (so the signal is well
        # fitted) but later we take off the offset of each BPM
        fit_signals[i][:] = 0 + b*sin(c + freq*2*pi*x_fit)

    new_data = fit_signals

    # Look for the index of the period in the variable Xfit
    PeriodXfit = np.where(x_fit < 1/freq)[0].size

    # Let's find the RMS value in a perod and take the bigger
    # sum sums each column
    RMSperiod = sum(np.power(new_data, 2))

    # Save the RMS of the whole period
    mRMS = sum(RMSperiod[0:PeriodXfit])

    # I is the index of the biggest RMS orbit in the signal
    I = np.argmax(RMSperiod[0:PeriodXfit])

    # This will be the orbit with the biggest amplitud
    big_orbit = new_data[:][I]

    return new_data, big_orbit, mRMS
