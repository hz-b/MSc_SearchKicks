# -*- coding: utf-8 -*-


""" Maths-related helpers needed in the project.
"""

from __future__ import division, print_function

from math import atan2
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize


def rotate(cos_amp, sin_amp, phi, deg_rad='rad'):
    if deg_rad == 'deg':
        phi = phi*np.pi/180.
    elif deg_rad == 'rad':
        pass
    else:
        raise ValueError("4th argument must be 'deg' or 'rad'")

    z = cos_amp + 1j*sin_amp
    z = z * np.exp(1j*phi)

    return z.real, z.imag


def optimize_rotation(cos_amp, sin_amp, step_size):
    maxval = 1e10
    angle_opt = 0
    for angle in np.arange(-180, 180, step_size):
        sin_opt, cos_opt = rotate(cos_amp, sin_amp, angle, 'deg')
        if max(abs(cos_opt)) < maxval:
            maxval = max(abs(cos_opt))
            angle_opt = angle

    cos_opt, sin_opt = rotate(cos_amp, sin_amp, angle_opt, 'deg')

    return cos_opt, sin_opt, angle_opt


def fit_sine(signal, phase, offset_opt=True, plot=False):
    """ Find a sine that fits with the signal.

        The funtion to fit with is
        y = a + b1*cos(d*t) + b2*sin(d*t)
          = a + b*cos(d*t + c)

        It internally calls fit_sin_cos(signal, phase, offset_opt, False)

        Parameters
        ----------
        signal : np.array
            Signal to be approximated.
        phase : np.array
            Argument of the sine. in `a + b*sin(c+d*t)` it would be `d*t`
        offset_opt : bool, optional.
            If False, the fit function is `b*sin(c + phase)`, else it is
            is `a + b*cos(c + phase)`. Default to True.
        plot : bool, optional.
            If True, plot the signal and the calculated sine together.
            Default to False.

        Returns
        -------
        offset : float
            The `a` in `a + b*cos(c + phase)`. If offset_opt is False, it is 0.
        amplitude : float
            The `b` in `a + b*cos(c + phase)`.
        phase_shift : float
            The `c` in `a + b*cos(c + phase)`.

    """

    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        raise TypeError('Arguments 3 and 4 must be booleans')

    offset, amp_cos, amp_sin = fit_sin_cos(signal, phase, offset_opt, False)

    amplitude = np.linalg.norm([amp_cos, amp_sin])
    # atan2 keeps the information of the sign of the b1 and b2
    phase_shift = -atan2(amp_sin, amp_cos)

    if plot:
        plt.figure('sktools::maths::fit_sine [{}]'
                   .format(len(plt.get_fignums())))
        y = offset + amplitude*np.cos(phase + phase_shift)
        plt.plot(phase, signal, '+r')
        plt.plot(phase, y, '-b')

        plt.grid(True)

    return offset, amplitude, phase_shift


