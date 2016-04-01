#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/PyML")
sys.path.append(__my_dir+"/search_kicks")

import scipy.io
import numpy as np
import search_kicks.core as skcore
import search_kicks.tools as sktools
import PyML
import matplotlib.pyplot as plt
from zmq_client import *

DEFAULT_DATA = 'search_kicks/search_kicks/default_data/'
PHASE_FILE = DEFAULT_DATA + 'phases.mat'
SMAT_FILE = DEFAULT_DATA + 'Smat-CM-Standard_HMI.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-57-56_vert10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-54-42_horz10Hz.mat'
#DATA_FILE = '../../_data/translated_FastBPMData_2015-10-26_06-39-01-ohne_10Hz.mat'
#AXIS = 'x'
AXIS = 'y'

# Hardcoded constants
tuneX = 17.8509864542659
tuneY = 6.74232980750181
ref_freq = 10#9.979248046875
fs = 150 #Hz
SAMPLE_NB = 1000

def parse_frames(messages):
    sample_nb = len(messages)
    bpm_nb = np.fromstring(messages[0][2], dtype='double').size

    valuesX = np.zeros((bpm_nb, sample_nb))
    valuesY = np.zeros((bpm_nb, sample_nb))

    # parse frames in values X
    for count, message in enumerate(messages):
        valuesX[:, count] = np.fromstring(message[2], dtype='double')
        valuesY[:, count] = np.fromstring(message[3], dtype='double')
        
    return valuesX, valuesY

if __name__=='__main__':
    if len(sys.argv) > 1:
        ref_freq = float(sys.argv[1])

    plt.close('all')
    pml = PyML.PyML()
    pml.setao(pml.loadFromExtern('search_kicks/external/bessyIIinit.py', 'ao'))
    pml.loadBPMOffsets('/opt/OPI/MapperApplications/conf/Orbit/SR/RefOrbit.Dat')

    active_bpmsx = pml.getActiveIdx('BPMx')
    active_bpmsy = pml.getActiveIdx('BPMy')

    sx = pml.getfamilydata('BPMx', 'Pos')
    sy = pml.getfamilydata('BPMy', 'Pos')

    namesX = pml.getfamilydata('BPMx', 'CommonNames')
    namesY = pml.getfamilydata('BPMx', 'CommonNames')

    Smat_xx, Smat_yy = sktools.IO.load_Smat(SMAT_FILE)
    Smat_xx = Smat_xx[active_bpmsx, :]
    Smat_yy = Smat_yy[active_bpmsy, :]

    #idx = pml.family2idx('BPMx')
    #idy = pml.family2idx('BPMy')

    #offsetx = pml.getfamilydata('BPMx','Offset',None,idx)
    #offsety = pml.getfamilydata('BPMy','Offset',None,idy)

    zclient = ZmqClient()
    zclient.connect("tcp://gofbz12c.ctl.bessy.de:5563")
    zclient.subscribe(['FOFB-BPM-DATA'])
    messages = zclient.receive(SAMPLE_NB)
   
    valuesX, valuesY = parse_frames(messages)

    phases_mat = scipy.io.loadmat(PHASE_FILE)
    phaseX = np.delete(phases_mat['PhaseX'][:, 0], 38)
    phaseY = np.delete(phases_mat['PhaseZ'][:, 0], 38)

    if AXIS == 'y':
        pos = sy[active_bpmsy]
        Smat = Smat_yy
        phase = phaseY
        tune = tuneY
        values = valuesY#[active_bpms, :]
        names = namesY[active_bpmsy]
    elif AXIS == 'x':
        pos = sx[active_bpmsx]
        Smat = Smat_xx
        phase = phaseX
        tune = tuneX
        values = valuesX#[active_bpms, :]
        names = namesX[active_bpmsx]

    sample_nb = values.shape[1]

    # Extract sin cos
    asin, acos = sktools.maths.extract_sin_cos(values, fs, ref_freq, 'fft')

    plt.figure("sin/cos")
    plt.plot(pos, asin)
    plt.plot(pos, acos)
    plt.legend(['sin','cos'])
    plt.title('With fft')

    # Optimize
    step_size = 0.1
    asin_opt, acos_opt, _ = sktools.maths.optimize_rotation(asin, acos, step_size)
    A = [asin, acos]
    klt = sktools.maths.klt(A)

    plt.figure("optimisaton")
    plt.subplot(2,1,1)
    plt.title("Rotation")
    plt.plot(pos, asin_opt)
    plt.plot(pos, acos_opt)
    plt.legend(['sin','cos'])
    plt.subplot(2,1,2)
    plt.title("KLT")
    plt.plot(pos, klt[0])
    plt.plot(pos, klt[1])

    # Correction fft
    S_inv = sktools.maths.inverse_with_svd(Smat, 32)

    # Kick fft
    phase_kick, coeff = skcore.get_kick(np.array(asin_opt), phase, tune, True, True)
    kick_idx = np.argmin(abs(phase-phase_kick))
    corr = np.dot(S_inv, asin_opt)

    # Kick fft
    phase_kick_cos, coeff = skcore.get_kick(np.array(acos_opt), phase, tune, True,True)
    kick_idx_cos = np.argmin(abs(phase-phase_kick_cos))

    plt.figure('CMs, kick')
    plt.subplot(2, 1, 1)
    plt.plot(corr)
    plt.title('Correctors for f = {} Hz'.format(ref_freq))
    

    plt.subplot(2, 1, 2)
    plt.plot(pos, asin_opt, '-g')
    plt.axvline(pos[kick_idx], -2, 2)
    plt.title('kick in sine component for f = {} Hz'.format(ref_freq))

    print("sin = " + names[kick_idx])
    corr_cos = np.dot(S_inv, acos_opt)

    plt.figure('CMs, kick cos')
    plt.subplot(2, 1, 1)
    plt.plot(corr_cos)
    plt.title('Correctors for f = {} Hz [cos]'.format(ref_freq))
    

    plt.subplot(2, 1, 2)
    plt.plot(pos, acos_opt, '-g')
    plt.axvline(pos[kick_idx_cos], -2, 2)
    plt.title('kick in sine component for f = {} Hz [cos]'.format(ref_freq))

    print("cos = " + names[kick_idx_cos])
    plt.show()
