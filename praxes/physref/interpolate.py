"""
"""

import numpy as np
from scipy import interpolate as _sp_interp


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
