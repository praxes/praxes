"""
"""

from __future__ import absolute_import, with_statement

import os
import posixpath
import shutil
import tempfile

from ..file import File


class TestCase(object):

    _ref_fname = None

    @property
    def file(self):
        return self.get_file()

    @property
    def fname(self):
        return self._fname

    @property
    def ref_fname(self):
        if self._ref_fname is None:
            return
        return '/'.join([posixpath.split(__file__)[0], self._ref_fname])

    def get_file(self, mode='a', lock=None):
        return File(self.fname, mode, lock)

    def setUp(self):
        self._fname = tempfile.mktemp('.hdf5')
        if self.ref_fname is not None:
            shutil.copy(self.ref_fname, self._fname)

    def tearDown(self):
        os.unlink(self.fname)
