
from __future__ import absolute_import, with_statement

import posixpath
import time

from numpy import testing as npt
from .utils import TestCase
from ..exceptions import H5Error
from .. import sorting

class TestSorting(TestCase):

    def test_defaults(self):
        with self.get_file() as f:
            a=f.create_group('a')
            b=f.create_group('b')
            c=f.create_group('c')
            npt.assert_array_equal(f.keys(), ['a', 'b', 'c'])
            npt.assert_array_equal(f.values(), [a, b, c])
            npt.assert_array_equal(f.items(), [('a', a), ('b', b), ('c', c)])
            npt.assert_array_equal(f.listnames(), ['a', 'b', 'c'])
            npt.assert_array_equal(f.listobjects(), [a, b, c])
            npt.assert_array_equal(f.listitems(), [('a', a), ('b', b), ('c', c)])

    def test_sequential_name(self):
        with self.get_file() as f:
            f.sorted_with(sorting.sequential)

            f.create_group('a')
            f.create_group('b')
            f.create_group('c')
            npt.assert_equal(f.keys(), ['a', 'b', 'c'])

    def test_default_start_time(self):
        with self.get_file() as f:
            a = f.create_group('c')
            a.attrs['start_time'] = time.time()
            time.sleep(.01)

            b = f.create_group('b')
            b.attrs['start_time'] = time.time()
            time.sleep(.01)

            c = f.create_group('a')
            c.attrs['start_time'] = time.time()

            npt.assert_equal(f.keys(), ['a', 'b', 'c'])

    def test_sequential_start_time(self):
        with self.get_file() as f:
            f.sorted_with(sorting.sequential)

            a = f.create_group('c')
            a.attrs['start_time'] = time.time()
            time.sleep(.01)

            b = f.create_group('b')
            b.attrs['start_time'] = time.time()
            time.sleep(.01)

            c = f.create_group('a')
            c.attrs['start_time'] = time.time()

            npt.assert_equal(f.keys(), ['c', 'b', 'a'])
            npt.assert_array_equal(f.values(), [c, b, a])
            npt.assert_array_equal(f.items(), [('c', c), ('b', b), ('a', a)])
            npt.assert_array_equal(f.listnames(), ['c', 'b', 'a'])
            npt.assert_array_equal(f.listobjects(), [c, b, a])
            npt.assert_array_equal(f.listitems(), [('c', c), ('b', b), ('a', a)])
