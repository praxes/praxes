from __future__ import absolute_import, with_statement

import numpy as np

from .common import TestCase, ut
from ..registry import registry


class TestDataset(TestCase):

    def test_create(self):
        self.f['foo'] = [0,1,2,3]
        self.assertArrayEqual(self.f['foo'], np.array([0,1,2,3]))
        self.f.create_dataset('bar', data=np.array([1,2,3]), type='Axis')
        self.assertArrayEqual(self.f['bar'], np.array([1,2,3]))
        self.assertTrue(isinstance(self.f['bar'], registry['Axis']))
        self.f.create_dataset('baz', shape=[2,2], dtype='f')
        self.assertArrayEqual(self.f['baz'], np.array([[0,0],[0,0]], 'f'))
