import os
import tempfile
import unittest2

from praxes.testing import TestCase
from praxes.io import spec

class TestSequenceFunctions(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.seq = (
            "#F testfile.dat\n",
            "\n",
            )
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            cls.filename = f.name
            f.file.writelines(cls.seq)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.filename):
            os.remove(cls.filename)

    def test_open(self):
        # make sure the shuffled sequence does not lose any elements
        with spec.open(self.filename) as f:
            self.assertEqual(tuple(f.readlines()), self.seq)
            self.assertRaises(IOError, f.write, 'an additional line')

    def test_array(self):
        self.assertArrayEqual(1, 1.0)

#    def test_choice(self):
#        element = random.choice(self.seq)
#        self.assertTrue(element in self.seq)

#    def test_sample(self):
#        with self.assertRaises(ValueError):
#            random.sample(self.seq, 20)
#        for element in random.sample(self.seq, 5):
#            self.assertTrue(element in self.seq)
