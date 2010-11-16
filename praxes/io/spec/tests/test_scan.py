import operator as op

import numpy as np

from .common import TestCase


reference_data = \
"""#F testfile.dat
#E 1000
#D Sat Jan 1 00:00:00 2010
#C spec  User = specuser
#O0     samx      samy      samz
#O1 detx  det y  det_z

#S 1  dscan  samx -1 1 2 1
#D Sat Jan 1 00:01:00 2010
#M 1000  (I0)
#G0 0
#G1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#G3 0 0 0 0 0 0 0 0 0
#G4 0
#Q
#P0 0 10 -10
#P1 1 2 3
#C A gratuitous comment
#U A user comment
#@vortex %25C
#@CHANN 30 0 29 1
#@CALIB 0 0.01 0
#N 4
#L samx  Epoch  I0  I1
-1 100 1000 100
@vortex 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
0 200 1000 200
@vortex 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
1 300 1000 300
@vortex 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0
"""


class TestSpecScanInterface(TestCase):

    @classmethod
    def get_reference_data(cls):
        return reference_data

    def test_0_open(self):
        "test file contents are identical to the original data"
        with open(self.f.name) as f:
            self.assertEqual(f.read(), reference_data)
            self.assertRaises(IOError, f.write, 'an additional line')

        self.assertEqual(self.f.name, self.file_name)

    def test_command(self):
        self.assertEqual(self.f['1'].attrs['command'], 'dscan samx -1 1 2 1')

    def test_comments(self):
        self.assertEqual(self.f['1'].attrs['comments'], ['A gratuitous comment'])

    def test_date(self):
        self.assertEqual(self.f['1'].attrs['date'], 'Sat Jan 1 00:01:00 2010')

    def test_duration(self):
        self.assertEqual(self.f['1'].attrs['duration'], ('I0', 1000))

    def test_epoch_offset(self):
        self.assertEqual(self.f['1'].attrs['epoch_offset'], 1000)

    def test_get_item(self):
        self.assertEqual(self.f['1']['samx'][0], -1)
        self.assertArrayEqual(self.f['1']['samx'][:], np.array([-1, 0, 1]))
        self.assertArrayEqual(
            self.f['1']['samx'][...],
            np.array([-1, 0, 1])
            )
        self.assertArrayEqual(
            self.f['1']['samx'][:2],
            np.array([-1, 0])
            )
        self.assertArrayEqual(
            self.f['1']['samx'][1:],
            np.array([0, 1])
            )
        self.assertArrayEqual(
            self.f['1']['samx'][1:2],
            np.array([0])
            )
        self.assertArrayEqual(
            self.f['1']['samx'][[0, 1, 2]],
            np.array([-1, 0, 1])
            )
        self.assertArrayEqual(
            self.f['1']['Epoch'][...],
            np.array([100, 200, 300])
            )
        self.assertArrayEqual(
            self.f['1']['I0'][...],
            np.array([1000, 1000, 1000])
            )
        self.assertArrayEqual(
            self.f['1']['I1'][...],
            np.array([100, 200, 300])
            )

    def test_iter_item(self):
        self.assertEqual([i for i in self.f['1']['samx']], [-1, 0, 1])

    def test_labels(self):
        self.assertEqual(
            self.f['1'].attrs['labels'],
            ['samx', 'Epoch', 'I0', 'I1']
            )

    def test_len(self):
        "test that the scan length is equal to the number of entries"
        self.assertEqual(len(self.f['1']), 5)

    def test_mcas(self):
        self.assertArrayEqual(
            self.f['1']['@vortex'][0],
            np.array([1]+[0]*29)
            )
        self.assertArrayEqual(
            self.f['1']['@vortex'][1],
            np.array([2]+[0]*29)
            )
        self.assertArrayEqual(
            self.f['1']['@vortex'][:],
            np.array([[1]+[0]*29, [2]+[0]*29, [3]+[0]*29])
            )
        self.assertArrayEqual(
            self.f['1']['@vortex'][...],
            np.array([[1]+[0]*29, [2]+[0]*29, [3]+[0]*29])
            )
        self.assertArrayEqual(
            self.f['1']['@vortex'][[0,1,2]],
            np.array([[1]+[0]*29, [2]+[0]*29, [3]+[0]*29])
            )
        self.assertArrayEqual(
            self.f['1']['@vortex'][0:3, :15],
            np.array([[1]+[0]*14, [2]+[0]*14, [3]+[0]*14])
            )
        self.assertEqual(self.f['1']['@vortex'][0, 0], 1)
        self.assertRaises(IndexError, op.getitem, self.f['1']['@vortex'], 3)
        self.assertRaises(
            IndexError, op.getitem, self.f['1']['@vortex'], (2, 35)
            )
        self.assertRaises(
            IndexError, op.getitem, self.f['1']['@vortex'], slice(0, 10)
            )
        self.assertRaises(
            IndexError, op.getitem, self.f['1']['@vortex'], (0, slice(50))
            )
        self.assertRaises(
            IndexError, op.getitem, self.f['1']['@vortex'], (slice(0, 10), 0)
            )

    def test_monitor(self):
        self.assertEqual(self.f['1'].attrs['monitor'], 'I0')

    def test_positions(self):
        self.assertEqual(
            self.f['1'].attrs['positions'],
            {'samx': 0, 'samy': 10, 'samz': -10,
             'detx': 1, 'det y': 2, 'det_z': 3}
            )

    def test_program(self):
        self.assertEqual(self.f['1'].attrs['program'], 'spec')

    def test_update(self):
        with open(self.file_name, 'r+') as f:
            f.seek(0,2)
            f.write('\n'.join(reference_data.split('\n')[5:]))
        self.f.update()
        self.assertEqual(len(self.f['1.2']), 5)

    def test_user(self):
        self.assertEqual(self.f['1'].attrs['user'], 'specuser')

    def test_user_comments(self):
        self.assertEqual(self.f['1'].attrs['user_comments'], ['A user comment'])
