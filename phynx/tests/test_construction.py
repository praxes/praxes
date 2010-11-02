
from __future__ import absolute_import, with_statement

import posixpath
import time

import numpy as np
from numpy import testing as npt
from .utils import TestCase
from ..exceptions import H5Error
from .. import sorting

import phynx

class TestSorting(TestCase):

    def test_unrecognized_class(self):
        with self.file as f:
            a = f.create_group('a')
            a.attrs['class'] = np.array('Foo')
            assert isinstance(f['a'], phynx.Group)

    def test_unrecognized_nxclass(self):
        with self.file as f:
            a = f.create_group('a')
            a.attrs['nx_class'] = np.array('Foo')
            assert isinstance(f['a'], phynx.Group)

    def test_class_attribute_array(self):
        with self.file as f:
            a = f.create_group('a')
            a.attrs['class'] = np.array(['Foo'])
            assert isinstance(f['a'], phynx.Group)

    def test_class_attribute_respected(self):
        with self.file as f:
            a = f.create_group('a')
            a.attrs['class'] = 'Measurement'
            assert isinstance(f['a'], phynx.Measurement)

    def test_class_attribute_saved(self):
        with self.file as f:
            a = f.create_group('a', type='Entry')
            assert isinstance(f['a'], phynx.Entry)

    def test_use_nxclass(self):
        with self.file as f:
            a = f.create_group('a', type='Entry')
            del a.attrs['class']
            assert isinstance(f['a'], phynx.Entry)

    def test_use_default_interface(self):
        with self.file as f:
            a = f.create_group('a', type='Entry')
            del a.attrs['class']
            del a.attrs['NX_class']
            assert not isinstance(f['a'], phynx.Entry)
            assert isinstance(f['a'], phynx.Group)
