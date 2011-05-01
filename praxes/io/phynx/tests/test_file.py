from __future__ import absolute_import, with_statement

from .common import TestCase, ut
from ..file import File


class TestFile(TestCase):

    def test_File_init_r(self):
        f = self.getfile('citrus_leaves.dat.h5', mode='r')
        self.assertEqual(f.mode, 'r')
        self.assertEqual(f.file_name, f._h5node.filename)
        self.assertRaises(Exception, f.create_group, 'foo')

        self.assertRaises(IOError, open, '.', 'r')

    def test_file_property(self):
        f = self.mktemp()
        self.assertEqual(f, f.file)
        self.assertEqual(f.file, f['/'].file)

        f['foo'] = [1, 2]
        self.assert_(isinstance(f.file, File))
        self.assert_(isinstance(f['/'].file, File))
        self.assert_(isinstance(f['/foo'].file, File))

    def test_parent(self):
        f = self.mktemp()
        self.assertEqual(f.parent, f['/'])

    def test_path(self):
        f = self.mktemp()
        self.assertEqual(f.path, '/')
        self.assertEqual(f.name, '/')
        self.assertEqual(f.id, '/')

    def test_close(self):
        f = self.mktemp()
        f.close()
        self.assertRaises(ValueError, f.values)
