#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys
import os

__my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__my_dir+"/..")

import core as skcore


def test_fit_sinus():
    print("\n==========================")
    print("Start test for fit_sinus()")
    print("==========================")
    phase = 2*np.pi*np.arange(1, 21).T/10
    signal_clean = 2*np.sin(phase+1.4) + 1
    noise = np.random.random(phase.size)*2 - 1
    signal = signal_clean + noise

    offset, amplitude, phase_shift = skcore.fit_sinus(signal,
                                                      phase,
                                                      True,
                                                      True)
    print("offset = {}\namplitude = {}\nphase_shift = {}".format(offset,
                                                                 amplitude,
                                                                 phase_shift
                                                                 ))


# The created orbit doesn't work, because it must be smooth
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
    test_fit_sinus()
    test_get_kick()
