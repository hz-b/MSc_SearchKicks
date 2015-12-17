#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")

import core as skcore


def test_fit_sinus(signal, phase):
    print("\n==========================")
    print("Start test for fit_sinus()")
    print("==========================")

    offset, amplitude, phase_shift = skcore.fit_sinus(signal,
                                                      phase,
                                                      'sum',
                                                      True,
                                                      True)

    offset2, amplitude2, phase_shift2 = skcore.fit_sinus(signal,
                                                         phase,
                                                         'inv',
                                                         True,
                                                         True)
    print("'sum'\n"
          "\toffset = {}\n"
          "\tamplitude = {}\n"
          "\tphase_shift = {}".format(offset,
                                      amplitude,
                                      phase_shift
                                      ))
    print("'inv'\n"
          "\toffset = {}\n"
          "\tamplitude = {}\n"
          "\tphase_shift = {}".format(offset2,
                                      amplitude2,
                                      phase_shift2
                                      ))

def test_fit_sin_cos(signal, phase):
    print("\n==========================")
    print("Start test for fit_sin_cos()")
    print("==========================")

    offset, amplitude_s, amplitude_c = skcore.fit_sin_cos(signal,
                                                        phase,
                                                        'sum',
                                                        True,
                                                        True)

    offset2, amplitude_s2, amplitude_c2 = skcore.fit_sin_cos(signal,
                                                           phase,
                                                           'inv',
                                                           True,
                                                           True)
    print("'sum'\n"
          "\toffset = {}\n"
          "\tamplitude sinus = {}\n"
          "\tamplitude cosinus = {}".format(offset,
                                            amplitude_s,
                                            amplitude_c
                                            ))
    print("'inv'\n"
          "\toffset = {}\n"
          "\tamplitude sinus = {}\n"
          "\tamplitude cosinus = {}".format(offset2,
                                            amplitude_s2,
                                            amplitude_c2
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
    orbit_full, phase_full = skcore.build_sinus(kick, tune, [1, 0])

    for i in range(phase.size):
        idx = np.argmin(abs(phase_full-phase[i]))
        orbit[i] = orbit_full[idx]

    orbit += 0.5*noise

    kick_found, _ = skcore.get_kick(orbit, phase, tune, True)
    print("kick set at {}".format(kick/(2*np.pi)))
    print("kick set found at {}".format(kick_found/(2*np.pi)))

if __name__ == "__main__":
    plt.close('all')

    phase = 2*np.pi*np.arange(1, 41).T/10
    signal_clean = 2*np.sin(phase+1.4) + 1
    noise = np.random.random(phase.size)*2 - 1
    signal = signal_clean + noise

    test_fit_sinus(signal, phase)
    test_fit_sin_cos(signal, phase)
    test_get_kick()
