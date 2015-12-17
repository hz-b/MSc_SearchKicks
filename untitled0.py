#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.io
import numpy as np
import search_kicks.core as skcore
import PyML
import matplotlib.pyplot as plt
import cmath

def function_sin_cos(ref_freq, values, fs, ph):
    A = []
    B = []
    t = np.arange(values[1,:].size)/freq

    phase_sin = t*ref_freq
    for k in active_bpms:
        _, A_t, B_t = skcore.fit_sin_cos(values[k, :], phase_sin, 'sum', False)
        A.append(A_t)
        B.append(B_t)

    plt.figure("sin/cos")
    plt.plot(ph,A)
    plt.plot(ph,B)

    return A,B

def function_fft(ref_freq, values, freq, ph):
    t = np.divide(np.arange(sp_nb), freq*np.ones(sp_nb))
    f = np.fft.fftfreq(t.shape[-1], 1/freq)
    freq_idx=np.argmin(np.abs(ref_freq - f))
    print('+++++++++')
    print(f[freq_idx])
    print('+++++++++')

    b1 = []
    b2 = []

    fftx = np.fft.fft(values[0, :])[freq_idx]
    amp,phi=cmath.polar(1./fftx)
    rot=cmath.rect(1.,phi)

    for k in active_bpms:
        fftxk = np.fft.fft(values[k, :])[freq_idx]#*rot*amp
        b1.append(fftxk.real)
        b2.append(fftxk.imag)

    plt.figure("sin/cos fft")
    plt.plot(ph,b1)
    plt.plot(ph,b2)

    return b1,b2

def do_svd(A,B,Smat,title):
    U, s, V = np.linalg.svd(Smat, full_matrices=False)
    # S_mat = U * diag(s) * V
    idmax = 20
    Sred = np.diag(np.ones(idmax)/s[:idmax])
    Ured = U[:,:idmax]
    Vred = V[:idmax,:]

    S_inv = np.dot(Vred.conj().T, np.dot(Sred, Ured.conj().T))
    r1 = np.dot(S_inv, A)
    r2 = np.dot(S_inv, B)


    plt.figure('CMs with '+title)
    plt.plot(abs(r1))
    plt.plot(abs(r2))
    plt.legend(['sin', 'cos'])

if __name__=='__main__':
    plt.close('all')
    mml = PyML.PyML()
    mml.setao(mml.loadFromExtern('bessyIIinit.py', 'ao'))

    active_bpms = mml.getActiveIdx('BPMx')
    #
    sx = mml.getfamilydata('BPMx', 'Pos')
    sy = mml.getfamilydata('BPMy', 'Pos')

    namesX = mml.getfamilydata('BPMx', 'CommonNames')
    namesY = mml.getfamilydata('BPMx', 'CommonNames')


    smat = scipy.io.loadmat('../_data/Smat-CM-Standard_HMI.mat')
    Smat_xx = smat['Rmat'][0, 0]['Data'][active_bpms, :]
    Smat_yy = smat['Rmat'][1, 1]['Data'][active_bpms, :]

    #data = scipy.io.loadmat(
    #    '../_data/FastBPMData_2015-10-26_06-41-34-ohneSOFB.mat'
    #    )
    data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-57-56_vert10Hz')
    #data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-54-42horz10Hz')

    valuesX = data['valuesX']
    valuesY = data['valuesY']
    freq = float(data['Freq'][0])

    phases_mat = scipy.io.loadmat('phases.mat')
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    tuneX = 17.8509864542659
    tuneY = 6.74232980750181

    ph = sy[active_bpms]
    Smat = Smat_yy
    phase = phaseY
    tune = tuneY
    values = valuesY
    names = namesY

    sp_nb = values.shape[1]


    fftx = np.fft.fft(values[0, :])

    # FIXME: don't hardcode me.
    ref_freq = 9.979248046875

    A,B = function_sin_cos(ref_freq, values, freq, ph)
    b1,b2 = function_fft (ref_freq, values, freq, ph)

    do_svd(b1,b2, Smat, 'fft')
    do_svd(A,B, Smat, 'sin_cos')


    ############
    # Get kick #
    ############
    kicka1, coeffa1 = skcore.get_kick(np.array(b1), phase, tune, False)
    kicka2, coeffa2 = skcore.get_kick(np.array(b2), phase, tune, False)

    kik1 = np.argmin(abs(phase-kicka1))
    kik2 = np.argmin(abs(phase-kicka2))

    plt.figure('Orbits + kick with sincos')
    plt.subplot(2, 1, 1)
    plt.plot(ph, A, '-g')
    #plt.plot(np.linspace(0,250), max(a1)*.2*np.sin(10*np.linspace(0,250)), '-b')
    plt.axvline(ph[kik1], -2, 2)
    plt.title('sinus')

    plt.subplot(2, 1, 2)
    plt.plot(ph, B, '-g')
    plt.axvline(ph[kik2], -2, 2)
    plt.title('cosinus')
    print(names[active_bpms][kik1], names[active_bpms][kik2])

    ############
    # Get kick #
    ############
    kicka1, coeffa1 = skcore.get_kick(np.array(b1), phase, tune, False)
    kicka2, coeffa2 = skcore.get_kick(np.array(b2), phase, tune, False)

    kik1 = np.argmin(abs(phase-kicka1))
    kik2 = np.argmin(abs(phase-kicka2))

    plt.figure('Orbits + kick with  fft')
    plt.subplot(2, 1, 1)
    plt.plot(ph, b1, '-g')
    #plt.plot(np.linspace(0,250), max(a1)*.2*np.sin(10*np.linspace(0,250)), '-b')
    plt.axvline(ph[kik1], -2, 2)
    plt.title('sinus')

    plt.subplot(2, 1, 2)
    plt.plot(ph, b2, '-g')
    plt.axvline(ph[kik2], -2, 2)
    plt.title('cosinus')
    print(names[active_bpms][kik1], names[active_bpms][kik2])

    ######
