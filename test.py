# -*- coding: utf-8 -*-

import scipy.io
import numpy as np
import search_kicks.core as skcore
# import PyML
import matplotlib.pyplot as plt

# plt.close('all')
# mml = PyML.PyML()
# mml.setao(mml.loadFromExtern('bessyIIinit.py', 'ao'))
#
# sx = mml.getfamilydata('BPMx', 'Pos')
# sy = mml.getfamilydata('BPMy', 'Pos')


# data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-41-34-ohneSOFB.mat')
# data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-57-56_vert10Hz')
data = scipy.io.loadmat('../_data/FastBPMData_2015-10-26_06-54-42horz10Hz')

valuesX = data['valuesX']
valuesY = data['valuesY']
freq = int(data['Freq'][0])

phases_mat = scipy.io.loadmat('phases.mat')
phaseX = phases_mat['PhaseX'][:, 0]
phaseY = phases_mat['PhaseZ'][:, 0]

tuneX = 17.8509864542659
tuneY = 6.74232980750181

s10Hz = 0
BPM_ids = np.concatenate((np.arange(8, 14),
                          np.arange(15, 40),
                          np.arange(41, 43),
                          np.arange(45, 54),
                          np.arange(55, 80),
                          np.arange(85, 126)
                          ))
sp_nb = valuesY.shape[1]
t = np.divide(np.arange(sp_nb), freq*np.ones(sp_nb))
f = np.fft.fftfreq(t.shape[-1])*freq

fftx = np.fft.fft(valuesX[0, :])
idx = abs(f-10) < 3
ref_freq = f[idx][np.argmax(abs(fftx[idx]))]

freq_max = []
freq_diff = []
for k in BPM_ids:
    fftx = np.fft.fft(valuesX[k, :])
    idx = abs(f-10) < 4
    freq_diff.append(f[idx][np.argmax(abs(fftx[idx]))] - ref_freq)
    freq_max.append(f[idx][np.argmax(abs(fftx[idx]))])

print(freq_max)
print(ref_freq)

a1 = []
a2 = []
for k in BPM_ids:
    phase = t*ref_freq

    _, b, c = skcore.fit_sinus(valuesY[k, :], phase)
    # a sin wt + b = a cos b sin wt + a sin b cos wt
    #              = a1 sin wt + a2 cos wt
    a1.append(b*np.cos(c))
    a2.append(b*np.sin(c))

a1 = np.array(a1)
a2 = np.array(a2)

plt.figure(0)
plt.plot(a1,a2,'+')

covA = np.cov(np.array([a1, a2]))
val, vec = np.linalg.eig(covA)
klt = np.dot(vec,np.array([a1, a2]))
plt.plot(klt[0,:],klt[1,:],'r+')

kicka1, coeffa1 = skcore.get_kick(a1, phaseY, tuneY, False)
kicka2, coeffa2 = skcore.get_kick(a2, phaseY, tuneY, False)

kik1 = np.argmin(abs(phaseY-kicka1))
kik2 = np.argmin(abs(phaseY-kicka2))

plt.figure('sinus')
plt.plot(sy[BPM_ids], a1, '-g')
plt.axvline(sy[BPM_ids][kik1], -2, 2)

plt.figure('cosinus')
plt.plot(sy[BPM_ids], a2, '-g')
plt.axvline(sy[BPM_ids][kik2], -2, 2)

print(sy[BPM_ids][kik1], sy[BPM_ids][kik2])