
from __future__ import absolute_import, with_statement

from numpy import testing as npt
from .utils import TestCase
from ..exceptions import H5Error

class TestFile(TestCase):

    _ref_fname = 'citrus_leaves.dat.h5'

    def test_File_init_r(self):
        with self.get_file('r') as f:
            npt.assert_raises(H5Error, f.create_group, "foo")
            npt.assert_equal(f.mode, 'r')
            npt.assert_equal(f.filename, self.fname)
