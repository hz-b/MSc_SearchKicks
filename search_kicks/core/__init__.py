#!/usr/bin/env python.
# -*- coding: utf-8 -*-

""" search_kick.core contains the relevant function for the analysis and can
    used as a simple library or toolbox.
"""

__author__ = "Olivier CHURLAUD"
__version__ = "0.1.0"
__maintainer__ = ""
__email__ = "olivier.churlaud@helmholtz-berlin.de"
__status__ = "Developpement"


from .build_sine import build_sine
from .fit_sine import fit_sine, fit_sin_cos
from .get_kick import get_kick
from .time_analysis import extract_cos_sin_withfft