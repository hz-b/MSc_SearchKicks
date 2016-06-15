#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IO Module
=========

Load/Save time data from multiple supports and formats.

Note
----
It's better to use these function in a try/except structure as they raise
errors whenever something goes wrong.

@author: Olivier CHURLAUD <olivier.churlaud@helmholtz-berlin.de>
"""

import csv
from datetime import datetime, timedelta
import locale
import os

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except:
    from urllib import urlopen, urlencode

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

DATETIME_ISO = "%Y-%m-%dT%H:%M:%S.%f"


def load_orbit(*args):
    """ Load an orbit.

    This uses function only calls other functions based on the number and
    values of its arguments.

    Raises
    -------
    ValueError:
        If the arguments don't fit any known case.
    Exception:
        If underlying function return exceptions.
    """

    if len(args) == 1:  # can only be a file
        filename = args[0]
        ext = os.path.splitext(filename)[1]
        if ext == ".hdf5":
            try:
                return load_orbit_hdf5(filename)
            except Exception:
                raise
        elif ext == ".mat":
            try:
                return load_orbit_dump(filename)
            except Exception:
                raise
        elif ext == '.npy':
            try:
                return load_orbit_npy(filename)
            except Exception:
                raise
        else:
            raise ValueError("I don't know how to load this type of file '{}'."
                             .format(filename))
    elif len(args) == 2 or len(args) == 3:
        return load_orbit_from_archiver(*args)
    else:
        raise ValueError("This function has 1, 2 or 3 arguments.")


class OrbitData(object):
    """ Data container class that should be used in the programs.

    The users of this module should use this class to work in an abstract way
    with the data.

    If the object cannot be constructed, an exception is raised.

    """

    def __init__(self, BPMx=None, BPMy=None, CMx=None, CMy=None, names=None,
                 sampling_frequency=None, measure_date=None):

        sample_nb = 0

        def check_single_arrays(name, item, sample_nb):
            if item is None:
                return

            if type(item) is not np.ndarray:
                raise TypeError("{} type must be ndarrays, not {}."
                                .format(name, type(item)))
            if item.ndim != 2:
                raise ValueError("{} must be a 2-dimensional arrays."
                                 .format(name))

            if sample_nb and sample_nb != item.shape[1]:
                raise ValueError("All arrays must have the same number of "
                                 "samples, {} has {}, an other has {}."
                                 .format(name, item.shape[1], sample_nb))
            else:
                sample_nb = item.shape[1]
            return sample_nb

        sample_nb = check_single_arrays('BPMx', BPMx, sample_nb)
        sample_nb = check_single_arrays('BPMy', BPMy, sample_nb)
        sample_nb = check_single_arrays('CMx', CMx, sample_nb)
        sample_nb = check_single_arrays('CMy', CMy, sample_nb)

        if names is None:
            names = {'BPMx': None, 'BPMy': None, 'CMx': None, 'CMy': None}
        elif type(names) is not dict:
            print("Names should be None or a dictionary: discarded.")
        elif ('BPMx' not in names.keys() or 'BPMy' not in names.keys() or
              'CMx' not in names.keys() or 'CMy' not in names.keys()):
            print("Names should contain BPMx, BPMy, CMx, CMy: discarded.")
        elif (len(names['BPMx']) != BPMx.shape[0] or
              len(names['BPMy']) != BPMy.shape[0] or
              len(names['CMx']) != CMx.shape[0] or
              len(names['CMy']) != CMy.shape[0]):
            print("Names should have the same length as corresponding objects "
                  "first dimension: discarded.")
        self.BPMx = BPMx
        self.BPMy = BPMy
        self.CMx = CMx
        self.CMy = CMy
        self.sampling_frequency = float(sampling_frequency)
        self.sample_number = sample_nb
        self.measure_date = measure_date
        self.time = np.arange(self.sample_number)/self.sampling_frequency
        self.names = names

    def _plot_single_fft(self, x, i, title, ylabel):
        N = x.shape[1]
        freqs = np.fft.fftfreq(N, 1/self.sampling_frequency)[:N//2]
        X = np.fft.fft(x[i, :])[:N//2]*2/N*10**6
        X[0] = 0
        plt.plot(freqs, abs(X))
        plt.title(title)
        plt.xlabel('Frequency [in Hz]')
        plt.ylabel(ylabel)
        plt.grid()

    def plot_fft(self, which=0, title="", opt=""):
        if which == 0:
            which = [0,0,0,0]
        elif len(which) == 2 and opt == "no_CM":
            which.extend([0, 0])
        elif len(which) == 2 and opt == "no_BPM":
            which = [0, 0].extend(which)
        elif len(which) != 4:
            raise ValueError("1st argument (which) must be a list with 4 elements")

        if opt not in ["", "no_CM", "no_BPM"]:
            raise ValueError("3rd argument (opt) can be 'no_CM', 'no_BPM' or "
                             "empty, but not {}".format(opt))

        if opt == "":
            h_nb = 2
        else:
            h_nb = 1
        if opt != "no_BPM":
            plt.subplot(h_nb, 2, 1)
            self._plot_single_fft(self.BPMx, which[0], "BPMx", 'Beam motion [in nm]')
            plt.subplot(h_nb, 2, 2)
            self._plot_single_fft(self.BPMy, which[1], "BPMy", 'Beam motion [in nm]')
        if opt != "no_CM":
            plt.subplot(h_nb, 2, 2*(h_nb-1) + 1)
            self._plot_single_fft(self.CMx, which[2], "CMx", 'Correction [in uA]')
            plt.subplot(h_nb, 2, 2*(h_nb-1) + 2)
            self._plot_single_fft(self.CMy, which[3], "CMy", 'Correction [in uA]')
            plt.tight_layout()

    @property
    def datetime(self):
        return self.measure_date + timedelta(seconds=1)*self.time


def load_golden_orbit(filename):
    """ This should be in PyML
    """
    names = []
    orbitX = []
    orbitY = []
    try:
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                names.append(row[0].replace(' ', ''))
                orbitX.append(float(row[1]))
                orbitY.append(float(row[2]))
    except Exception:
        raise
    else:
        return np.array(orbitX), np.array(orbitY), names


def load_orbit_npy(filename):

    try:
        data = np.load(filename)[0]
    except Exception:
        raise
    else:
        if '__version__' not in data:
            raise ValueError("Version of data not set")

        if data['__version__'] == '1.0':
            try:
                return OrbitData(
                    BPMx=data['BPMx'], BPMy=data['BPMy'],
                    CMx=data['CMx'], CMy=data['CMy'],
                    sampling_frequency=data['sampling_frequency'],
                    names=data['names'],
                    measure_date=datetime.strptime(data['measure_date'],
                                                   DATETIME_ISO)
                    )
            except Exception:
                raise
        else:
            raise NotImplementedError("The version {} is unknown to me, "
                                      "maybe you should teach it to me?"
                                      .format(data['__version__'])
                                      )


def save_orbit_npy(filename, obj):
    VERSION = '1.0'
    data = {
        'BPMx': obj.BPMx,
        'BPMy': obj.BPMy,
        'CMx': obj.CMx,
        'CMy': obj.CMy,
        'names': obj.names,
        'sampling_frequency': obj.sampling_frequency,
        'data_structure': "array[item, time_sample]",
        'measure_date': obj.measure_date.strftime(DATETIME_ISO),
        '__version__': VERSION,
    }
    np.save(filename, [data])


def load_orbit_hdf5(filename):

    try:
        with h5py.File(filename, 'r') as f:
            if '__version__' in f.attrs and f.attrs['__version__'] == '1.0':
                try:
                    return OrbitData(
                        BPMx=f['data/BPMx'][:], BPMy=f['data/BPMy'][:],
                        CMx=f['data/CMx'][:], CMy=f['data/CMy'][:],
                        sampling_frequency=f['sampling_frequency'][()],
                        measure_date=(f.attrs['measure_date'], DATETIME_ISO),
                        names={'BPMx': f['names/BPMx'][:],
                               'BPMy': f['names/BPMy'][:],
                               'CMx': f['names/CMx'][:],
                               'CMy': f['names/CMy'][:],
                               },
                        )
                except:
                    raise
            else:
                raise NotImplementedError("The version {} is unknown to me, "
                                          "maybe you should teach it to me?"
                                          .format(f.attrs['__version__']))
    except Exception:
        raise


def save_orbit_hdf5(filename, obj):
    """ Save data to hdf5
    """
    VERSION = '1.0'

    if os.path.splitext(filename) != '.hdf5':
        filename += '.hdf5'
    
    if obj.names['BPMx'] is None:
        names_BPMx = []
        names_BPMy = []
        names_CMx = []
        names_CMy = []
    else:
        names_BPMx = obj.names['BPMx']
        names_BPMy = obj.names['BPMy']
        names_CMx = obj.names['CMx']
        names_CMy = obj.names['CMy']

    with h5py.File(filename, 'w') as f:
        f.create_dataset('data/BPMx', data=obj.BPMx)
        f.create_dataset('data/BPMy', data=obj.BPMy)
        f.create_dataset('data/CMx', data=obj.CMx)
        f.create_dataset('data/CMy', data=obj.CMy)
        f.create_dataset('sampling_frequency', data=obj.sampling_frequency)
        f.create_dataset('names/BPMx', data=names_BPMx)
        f.create_dataset('names/BPMy', data=names_BPMy)
        f.create_dataset('names/CMx', data=names_CMx)
        f.create_dataset('names/CMy', data=names_CMy)
        f.attrs['data_structure'] = "array[item, time_sample]"
        f.attrs['measure_date'] = obj.measure_date.strftime(DATETIME_ISO)
        f.attrs['creation_date'] = datetime.now().strftime(DATETIME_ISO)
        f.attrs['__version__'] = VERSION


def load_orbit_dump(filename):

    try:
        data = scipy.io.loadmat(filename)
    except:
        raise
    else:
        if '__version__' not in data:
            print("Unknown version, I might not understand your data.")

        if data['__version__'] == '1.0':
            pass
        else:
            raise NotImplementedError("The version {} is unknown to me, "
                                      "maybe you should teach it to me?"
                                      .format(data['__version__']))

        keys = ['difforbitX', 'difforbitY',
                'CMx', 'CMy',
                '__version__', '__header__',
                ]
        for key in keys:
            if key not in data:
                raise ValueError("Input file is not well formated, "
                                 "'{}' is key missing"
                                 .format(key))

        # data['header'] = 'MATLAB 5.0 MAT-file, Platform: GLNX86, Created on: Mon May 30 16:30:30 2016'
        loc = locale.getlocale()
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        creation_date = (data['__header__'].decode('utf8')
                                           .split('Created on: ')[1])
        creation_date = datetime.strptime(creation_date,
                                          '%a %b %d %H:%M:%S %Y')
        locale.setlocale(locale.LC_ALL, loc)

        _, sample_nb = data['difforbitX'].shape

        BPMx_nb, _ = data['difforbitX'][0, 0].shape
        BPMy_nb, _ = data['difforbitY'][0, 0].shape
        CMx_nb, _ = data['CMx'][0, 0].shape
        CMy_nb, _ = data['CMy'][0, 0].shape

        BPMx = np.zeros((BPMx_nb, sample_nb))
        BPMy = np.zeros((BPMy_nb, sample_nb))
        CMx = np.zeros((CMx_nb, sample_nb))
        CMy = np.zeros((CMy_nb, sample_nb))

        for i in range(sample_nb):
            BPMx[:, i] = data['difforbitX'][0, i][:, 0]
            BPMy[:, i] = data['difforbitY'][0, i][:, 0]
            CMx[:, i] = data['CMx'][0, i][:, 0]
            CMy[:, i] = data['CMy'][0, i][:, 0]

        orbit_data = OrbitData(
            BPMx=BPMx, BPMy=BPMy,
            CMx=CMx, CMy=CMy,
            sampling_frequency=150.,
            measure_date=creation_date
            )

        return orbit_data


def load_orbit_from_archiver(t_start, t_end):
    a = Archiver()

    BPMs_patt = "^BPMZ[1-7].*:rd[X|Y]$"
    CMx_patt = "^HS[1-4].*:rdbkSet$"
    CMy_patt = "^VS[1-3].*:rdbkSet$"
    patterns = "({})|({})|({})".format(BPMs_patt, CMx_patt, CMy_patt)
    data = a.read(patterns, t_start, t_end)

    if not data:
        raise RuntimeError("No data returned...I'm confused... "
                           "This is unexpected.")

    BPMx = []
    BPMy = []
    CMx = []
    CMy = []
    names = {'BPMx': [], 'BPMy': [], 'CMx': [], 'CMy': []}

    sample_number = int((t_end-t_start).total_seconds()/2)

    for key in data:
        d = []
        k = 0

        for j in range(sample_number):
            if (data[key]['time'][k] <= t_start + j*timedelta(seconds=2) and
                    k+1 < len(data[key]['time'])):
                k += 1
            d.append(data[key]['values'][k])

        if key[:2] == "HS":
            CMx.append(d)
            names['CMx'].append(key)
        elif key[:2] == "VS":
            CMy.append(d)
            names['CMy'].append(key)
        elif key[:3] == "BPM" and key[-1] == "X":
            BPMx.append(d)
            names['BPMx'].append(key)
        elif key[:3] == "BPM" and key[-1] == "Y":
            BPMy.append(d)
            names['BPMy'].append(key)
        else:
            raise RuntimeError("{} was not an expected name.".format(key))

    return OrbitData(
        BPMx=np.array(BPMx), BPMy=np.array(BPMy),
        CMx=np.array(CMx), CMy=np.array(CMy),
        names=names,
        sampling_frequency=0.5,
        measure_date=t_start
        )


class Archiver(object):
    url = "http://archiver.bessy.de/archive/cgi/CGIExport.cgi"

    def filter_camonitor(self, data):
        values = dict()

        datalist = data.decode('utf8').split('\t\n')

        # create dict of values/time
        for line in datalist[:-1]:
            # last element is empty
            l = line.split()
            key = l[0]
            value = float(l[3])
            t = datetime.strptime(' '.join(l[1:3]),
                                  "%Y-%m-%d %H:%M:%S.%f")

            if key not in values:
                values[key] = {'values': [], 'time': []}

            values[key]['values'].append(value)
            values[key]['time'].append(t)

        # Change the values in ndarray
        for key in values:
            values[key]['values'] = np.array(values[key]['values'])

        return values

    def read(self, var, t0, t1=None):

        if t1 is None:
            t1 = t0

        if type(t0) is not datetime \
                or type(t1) is not datetime:
            raise TypeError("2nd and 3rd arguments must be datetime.datetime"
                            "types")
        if t0 > t1:
            raise ValueError("End time must be greater than endtime.")

        now = datetime.now()
        if t1 > now:
            raise ValueError("End time must be in the past. "
                             "I'm not Marty, Doc..")

        same_week = now.isocalendar()[1] == t0.isocalendar()[1]

        if same_week:
            index = "/opt/Archive/current_week/index"
        else:
            index = "/opt/Archive/master_index"

        if type(var) is list:
            var = '\n'.join(var)
            type_var = 'NAMES'
        else:
            type_var = 'PATTERN'

        data_dict = {'INDEX': index,
                     'COMMAND': "camonitor",
                     'STRSTART': 1,
                     'STARTSTR': t0.strftime("%Y-%m-%d %H:%M:%S"),
                     'STREND': 1,
                     'ENDSTR': t1.strftime("%Y-%m-%d %H:%M:%S"),
                     type_var: var,
                     }

        data = urlencode(data_dict, encoding='utf8')
        full_url = self.url + '?' + data

        try:
            with urlopen(full_url) as response:
                return self.filter_camonitor(response.read())
        except Exception:
            raise


def load_Smat(filename):
    try:
        smat = scipy.io.loadmat(filename)
    except Exception:
        raise
    else:
        if 'Rmat' not in smat:
            raise ValueError("Cannot find Rmat structure. Check the file you "
                             "provided.")

        Smat_xx = smat['Rmat'][0, 0]['Data']
        Smat_yy = smat['Rmat'][1, 1]['Data']

        return Smat_xx, Smat_yy


if __name__ == "__main__":
    a = Archiver()
    t0 = datetime(2016, 5, 30, 16, 30, 29)
    t1 = t0 + timedelta(minutes=2)
    r = a.read(['BBQR:X:MAX1202:CH0', 'r1BBQR:X:MAX1202:CH1'], t0, t1)
    q = load_orbit_from_archiver(t0,t1)
