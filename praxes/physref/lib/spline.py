import numpy as np


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
