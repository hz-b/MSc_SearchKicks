# -*- coding: utf-8 -*-


""" Maths-related helpers needed in the project.
"""

from __future__ import division, print_function

from math import atan2
import numpy as np
from numpy import cos, sin, exp
import matplotlib.pyplot as plt


def rotate(sin_amp, cos_amp, phi, deg_rad='rad'):
    if deg_rad == 'deg':
        phi = phi*np.pi/180.
    elif deg_rad == 'rad':
        pass
    else:
        raise ValueError("2nd argument must be 'deg' or 'rad'")

    z = cos_amp + 1j*sin_amp
    z = z * np.exp(1j*phi)

    return z.imag, z.real


def optimize_rotation(sin_amp, cos_amp, step_size):
    maxval = 1e10
    angle_opt = 0
    for angle in np.arange(-180, 180, step_size):
        sin_opt, cos_opt = rotate(sin_amp, cos_amp, angle, 'deg')
        if max(abs(cos_opt)) < maxval:
            maxval = max(abs(cos_opt))
            angle_opt = angle

    sin_opt, cos_opt = rotate(sin_amp, cos_amp, angle_opt, 'deg')

    return sin_opt, cos_opt, angle_opt


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
        method : string
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
        raise ValueError('Arguments 1 and 2 must have the same length, not {} and {}'.format(phase.shape[0],signal.shape[0]))
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


def extract_sin_cos(values, fs, f, method):
    """ Approximate the time signals by a funtion of type:
        `f(t) = a*sin(f*t) + b*cos(f*t)`.

        Parameters
        ----------
        values : np.array (nb_bpm x nb_time_samples)
            Each line is the signal of a given BPM.
        fs : float
            Sampling frequency.
        f : float
            Frequency to extract.
        method : string
            Which method to use: 'sum' or 'fft'

        Returns
        -------
        amp_sin : list
            Sinus amplitude for each BPM (list of all `a`, nb_bpm elements).
        am_cos : list
            Sinus amplitude for each BPM (list of all `b`, nb_bpm elements).

    """

    if method == "fft":
        return _extract_cos_sin_withfft(values, fs, f)
    elif method == "sum":
        return _extract_cos_sin_withsum(values, fs, f)
    else:
        raise ValueError("Argument 4 must be 'fft' or 'sum'")


def _fit_with_sum(signal, phase, offset_opt):

    N = signal.size
    e = exp(1j*phase)

    if offset_opt:
        offset = sum(signal)[0]/N
    else:
        offset = 0.

    c = sum(e*signal)[0]*2/N

    return offset, np.imag(c), np.real(c)


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


def _extract_cos_sin_withsum(values, fs, f):
    amp_sin = []
    amp_cos = []

    sample_nb = values.shape[1]
    t = np.arange(sample_nb)/fs
    all_freq = fs * 1/sample_nb * np.arange(sample_nb)
    f_approx = all_freq[np.argmin(abs(all_freq-f))]

    phase_sin = 2*np.pi*t*f_approx
    for row in values:
        _, A_t, B_t = fit_sin_cos(row,
                                  phase_sin,
                                  'sum',
                                  False)
        amp_sin.append(A_t)
        amp_cos.append(B_t)

    return np.array(amp_sin), np.array(amp_cos)


def _extract_cos_sin_withfft(values, fs, f):
    sample_nb = values.shape[1]
    t = np.arange(sample_nb)/fs
    all_freq = fs * 1/sample_nb * np.arange(sample_nb)
    f_approx = all_freq[np.argmin(abs(all_freq-f))]

    frequencies = np.fft.fftfreq(t.shape[-1], t[1])
    freq_idx = np.argmin(np.abs(frequencies - f_approx))

    fftx = np.fft.fft(values, axis=1)*2/sample_nb
    amp_cos = np.real(fftx[:, freq_idx])
    amp_sin = -np.imag(fftx[:, freq_idx])

    return np.array(amp_sin), np.array(amp_cos)


def klt(inputs):
    """ Apply the KLT to the input

        Parameters
        ----------
        input : np.array (signal_length x nb of dimensions)
            Each column represents a dimension of the signal.

        Returns
        -------
        output : np.array (signal_length x nb of dimensions)
            Each column represents a dimension of the signal.

    """

    covar = np.cov(inputs)
    val,vec = np.linalg.eig(covar)

    # Sort the eigenvectors with decreasing eigenvalues
    idx = val.argsort()[::-1]
    val = val[idx]
    vec = vec[:, idx]
    output = np.dot(vec.T, inputs)

    return output

def inverse_with_svd(M, nb_values):
    """ Compute the SVD and return the pseudo inverse of M with `nb_values`
        eigenvalues.

        Parameters
        ----------
        M : np.array (m x n)
            Matrix to compute
        nb_values : integer
            Number of eigenvalue to keep in the computation

        Returns
        -------
        M_inv : np.array (n x m)
            Pseudo inverse of M

    """

    U, s, V = np.linalg.svd(M.newbyteorder('='), full_matrices=False)
    #U, s, V = np.linalg.svd(M, full_matrices=False)
    # S_mat = U * diag(s) * V
    idmax = nb_values
    Sred = np.diag(np.ones(idmax)/s[:idmax])
    Ured = U[:,:idmax]
    Vred = V[:idmax,:]

    M_inv = np.dot(Vred.conj().T, np.dot(Sred, Ured.conj().T))

    return M_inv
