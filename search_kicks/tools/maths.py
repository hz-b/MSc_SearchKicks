# -*- coding: utf-8 -*-

import numpy as np

def rotate(sin_amp, cos_amp, phi, deg_rad='rad'):
    if deg_rad == 'deg':
        phi = phi*np.pi/180.
    elif deg_rad == 'rad':
        pass
    else:
        raise ValueError("2nd argument must be 'deg' or 'rad'")


    z = cos_amp + 1j*sin_amp
    z = z* np.exp(1j*phi)

    return z.imag, z.real