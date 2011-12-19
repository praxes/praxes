import os
import shutil
import sys
import tempfile

if sys.version_info[:2] == (2,7) or sys.version_info[:2] >= (3,2):
    import unittest as ut
else:
    import unittest2 as ut

import numpy as np

from ..file import open


class TestCase(ut.TestCase):

    def setUp(self):
        self.f = self.mktemp(mode='w')

    def tearDown(self):
        if self.f:
            self.f.close()

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp(prefix='phynx-test_')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def getfile(self, filename, mode='a'):
        dir = self.tempdir
        fname = tempfile.mktemp(suffix='.h5', dir=self.tempdir)
        path = os.path.split(__file__)[0]
        shutil.copy(os.path.join(path, filename), fname)
        return open(fname, mode=mode)

    def mktemp(self, mode='a', suffix='.h5', prefix='', dir=None):
        if dir is None:
            dir = self.tempdir
        return open(tempfile.mktemp(suffix, prefix, dir=self.tempdir), mode)

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
