import time
import warnings
warnings.filterwarnings("ignore")

from .common import TestCase, ut
from ..file import open
from ..registry import registry

import numpy as np


class TestConstruction(TestCase):

    def test_unrecognized_class(self):
        a = self.f.create_group('a')
        a.attrs['class'] = 'Foo'
        self.assert_(isinstance(self.f['a'], registry['Group']))

    def test_unrecognized_nxclass(self):
        a = self.f._h5node.create_group('a')
        a.attrs['nx_class'] = 'Foo'
        self.assert_(isinstance(self.f['a'], registry['Group']))

    @ut.expectedFailure
    def test_class_attribute_array(self):
        a = self.f.create_group('a')
        a.attrs['class'] = np.array(['Foo'])
        self.assert_(isinstance(self.f['a'], registry['Group']))

    def test_class_attribute_respected(self):
        a = self.f.create_group('a')
        a.attrs['class'] = 'Measurement'
        self.assert_(isinstance(self.f['a'], registry['Measurement']))

    def test_class_attribute_saved(self):
        a = self.f.create_group('a', type='Entry')
        self.assert_(isinstance(self.f['a'], registry['Entry']))

    def test_use_nxclass(self):
        a = self.f.create_group('a', type='Entry')
        del a.attrs['class']
        self.assert_(isinstance(self.f['a'], registry['Entry']))

    def test_use_default_interface(self):
        a = self.f.create_group('a', type='Entry')
        del a.attrs['class']
        del a.attrs['NX_class']
        self.assert_(not isinstance(self.f['a'], registry['Entry']))
        self.assert_(isinstance(self.f['a'], registry['Group']))
