#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.io
import numpy as np
import search_kicks.core as skcore
import search_kicks.tools as sktools

import PyML
import matplotlib.pyplot as plt
import cmath

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
# data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-57-56_vert10Hz')
# data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-54-42horz10Hz')
data = scipy.io.loadmat('translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat')
valuesX, valuesY, _, _, BPMs_names, freq = sktools.IO.load_timeanalys('translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat')

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

freqs = np.fft.fftfreq(valuesX.shape[1], 1/freq)
freqs = freqs[:freqs.size/2]

BPMx_nb = valuesX.shape[0]

plt.figure('fft')
for i in range(BPMx_nb):
    fftx = np.fft.fft(valuesX[i, :])
    fftx = fftx[:fftx.size/2]
    fftx[0] = 0
    plt.plot(freqs, np.abs(fftx))


sp_nb = values.shape[1]
t = np.divide(np.arange(sp_nb), freq*np.ones(sp_nb))
f = np.fft.fftfreq(t.shape[-1], 1/freq)

fftx = np.fft.fft(values[0, :])
idx = abs(f-10) < 3
ref_freq = f[idx][np.argmax(abs(fftx[idx]))]

# FIXME: don't hardcode me.
ref_freq = 9.979248046875

freq_idx = idx=np.argmin(np.abs(ref_freq - f))

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

plt.figure("sin/cos")
plt.plot(ph,b1)
plt.plot(ph,b2)


#############
# GETSINCOS #
#############

A = []
B = []
t = np.arange(values[1,:].size)/freq

phase_sin = t*ref_freq
for k in active_bpms:
    _, A_t, B_t = skcore.fit_sin_cos(values[k, :], phase_sin, 'sum', False)
    A.append(A_t)
    B.append(B_t)

plt.figure("sin/cos 2")
plt.plot(ph,A)
plt.plot(ph,B)

#######
# SVD #
#######
U, s, V = np.linalg.svd(Smat, full_matrices=False)
# S_mat = U * diag(s) * V
idmax = 20
Sred = np.diag(np.ones(idmax)/s[:idmax])
Ured = U[:,:idmax]
Vred = V[:idmax,:]

S_inv = np.dot(Vred.conj().T, np.dot(Sred, Ured.conj().T))
r1 = np.dot(S_inv, b1)
r2 = np.dot(S_inv, b2)


plt.figure('CMs')
plt.plot(abs(r1))
plt.plot(abs(r2))
plt.legend(['sin', 'cos'])

############
# Get kick #
############
kicka1, coeffa1 = skcore.get_kick(np.array(b1), phase, tune, False)
kicka2, coeffa2 = skcore.get_kick(np.array(b2), phase, tune, False)

kik1 = np.argmin(abs(phase-kicka1))
kik2 = np.argmin(abs(phase-kicka2))

plt.figure('Orbits + kick')
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
