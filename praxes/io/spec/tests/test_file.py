import os
import tempfile
import unittest2

from praxes.testing import TestCase
from praxes.io import spec


reference_data = \
"""#F testfile.dat
#E 1000
#D Sat Jan 1 00:00:00 2010
#C spec  User = specuser
#O0     samx      samy      samz

#S 1  dscan  samx -1 1 2 1
#D Sat Jan 1 00:01:00 2010
#M 1000  (I0)
#G0 0
#G1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#G3 0 0 0 0 0 0 0 0 0
#G4 0
#Q
#P0 0 10 -10
#U Saving mca spectra for each scan pt
#@vortex %25C
#@CHANN 30 0 29 1
#@CALIB 0 0.01 0
#N 4
#L samx  Epoch  I0  I1
-1 100 1000 100
@vortex 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
0 200 1000 200
@vortex 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
1 300 1000 300
@vortex 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
"""


class TestSpecFileInterface(TestCase):

    file_name = None

    @classmethod
    def setUpClass(cls):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            cls.file_name = f.name
            f.file.write(reference_data)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.file_name):
            os.remove(cls.file_name)

    def test_builtin_open(self):
        "test file contents are identical to the original data"
        with open(self.file_name) as f:
            self.assertEqual(f.read(), reference_data)
            self.assertRaises(IOError, f.write, 'an additional line')

    def test_spec_open(self):
        f = spec.open(self.file_name).file
        self.assertEqual(f.read(), reference_data)
        self.assertRaises(IOError, f.write, 'an additional line')

        f = spec.open(self.file_name)
        self.assertEqual(f.name, self.file_name)