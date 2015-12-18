# -*- coding: utf-8 -*-

import numpy as np

def extract_cos_sin_withfft(values, fs, f):
    """
        Approximate the time signals by a funtion of type:
        `f(t) = a*sin(f*t) + b*cos(f*t)`.

        Parameters
        ----------
        values : np.array (nb_bpm x nb_time_samples)
            Each line is the signal of a given BPM.
        fs : float
            Sampling frequency.
        f: float
            Frequency to extract.

        Return
        ------
        amp_sin: list
            Sinus amplitude for each BPM (list of all `a`, nb_bpm elements).
        am_cos: list
            Sinus amplitude for each BPM (list of all `b`, nb_bpm elements).

    """

    sample_nb = values.shape[1]
    bpm_nb = values.shape[0]
    t = np.divide(np.arange(sample_nb), fs*np.ones(sample_nb))
    frequencies = np.fft.fftfreq(t.shape[-1], 1/fs)

    freq_idx = np.argmin(np.abs(frequencies - f))

    amp_sin = []
    amp_cos = []

    for k in range(bpm_nb):
        fftxk = np.fft.fft(values[k, :])[freq_idx]
        amp_cos.append(fftxk.real)
        amp_sin.append(fftxk.imag)

    return np.array(amp_sin), np.array(amp_cos)