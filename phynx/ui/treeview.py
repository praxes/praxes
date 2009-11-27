from __future__ import absolute_import

from enthought.traits.api import HasTraits, Instance, List, Str
from enthought.traits.ui.api import Item, View, TreeEditor, TreeNode

# TODO: when registering classes, they should also register TreeNodes
# then these imports are unnecessary:
from ...file import File
from ...group import Group
from ...dataset import Dataset

class File_List(HasTraits):
    name = Str
    files = List(File)

    def append(self, h5file):
        self.files.append(h5file)

no_view=View()

main_tree_editor = TreeEditor(
    nodes=[
        TreeNode(node_for=[File_List],
                 children ='files',
                 label='name',
                 view = no_view,
                 ),
        TreeNode(node_for=[File],
                 children ='children',
                 label='filename',
                 view = View(['name']),
                 ),
        TreeNode(node_for=[Group],
                 children='children',
                 label='name',
                 view = View(['name']),
                 ),
        TreeNode(node_for = [Dataset],
                 label = 'name',
                 view=View(['name', 'shape'])),
        ])


class MainInterface(HasTraits):
    name = Str('Phynx Interface')
    file_list = File_List(name='File List')

    view = View(
        Item( name = 'file_list',
              editor = main_tree_editor,
              show_label = False
              ),
        title = 'HDF5 File Structure',
        buttons = ['OK'],
        resizable = True,
        style='custom',
        width = .3,
        height = .3
        )

    def open_file(self, name, mode = 'a'):
        self.file_list.append(File(name, mode))
