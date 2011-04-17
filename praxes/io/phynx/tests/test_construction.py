from __future__ import absolute_import, with_statement

import time
import warnings
warnings.filterwarnings("ignore")

from .common import TestCase, ut
from ..file import open
from ..registry import registry

import numpy as np


class TestConstruction(TestCase):

    def test_unrecognized_class(self):
        f = self.mktemp()
        a = f.create_group('a')
        a.attrs['class'] = 'Foo'
        self.assert_(isinstance(f['a'], registry['Group']))

    def test_unrecognized_nxclass(self):
        f = self.mktemp()
        a = f._h5node.create_group('a')
        a.attrs['nx_class'] = 'Foo'
        self.assert_(isinstance(f['a'], registry['Group']))

    def test_class_attribute_array(self):
        f = self.mktemp()
        a = f.create_group('a')
        a.attrs['class'] = np.array(['Foo'])
        self.assert_(isinstance(f['a'], registry['Group']))

    def test_class_attribute_respected(self):
        f = self.mktemp()
        a = f.create_group('a')
        a.attrs['class'] = 'Measurement'
        self.assert_(isinstance(f['a'], registry['Measurement']))

    def test_class_attribute_saved(self):
        f = self.mktemp()
        a = f.create_group('a', type='Entry')
        self.assert_(isinstance(f['a'], registry['Entry']))

    def test_use_nxclass(self):
        f = self.mktemp()
        a = f.create_group('a', type='Entry')
        del a.attrs['class']
        self.assert_(isinstance(f['a'], registry['Entry']))

    def test_use_default_interface(self):
        f = self.mktemp()
        a = f.create_group('a', type='Entry')
        del a.attrs['class']
        del a.attrs['NX_class']
        self.assert_(not isinstance(f['a'], registry['Entry']))
        self.assert_(isinstance(f['a'], registry['Group']))
