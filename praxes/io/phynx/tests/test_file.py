from __future__ import absolute_import, with_statement

import os
import shutil
import tempfile
import time
import warnings
warnings.filterwarnings("ignore")

from .common import TestCase, ut
from ..file import File, open
from ..registry import registry

import numpy as np
from ..file import open


class TestFile(TestCase):

    def mktemp(self, mode='a'):
        dir = self.tempdir
        fname = tempfile.mktemp(suffix='.h5', dir=self.tempdir)
        path = os.path.split(__file__)[0]
        shutil.copy(os.path.join(path, 'citrus_leaves.dat.h5'), fname)
        return open(fname, mode=mode)

    def test_File_init_r(self):
        f = self.mktemp('r')
        self.assertRaises(IOError, f.create_group, 'foo')
        self.assertEqual(f.mode, 'r')
        self.assertEqual(f.file_name, f._h5node.filename)

        self.assertRaises(IOError, open, '.', 'r')

    def test_file_property(self):
        f = self.mktemp()
        self.assertEqual(f, f.file)
        self.assertEqual(f.file, f['/'].file)

        f['foo'] = [1, 2]
        self.assert_(isinstance(f.file, File))
        self.assert_(isinstance(f['/'].file, File))
        self.assert_(isinstance(f['/foo'].file, File))
