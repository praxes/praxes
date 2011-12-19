from __future__ import absolute_import, with_statement

from .common import TestCase, ut
from ..registry import registry


class TestGroup(TestCase):

    def test_getitem(self):
        a = self.f.create_group('a', 'Entry')
        self.assertEqual(a, self.f['a'])
        self.assertTrue(isinstance(self.f['a'], registry['Entry']))

    def test_get(self):
        a = self.f.create_group('a')
        self.assertEqual(self.f.get('a'), a)
        self.assertEqual(self.f.get('b'), None)
        self.assertEqual(self.f.get('b', 'c'), 'c')

    def test_sorted(self):
        a = self.f.create_group('c')
        b = self.f.create_group('b')
        c = self.f.create_group('a')
        self.assertEqual(self.f.values(), [c, b, a])
        self.assertEqual(self.f.keys(), ['a', 'b', 'c'])
        self.assertEqual(self.f.items(), [('a', c), ('b', b), ('c', a)])

    def test_contains(self):
        a = self.f.create_group('a')
        self.assertTrue('a' in self.f)
        self.assertFalse('z' in self.f)

    def test_entry(self):
        a = self.f.create_group('a', 'Entry')
        b = a.create_group('b')
        self.assertEqual(self.f.entry, None)
        self.assertEqual(a, a.entry)
        self.assertEqual(a, b.entry)
