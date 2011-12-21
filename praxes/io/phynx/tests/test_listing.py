from .common import TestCase, ut


class TestSorting(TestCase):

    def test_defaults(self):
        a = self.f.create_group('a')
        b = self.f.create_group('b')
        c = self.f.create_group('c')
        self.assertEqual(sorted(self.f.keys()), ['a', 'b', 'c'])
        self.assertEqual(sorted(self.f.values()), [a, b, c])
        self.assertEqual(sorted(self.f.items()), [('a', a), ('b', b), ('c', c)])

    def test_sequential_name(self):
        a = self.f.create_group('a')
        b = self.f.create_group('b')
        c = self.f.create_group('c')
        self.assertEqual(list(self.f.values()), [a, b, c])

    def test_default_start_time(self):
        a = self.f.create_group('c', 'Entry')
        a.attrs['start_time'] = 1
        b = self.f.create_group('b', 'Entry')
        b.attrs['start_time'] = 2
        self.assert_(a < b)
        c = self.f.create_group('a', 'Entry')
        c.attrs['start_time'] = 0
        self.assert_(c < a)
        self.assertEqual(list(self.f.values()), [c, a, b])

    def test_entry_id(self):
        a = self.f.create_group('1', 'Entry')
        b = self.f.create_group('2', 'Entry')
        self.assertTrue(a < b)
        c = self.f.create_group('15', 'Entry')
        self.assert_(b < c)
        d = self.f.create_group('1.1', 'Entry')
        self.assertTrue(a < d and d < b and d < c)
        self.assertEqual(list(self.f.values()), [a, d, b, c])
