#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/../..")

import search_kicks.core as skcore
import search_kicks.tools as sktools


def test_fit_sine(signal, phase):
    print("\n==========================")
    print("Start test for fit_sine()")
    print("==========================")

    offset, amplitude, phase_shift = sktools.maths.fit_sine(signal,
                                                            phase,
                                                            True,
                                                            True)

    print(""
          "\toffset = {}\n"
          "\tamplitude = {}\n"
          "\tphase_shift = {}".format(offset,
                                      amplitude,
                                      phase_shift,
                                      ))

def test_fit_sin_cos(signal, phase):
    print("\n==========================")
    print("Start test for fit_sin_cos()")
    print("==========================")

    offset, amplitude_c, amplitude_s = sktools.maths.fit_sin_cos(signal,
                                                                 phase,
                                                                 True,
                                                                 True)

    print(""
          "\toffset = {}\n"
          "\tamplitude sine = {}\n"
          "\tamplitude cosine = {}".format(offset,
                                            amplitude_s,
                                            amplitude_c
                                            ))

# The created orbit doesn't work, because it must be smooth [closed orbit]
def test_get_kick():
    print("\n=========================")
    print("Start test for get_kick()")
    print("=========================")
    bpm_nb = 30
    i = 13  # BPM before kick
    away_ratio = 0.5

    tune = 6.5
    phase = np.linspace(0, 2*np.pi*tune*.95, bpm_nb)
    orbit = np.zeros(bpm_nb)
    noise = np.random.normal(0, 1, bpm_nb)

    kick = phase[i]+(phase[i+1]-phase[i])*away_ratio
    orbit_full, phase_full = skcore.build_sine(kick, tune, [1, 0])

    for i in range(phase.size):
        idx = np.argmin(abs(phase_full-phase[i]))
        orbit[i] = orbit_full[idx]

    orbit += 0.1*noise

    kick_found, _ = skcore.get_kick(orbit, phase, tune, True, True)
    print("kick set at {}".format(kick/(2*np.pi)))
    print("kick set found at {}".format(kick_found/(2*np.pi)))

if __name__ == "__main__":
    plt.close('all')
    phase = 2*np.pi*np.arange(1, 41).T/10
    signal_clean = 2*np.cos(phase+1.4) + 1
    noise = np.random.random(phase.size)*2 - 1
    signal = signal_clean + noise

    test_fit_sine(signal, phase)
    test_fit_sin_cos(signal, phase)
    test_get_kick()
    plt.show()
