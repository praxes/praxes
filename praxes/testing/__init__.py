import unittest2

import numpy as np


class TestCase(unittest2.TestCase):

    def assertArrayEqual(self, a1, a2, msg=None, delta=None):
        """ Make sure dset and arr have the same shape, dtype and contents, to
            within the given precision.

            Note that dset may be a NumPy array or an HDF5 dataset.
        """
        if delta is None:
            delta = 1e-5
        if msg is None:
            msg = ''
        else:
            msg = ' (%s)' % msg
        a1 = np.asanyarray(a1)
        a2 = np.asanyarray(a2)

        if a1.shape != a2.shape:
            raise self.failureException(
                "Shape mismatch (%s vs %s)%s" % (a1.shape, a2.shape, msg)
                )
        if not np.all(np.abs(a1 - a2) < delta):
            raise self.failureException(
                "Arrays differ by more than %g%s" % (delta, msg)
                )
