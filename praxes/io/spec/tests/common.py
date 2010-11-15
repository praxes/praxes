import os
import tempfile

from praxes import testing
from praxes.io import spec

class TestCase(testing.TestCase):

    file_name = None

    @classmethod
    def setUpClass(cls):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            cls.file_name = f.name
            f.file.write(cls.get_reference_data())

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.file_name):
            os.remove(cls.file_name)

    def setUp(self):
        self.f = spec.open(self.file_name)

    def tearDown(self):
        del(self.f)

    @classmethod
    def get_reference_data(cls):
        raise NotImplementedError
