import os
import sys
import tarfile

import numpy as np
import h5py

def process_waasmaierdb(data, root):
    if os.path.isfile(os.path.join(root, 'waasmaierdb.h5')):
        return

    try:
        archive = tarfile.open(data)
        lines = archive.extractfile(archive.getnames()[0]).readlines()[19:]
    finally:
        archive.close()

    with h5py.File(os.path.join(root, 'waasmaierdb.h5'), 'w') as elements:
        while 1:
            id = lines.pop(0).split()[0]
            if id == 'END':
                break

            el = elements.create_group(id)

            line = lines.pop(0)
            el['a'] = np.zeros(5, dtype='d')
            for i in range(5):
                el['a'][i], line = np.float64(line[:10]), line[10:]
            el['c'] = np.float64(line[:10])

            line = lines.pop(0)
            el['b'] = np.zeros(5, dtype='d')
            for i in range(5):
                el['b'][i], line = np.float64(line[:10]), line[10:]

            line = lines.pop(0) # skip empty line


if __name__ == '__main__':
    process_waasmaierdb(*sys.argv[1:])
