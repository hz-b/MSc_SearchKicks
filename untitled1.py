#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.io
import numpy as np
import search_kicks.core as skcore
import matplotlib.pyplot as plt

# data = scipy.io.loadmat('FastBPMData_2015-10-26_06-41-34-ohneSOFB.mat')
data = scipy.io.loadmat('../gety_end.mat')
phases_mat = scipy.io.loadmat('phases.mat')

orbit = data['orbit'][:, 0]
phase = phases_mat['PhaseZ'][:, 0]
tune = 6.7423

skcore.get_kick(orbit, phase,  tune, True)

#t = np.arange(0,6.01,0.01)
#x = 5*np.sin(t+0.125)+5*(2*np.random.random(t.size)-1)
#a,b,c = skcore.fit_sinus(x,t,False,True)
#print(a,b,c)
# data = scipy.io.loadmat('FastBPMData_2015-10-26_06-41-34-ohneSOFB.mat')
#data = scipy.io.loadmat('../gety_beg.mat')
#phases_mat = scipy.io.loadmat('phases.mat')
#
#orbit = data['orbit'][:, 0]
#phase = phases_mat['PhaseZ'][:, 0]
#Tune = 6.7423
#
#skcore.get_kick(orbit, phase,  Tune, True)