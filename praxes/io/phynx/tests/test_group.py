from __future__ import absolute_import, with_statement

from .common import TestCase, ut
from ..registry import registry


class TestGroup(TestCase):

    def test_getitem(self):
        f = self.mktemp()
        a = f.create_group('a', 'Entry')
        self.assertEqual(a, f['a'])
        self.assertTrue(isinstance(f['a'], registry['Entry']))

    def test_get(self):
        f = self.mktemp()
        a = f.create_group('a')
        self.assertEqual(f.get('a'), a)
        self.assertEqual(f.get('b'), None)
        self.assertEqual(f.get('b', 'c'), 'c')

    def test_sorted(self):
        f = self.mktemp()
        a = f.create_group('c')
        b = f.create_group('b')
        c = f.create_group('a')
        self.assertEqual(f.values(), [c, b, a])
        self.assertEqual(f.keys(), ['a', 'b', 'c'])
        self.assertEqual(f.items(), [('a', c), ('b', b), ('c', a)])

    def test_contains(self):
        f = self.mktemp()
        a = f.create_group('a')
        self.assertTrue('a' in f)
        self.assertFalse('z' in f)

    def test_entry(self):
        f = self.mktemp()
        a = f.create_group('a', 'Entry')
        b = a.create_group('b')
        self.assertEqual(f.entry, None)
        self.assertEqual(a, a.entry)
        self.assertEqual(a, b.entry)