def fit_sin_cos(signal, phase, offset_opt=True, plot=False):
    """ Find a sum of sine and cosine that fits with the signal.

        The funtion to fit with is
        `y = a + b1*cos(d*t) + b2*sin(d*t)`

        It internally uses a least square error method.

        Parameters
        ----------
        signal: np.array
            Signal to be approximated.
        phase: np.array
            Argument of the sine. in `a + b*cos(c+d*t)` it would be `d*t`
        offset_opt: bool, optional.
            If False, the fit function is `b*cos(c + phase)`, else it is
            is `a + b*cos(c + phase)`. Default to True.
        plot: bool, optional.
            If True, plot the signal and the calculated sine together.
            Default to False.

        Returns
        -------
        offset: float
            The `a` in `a + b1*sin(phase) + b2*cos(phase)`.
            If offset_opt is False, it is 0.
        amp_cos: float
            The `b1` in `a + b1*cos(phase) + b2*sin(phase)`.
        amp_sin: float
            The `b2` in `a + b1*cos(phase) + b2*sin(phase)`.

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
        raise ValueError('Arguments 1 and 2 must have the same length, '
                         'not {} and {}'
                         .format(signal.shape[0], phase.shape[0]))
    if phase.shape[1] != 1 or signal.shape[1] != 1:
        raise ValueError('Arguments 1 and 2 must be (n,1)-arrays')
    if not np.isscalar(offset_opt) or not np.isscalar(plot):
        raise TypeError('Arguments 4 and 5 must be booleans')

    if offset_opt:
        constant = np.ones(phase.shape)
    else:
        constant = np.zeros(phase.shape)

    # Solve the system equation
    eq_matrix = np.concatenate(
        (constant, np.cos(phase), np.sin(phase)),
        1
        )

    abc, residual, _, _ = np.linalg.lstsq(eq_matrix, signal)
    offset = abc[0, 0]
    amp_cos = abc[1, 0]
    amp_sin = abc[2, 0]

    if plot:
        plt.figure('sktools::maths::fit_sin_cos [{}]'
                   .format(len(plt.get_fignums())))
        y = offset + amp_cos*np.cos(phase) + amp_sin*np.sin(phase)
        plt.plot(phase, signal, '+r')
        plt.plot(phase, y, '-b')

        plt.grid(True)

    return offset, amp_cos, amp_sin


def extract_sin_cos(x, fs, f, output_format='cartesian'):
    """ Approximate the time signals by a funtion of type:
        `f(t) = a*cos(f*t) + b*sin(f*t)`.

        Parameters
        ----------
        x: np.array (nb_bpm x nb_time_samples)
            Each line is the signal of a given BPM.
        fs: float
            Sampling frequency.
        f: float
            Frequency to extract.
        output_format: string, optional, default to 'cartesian'.
            In which format the result should be output:
            'cartesian' or 'polar'

        Returns
        -------
        If 'cartesian':

        amp_cos: list
            Cosinus amplitude for each BPM (list of all `a`, nb_bpm elements).
        amp_sin: list
            Sinus amplitude for each BPM (list of all `b`, nb_bpm elements).

        If 'complex':

        value: list
            Complex amplitude for each BPM (`a + 1j*b`)

        If 'polar':

        amplitudes: list
            Amplitude for each BPM (`abs(a + j*b)`)
        phases: list
            Phases for each BPM (`angle(a + j*b)`)
    """

    def func(t, a, b, c, f):
        return a + b*np.cos(2*np.pi*f*t)+c*np.sin(2*np.pi*f*t)

    M, N = x.shape
    allowed_freqs = np.arange(N/2)*fs/N
    f0 = allowed_freqs[np.argmin(np.abs(f-allowed_freqs))]
    w0 = 2*np.pi*f0
    t = (np.arange(N)/fs).reshape((1, N)).repeat(M, axis=0)
    y = np.sum(x*np.exp(-1j*w0*t), axis=1)*2/N

    ampc = np.zeros(M)
    amps = np.zeros(M)

    for k in range(M):
        res, _ = optimize.curve_fit(func, t[k, :], x[k, :],
                                    [np.mean(x[k, :]), y.real[k], -y.imag[k], f])

        [_, ampc[k], amps[k], _] = res

    if output_format not in ['cartesian', 'polar']:
        print("Output format not understood fallback to default: 'cartesian'")
        output_format = 'cartesian'
    if output_format == 'cartesian':
        return ampc, amps
    elif output_format == 'polar':
        return np.abs(ampc +1j*amps), -np.angle(ampc + 1j*amps)


def klt(inputs):
    """ Apply the KLT to the input

        Parameters
        ----------
        input: np.array (signal_length x nb of dimensions)
            Each column represents a dimension of the signal.

        Returns
        -------
        output: np.array (signal_length x nb of dimensions)
            Each column represents a dimension of the signal.

    """

    covar = np.cov(inputs)
    val, vec = np.linalg.eig(covar)

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
        M: np.array (m x n)
            Matrix to compute
        nb_values: integer
            Number of eigenvalue to keep in the computation

        Returns
        -------
        M_inv: np.array (n x m)
            Pseudo inverse of M

    """

    try:
        M = M.newbyteorder('=')
    except AttributeError:
        pass

    U, s, V = np.linalg.svd(M, full_matrices=False)
    # S_mat = U * diag(s) * V
    idmax = nb_values
    Sred = np.diag(np.ones(idmax)/s[:idmax])
    Ured = U[:,:idmax]
    Vred = V[:idmax,:]

    M_inv = np.dot(Vred.conj().T, np.dot(Sred, Ured.conj().T))

    return M_inv
