#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys
sys.path.append("..")
import core


def test_fit_sinus():
    print("\n==========================")
    print("Start test for fit_sinus()")
    print("==========================")
    phase = 2*np.pi*np.arange(1, 21).T/10
    signal_clean = 2*np.sin(phase+1.4) + 1
    noise = np.random.random(phase.size)*2 - 1
    signal = signal_clean + noise

    offset, amplitude, phase_shift = core.fit_sinus(signal, phase, True, True)
    print("offset = {}\namplitude = {}\nphase_shift = {}".format(offset,
                                                                 amplitude,
                                                                 phase_shift
                                                                 ))


def test_get_kick():
    print("\n=========================")
    print("Start test for get_kick()")
    print("=========================")
    bpm_nb = 30
    i = 13  # BPM before kick
    away_ratio = 0.2

    tune = 6.5
    phase = np.linspace(0, 2*np.pi*tune, bpm_nb)

    noise = 2*np.random.random(30)-1

    kick = phase[i]+(phase[i+1]-phase[i])*away_ratio
    orbit = np.concatenate((
        np.sin(phase[:i]),
        np.sin(2*(kick)-phase[i:])
        )) + 0.5*noise

    kick_found, _ = core.get_kick(orbit, phase, tune, True)
    print("kick set at {}".format(kick/(2*np.pi)))
    print("kick set found at {}".format(kick_found/(2*np.pi)))

if __name__ == "__main__":
    test_fit_sinus()
    test_get_kick()
