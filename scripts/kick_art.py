#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, __my_dir+"/..")
sys.path.append(__my_dir+"/../../PyML")

import scipy.io
import numpy as np
import search_kicks.core as skcore
import search_kicks.tools as sktools
import PyML
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set_style("ticks")
    seaborn = True
except:
    seaborn = False

DEFAULT_DATA = '../search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-57-56_vert10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-39-01-ohne_10Hz.mat'
AXIS = 'y'
#AXIS = 'x'

# Hardcoded constants
tuneX = 17.8509864542659
tuneY = 6.74232980750181
# -*- coding: utf-8 -*-

def art_main(cidx, plotopt=True):
    print('I set cidx to {}'.format(cidx))
    plt.close('all')
    pml = PyML.PyML()
    pml.setao(pml.loadFromExtern('../../PyML/config/bessyIIinit.py', 'ao'))

    active_bpmsx = pml.getActiveIdx('BPMx')
    active_bpmsy = pml.getActiveIdx('BPMy')

    sx = pml.getfamilydata('BPMx', 'Pos')
    sy = pml.getfamilydata('BPMy', 'Pos')

    cx = pml.getfamilydata('HCM', 'Pos')[pml.getActiveIdx('HCM')]
    cy = pml.getfamilydata('VCM', 'Pos')[pml.getActiveIdx('VCM')]

    namesX = pml.getfamilydata('BPMx', 'CommonNames')
    namesY = pml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.io.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpmsx, :]
    Smat_yy = Smat_yy[active_bpmsy, :]

    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = phases_mat['PhaseX'][:, 0]
    phaseY = phases_mat['PhaseZ'][:, 0]

    if AXIS == 'y':
        pos_cor = cy
        pos = sy[active_bpmsy]
        Smat = Smat_yy
        phase = phaseY
        tune = tuneY
        names = namesY[active_bpmsy]
    elif AXIS == 'x':
        pos_cor = cx
        pos = sx[active_bpmsx]
        Smat = Smat_xx
        phase = phaseX
        tune = tuneX
        names = namesX[active_bpmsx]

    corr = np.zeros(Smat.shape[1])
    corr[cidx] = 1
    values = np.dot(Smat,corr)
    S_inv = sktools.maths.inverse_with_svd(Smat, 32)

    r1 = np.dot(S_inv, values)

    if plotopt:
        plt.figure('CMs')
        plt.plot(pos_cor, r1)
        plt.ylabel('Amplitude of correction')
        plt.xlabel('Position [in m]')
        plt.title('Correctors')
        plt.grid('on')
        if seaborn:
            sns.despine()

    # Kick
    kicka1, coeffa1 = skcore.get_kick(np.array(values), phase, tune, plotopt, plotopt)

    kik1 = np.argmin(abs(phase-kicka1))

    if plotopt:
        plt.figure('Orbits + kick')
        plt.plot(pos, values, '-g')
        plt.axvline(pos[kik1], -2, 2)
        plt.ylabel('Distance to ref. orbit [in m]')
        plt.xlabel('Position [in m]')
        plt.grid('on')
        if seaborn:
            sns.despine()

    if pos[kik1] == pos_cor[cidx]:
        text = names[kik1] + ' Good job!'
    else:
        val = abs(pos_cor[cidx]-pos[kik1])
        if val > 240/2:
            val = 240-val
        text = 'idx {} = {} found, d={}'.format(kik1, names[kik1], val)
    print(text)
    shouldidx = np.argmin(abs(pos-pos_cor[cidx]))
    print('It should have been idx {} = {}'.format(shouldidx,names[shouldidx]))
    if plotopt:
        for i in plt.get_fignums():
            plt.figure(num=i)
            if seaborn:
                sns.despine()
            plt.grid('on')
#            plt.savefig(str(i)+'.pdf')
        plt.show()
    return val

if __name__=='__main__':
    if len(sys.argv) == 1:
        cidx = np.random.randint(0, 64)
        art_main(cidx)
    elif sys.argv[1] == 'all':
        t = []
        for k in range(64):
            t.append(art_main(k, False))
        plt.figure()
        plt.plot(t)
        plt.xlabel('Corrector moved [index]')
        plt.ylabel('Distance: error of localization [in m]')
        plt.grid('on')
        if seaborn:
            sns.despine()
#       plt.savefig('all.pdf')
        plt.show()
    else:
        cidx = int(sys.argv[1])
        art_main(cidx)
