#!/usr/bin/env python.
# -*- coding: utf-8 -*-

import numpy as np
from numpy import pi
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject

from mods.core.enumerations import OrbitSourceItems, DataSourceItems, AxisItems


class SearchKickBackend(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

    def search(axis, signal, fix_phase):
        betaX, betaY, px, py, tune = modelbeta('All')
        phaseX, phaseZ, sx, sz, tune = modelphase(Family)

        if axe == AxisItem.x:
            beta = betaX
            phase = phaseX
            tune = tune[1]
            ac_position = sx
        elif axe == AxisItem.y:
            beta = betaY
            phase = phaseZ
            tune = tune[2]
            acc_position = sy
        else:
            print("Family should be either BPMx or BPMy")

        nb_BPMs = size(family2elem(axis), 1)
        xfit = 0  # Variable to save the x in the best fit
        # Phase for the expanded data (we add behind the same signal)
        phase_expand = np.array([[phase-tune*2*pi], [phase]])
        funk = np.array([[signal], [signal]])  # Function with duplicated data

        # This will be the RMS of the different positions for the kicks
        RMS_pos = zeros(1, nb_BPMs)
        coeff = 0  # Coefficients for the best fit
        phase_kick = 0  # Variable to save to phases of the posible kicks

        for i in range(nb_BPMs):
            # [i,b] is the interval to fit, taking into account that we
            # have numBPMs*2 data (it's duplicated)
            b = i+nb_BPMs
            st = funk[i:b]  # Piece of signal to compare
            xt = phase_expand[i:b]  # Equivalent piece from the phase

            a, b, c = fit_sinus('OffsetOFF', st, xt, v1)

            # We don't use the a coefficient (it's cero), we reduce a degree
            # of freedom
            y = a + b*sin(c + xt)

            RMS_pos[i] = sum(pow(y - st, 2))

            # Intervals where to look for the kick, it depends in which part
            # of the phase we are
            start = phase[i]
            if i == nb_BPMs:
                end = phase(1) + 2*pi*tune
            else:
                end = phase(i+1)

            # interval to look for the minimun (we allow it to be in between
            # two BPMs in each case)
            interval = np.linspace(start, end, 1000)
            C, I = min(abs(
                    (b*sin(interval + c)) - (b*sin(interval+c-2*pi*tune))
                ))
            phase_kick[i] = interval[I]

            # the first time we save the fit
            # + Logic condition that save the sin that fit best to the function
            if i == 1 or RMS_pos[i] < BestFit:
                bestFit = RMSpos[i]
                index = i
                xfit = xt  # Saving the phase to plot...
                coeff = np.array([[a, b, c]])

            # Logic condition in order to have the phase fixed
            # If this occurs then we have an specific point to look for
            # in the phase
            if fix_phase != 0 and i < nb_BPMs and phase[i+1] > fix_phase:
                BestFitF = RMSpos(i)
                indexF = i
                # Saving the specifications for the kick in the specific point
                xfitF = xt
                coeffF = np.array([[a, b, c]])
                PhasekickF = interval[I]

                # Once we are in, we have the data we want (we don't need to
                # compare more RMS, because we have the kick point predefined),
                # so we go out
                break

        # Now we check if the kick point is correct (if the two sinus
        # match), if it doesn't match we swept again the interval looking
        # for a best fit (but with the sinus fitted in the last for)
        comp = 0

        if abs(coeff[2]*sin(phase_kick[index] + coeff[3]) -
                coeff[2]*sin(phase_kick[index]+coeff[3]-2*pi*tune)
               ) > 1e7:

            if index == 1:
                start = phase[nb_BPMs]-2*pi*tune
                end = phase[1]
            elif index == nb_BPMs:
                start = phase[nb_BPMs]
                end = phase[1]+2*pi*tune
            else:
                start = phase[index-1]
                end = phase[index+1]

            # interval to look for the minimun (we allow it to be just in
            # between 3 near BPM)
            interval = np.linspace(start, end, 50000)
            C, I = min(abs(coeff(2)*sin(interval + coeff[3]) -
                coeff[2]*sin(interval + coeff[3] - 2*pi*tune)))
            phase_kick[index] = interval[I]
            comp = 1

        if abs(coeff[2]*sin(phase_kick[index] + coeff[3]) -
                coeff[2]*sin(phase_kick[index]+coeff[3]-2*pi*tune)
                ) > coeff[2]/4:
            # If the range is still big (there is no match in our region)
            # we look for a bigger region
            if index <= 11:
                start = phase[nb_BPMs-10]-2*pi*tune
                end = phase[8]
            elif index >= nb_BPMs-9:
                start = phase[nb_BPMs-10]
                end = phase[8]+2*pi*tune
            else:
                start = phase[index-10]
                end = phase[index+10]

            # interval to look for the minimun (we allow
            interval = np.linspace(start, end, 50000)
            C, I = min(abs(coeff[2]*sin(interval + coeff[3]) -
                coeff[2]*sin(interval + coeff[3] - 2*pi*tune)))
            phase_kick[index] = interval[I]
            comp = 2

        # Position of the kick in the phase
        phaseKickPosition = phase_kick[index]

        # In case we require an specific phase kick (ficKick)
        # we use that values related to that kick
        if fixPhase != 0:
            PhaseKickPosition = PhasekickF
            coeff = coeffF

        # With the next function, we get much more values in the phase (1247)
        phaseX, phaseZ, sx, sy, tune = modeltwiss("Phase")

        if axis == AxisItem.x:
            phase = phaseX
            tune = tune[1]
            acc_position = sx
        elif axis == AxisItem.x:
            phase = phaseZ
            tune = tune[2]
            acc_position = sy

        # Now we are going to compute some parameters, we need the point of
        # the position in the accelerator and the beta functionin those points,
        # then we interpolate
        maxIndexBeta = length(beta)

        BPMinterpolbottom = find(Phase < PhaseKickPosition)
        BPMinterpolbottom = length(BPMinterpolbottom)

        if BPMinterpolbottom == 0:
            # If the BPMinterpolbottom is 0 we interpolate inbetween
            # (Phase(max) - 2*pi*Tune) and Phase(1)

            RealPosition = 0 + (acc_position[BPMinterpolbottom + 1] - 0) * ((PhaseKickPosition - 0) /(Phase[BPMinterpolbottom + 1] - 0))

            BetaInterpol = beta[maxIndexBeta] + (beta[BPMinterpolbottom + 1] - beta[maxIndexBeta]) *((PhaseKickPosition - Phase[maxIndexBeta] + 2*pi*tune)/(Phase[BPMinterpolbottom + 1] - phase[maxIndexBeta] + 2*pi*tune))

        elif BPMinterpolbottom == maxIndexBeta:
            # If the BPMinterpolbottom is the last number of the BPM we
            # interpolate inbetween Phase(max) and (Phase(max) + 2*pi*Tune)

            RealPosition = acc_position[BPMinterpolbottom] + (240.00839012 - acc_position[BPMinterpolbottom])*((PhaseKickPosition - phase[BPMinterpolbottom])/(2*pi*tune - phase[BPMinterpolbottom]))

            BetaInterpol = beta[BPMinterpolbottom] + (beta[1] - beta[BPMinterpolbottom])*((PhaseKickPosition - Phase[BPMinterpolbottom])/(phase[1] + 2*pi*tune - phase[BPMinterpolbottom]))

        else:
            RealPosition = AccPosition(BPMinterpolbottom) + (AccPosition(BPMinterpolbottom + 1) - AccPosition(BPMinterpolbottom)) *((PhaseKickPosition - Phase(BPMinterpolbottom)) /(Phase(BPMinterpolbottom + 1) - Phase(BPMinterpolbottom)))

            BetaInterpol = Beta(BPMinterpolbottom) + (Beta(BPMinterpolbottom + 1) - Beta(BPMinterpolbottom)) *((PhaseKickPosition - Phase(BPMinterpolbottom)) /(Phase(BPMinterpolbottom + 1) - Phase(BPMinterpolbottom)))

        strength = 2*tan(tune*pi)*(a + coeff[2]*sin(coeff[3] + PhaseKickPosition))/BetaInterpol

        # Set the output
        point_phase = phase_kick_position
        pos = real_position

        return point_phase, position, strength, phexp, funk,
        phase_kick_position, coeff, beta_interpol, comp
