"""
"""

import numpy as np
from scipy import interpolate as _sp_interp


def splint(xa, ya, y2a, x):
    '''spline interpolation'''
    try:
        len(x)
    except TypeError:
        x = np.array([x])

    try:
        klo, khi = np.array([
            (np.flatnonzero(xa < i)[-1], np.flatnonzero(xa > i)[0])
            for i in x
            ]).transpose()
    except IndexError:
        raise ValueError(
            'Input values must be between %s and %s'
            % (np.exp(xa[0]), np.exp(xa[-1]))
            )

    h = xa[khi] - xa[klo]
    if any(h <= 0):
        raise ValueError, 'xa input must be strictly increasing'
    a = (xa[khi] - x) / h
    b = (x - xa[klo]) / h

    res = (
        a * ya[klo]
        + b * ya[khi]
        + ((a**3 - a) * y2a[klo] + (b**3 - b) * y2a[khi]) * (h**2) / 6
        )
    return res

def interpolate(x, ref_x, ref_y):
    try:
        shape = x.shape
        x = x.flat
    except:
        x = np.array([x],'f')
        shape = x.shape
    # mask values that can not be calculated by interpolation:
    checkrange = ((x < ref_x[0]) | (x > ref_x[-1]))
    x = np.where(checkrange, np.nan, x)
    return _sp_interp.interp1d(ref_x, ref_y)(x).reshape(shape)
