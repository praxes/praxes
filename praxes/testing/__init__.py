import unittest

import numpy as np


class TestCase(unittest.TestCase):

    def assertArrayEqual(self, a1, a2, msg=None, delta=None):
        """
        Make sure a1 and a2 have the same shape and contents to within the
        given precision.
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
