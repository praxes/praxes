from __future__ import absolute_import, with_statement

from .common import TestCase, ut
from ..file import File, open


class TestFile(TestCase):

    def test_File_init_r(self):
        fname = self.f.file_name
        self.f.close()
        f = open(fname, 'r')
        self.assertEqual(f.mode, 'r')
        self.assertEqual(f.file_name, f._h5node.filename)
        self.assertRaises(Exception, f.create_group, 'foo')
        f.close()
        self.assertRaises(IOError, open, '.', 'r')

    def test_file_property(self):
        self.assertEqual(self.f, self.f.file)
        self.assertEqual(self.f.file, self.f['/'].file)

        self.f['foo'] = [1, 2]
        self.assert_(isinstance(self.f.file, File))
        self.assert_(isinstance(self.f['/'].file, File))
        self.assert_(isinstance(self.f['/foo'].file, File))

    def test_parent(self):
        self.assertEqual(self.f.parent, self.f['/'])

    def test_path(self):
        self.assertEqual(self.f.path, '/')
        self.assertEqual(self.f.name, '/')
        self.assertEqual(self.f.id, '/')

    def test_close(self):
        f = self.mktemp()
        f.close()
        self.assertRaises(ValueError, f.values)
