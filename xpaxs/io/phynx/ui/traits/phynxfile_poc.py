
from xpaxs.io.phynx import File
from xpaxs.io.phynx.ui.traits.treeview import MainInterface


if __name__ == '__main__':
    file_interface = MainInterface()
    try:
        file_interface.open_file('../../tests/foo.h5', 'r')
    except:
        f=File('../../tests/foo.h5', 'w')
        e1=f.create_group('entry1')
        s1=e1.create_group('subentry1')
        s1.create_dataset('data1', shape=(10, ), dtype='f')
        e2=f.create_group('entry2')
        s2=e2.create_group('subentry2')
        s2.create_dataset('data2', shape=(10, ), dtype='f')
        f.flush()
        f.close()

        file_interface.open_file('../../tests/foo.h5', 'r')

    file_interface.configure_traits()
