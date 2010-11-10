from .common import TestCase


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

    @classmethod
    def get_reference_data(cls):
        return reference_data

    def test_0_open(self):
        "test file contents are identical to the original data"
        with self.f.file as f:
            self.assertEqual(f.read(), reference_data)
            self.assertRaises(IOError, f.write, 'an additional line')

        self.assertEqual(self.f.name, self.file_name)

    def test_len(self):
        "test that the file length is equal to the number of scans"
        self.assertEqual(len(self.f), reference_data.count('#S'))

    def test_getitem(self):
        self.assertEqual(self.f['1'].name, '1')

    def test_iter(self):
        self.assertEqual([id for id in self.f][0], '1')

    def test_keys(self):
        self.assertEqual(self.f.keys()[0], '1')

    def test_items(self):
        self.assertEqual([id for (id, index) in self.f.items()][0], '1')

    def test_values(self):
        self.assertEqual([index.name for index in self.f.values()][0], '1')

    def test_iterkeys(self):
        self.assertEqual([i for i in self.f.iterkeys()][0], '1')

    def test_iteritems(self):
        self.assertEqual([id for (id, index) in self.f.iteritems()][0], '1')

    def test_itervalues(self):
        self.assertEqual(
            [index.name for index in self.f.itervalues()][0], '1'
            )

    def test_update(self):
        with open(self.file_name, 'r+') as f:
            f.seek(0,2)
            f.write('\n'.join(reference_data.split('\n')[5:]))
        self.f.update()
        self.assertEqual(self.f.keys()[1], '1.2')
