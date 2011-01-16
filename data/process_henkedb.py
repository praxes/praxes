import os
import sys
import tarfile

import numpy as np
import h5py


def process_henkedb(data, root):
    if os.path.isfile(os.path.join(root, 'henkedb.h5')):
        return

    try:
        archive = tarfile.open(data)
        members = archive.getnames()
        members.remove('read.me')

        with h5py.File(os.path.join(root, 'henkedb.h5'), 'w') as elements:
            for member in members:
                el = elements.create_group(member.split('.')[0].capitalize())
                filedata = archive.extractfile(member)
                filedata.readline() # skip the header
                data = np.array(
                    [map(np.float64, line.split()) for line in filedata]
                    )
                el['energy'] = data[:,0]
                el['energy'].attrs['units'] = 'eV'
                el['f1'] = data[:,1]
                el['f2'] = data[:,2]
    finally:
        archive.close()


if __name__ == '__main__':
    process_henkedb(*sys.argv[1:])
