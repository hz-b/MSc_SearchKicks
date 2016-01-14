#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

f = 3
df = 0.2

t = np.linspace(0,10,100)

x_0 = np.sin(2*np.pi*f*t)
x_p = np.sin(2*np.pi*f*(1+df)*t)
x_m = np.sin(2*np.pi*f*(1-df)*t)

x = x_0 + 0.5*x_p + 0.5*x_m

plt.figure("Signal")
plt.plot(t,x)

fftx = np.fft.fft(x)/x.size
fx = np.fft.fftfreq(t.size, t[1])

plt.figure("fft")
plt.plot(fx, np.abs(fftx))

fx_id = np.argmin(abs(fx-f))

print('fft: {}'.format(2*np.abs(fftx[fx_id])))
print('sum: {}'.format(sum(x*x_0)*2/t.size))