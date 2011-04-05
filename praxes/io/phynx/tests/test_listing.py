
from __future__ import absolute_import, with_statement

from .common import TestCase, ut


class TestSorting(TestCase):

    def test_defaults(self):
        f = self.mktemp()
        a = f.create_group('a')
        b = f.create_group('b')
        c = f.create_group('c')
        self.assertItemsEqual(f.keys(), ['a', 'b', 'c'])
        self.assertItemsEqual(f.values(), [a, b, c])
        self.assertItemsEqual(f.items(), [('a', a), ('b', b), ('c', c)])

    def test_sequential_name(self):
        f = self.mktemp()
        a = f.create_group('a')
        b = f.create_group('b')
        c = f.create_group('c')
        self.assertEqual(f.values(), [a, b, c])

    def test_default_start_time(self):
        f = self.mktemp()
        a = f.create_group('c', 'Entry')
        a.attrs['start_time'] = 1
        b = f.create_group('b', 'Entry')
        b.attrs['start_time'] = 2
        self.assert_(a < b)
        c = f.create_group('a', 'Entry')
        c.attrs['start_time'] = 0
        self.assert_(c < a)
        self.assertEqual(f.values(), [c, a, b])
