from __future__ import absolute_import, with_statement

import numpy as np

from .common import TestCase, ut
from ..registry import registry


class TestDataset(TestCase):

    def test_create(self):
        f = self.mktemp()
        f['foo'] = [0,1,2,3]
        self.assertArrayEqual(f['foo'], np.array([0,1,2,3]))
        f.create_dataset('bar', data=np.array([1,2,3]), type='Axis')
        self.assertArrayEqual(f['bar'], np.array([1,2,3]))
        self.assertTrue(isinstance(f['bar'], registry['Axis']))
        f.create_dataset('baz', shape=[2,2], dtype='f')
        self.assertArrayEqual(f['baz'], np.array([[0,0],[0,0]], 'f'))
