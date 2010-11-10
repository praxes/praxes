from copy import copy

# this could be a subclass of ordered dict, requiring python-2.7:
class FileIndex(object):

    def __init__(self, file_name):
        self._file_name = file_name
        self._bytes_read = 0
        # would be nice to use python-2.7's ordered dict:
        self._id_list = []
        self._scan_dict = {}

        self.update()

    def __getitem__(self, id):
        return self._scan_dict[id]

    def __len__(self):
        return len(self._id_list)

    def __iter__(self):
        return iter(self._id_list)

    def iteritems(self):
        def g(file_index):
            for id in file_index._id_list:
                yield (id, file_index._scan_dict[id])
        return g(self)

    def iterkeys(self):
        return iter(self._id_list)

    def itervalues(self):
        def g(file_index):
            for id in file_index._id_list:
                yield file_index._scan_dict[id]
        return g(self)

    def items(self):
        return [(id, self._scan_dict[id]) for id in self._id_list]

    def keys(self):
        return copy(self._id_list)

    def update(self):
        # go to last line read, and continue
        # if additional lines have been added to the previous scan since
        # the last read, need to mark the scan index as dirty so it
        # knows to refresh
        with open(self._file_name, 'r+b') as f:
            f.seek(self._bytes_read)
            file_offset = f.tell()
            for line in f:
                if line[:2] == '#S':
                    scan_name = scan_id = line.split()[1]
                    dup = 1
                    while scan_id in self._scan_dict:
                        dup += 1
                        scan_id = '%d.%d' % (scan_name, dup)
                    scan_index = ScanIndex(
                        scan_name,
                        scan_id,
                        self._file_name,
                        file_offset
                        )
                    self._scan_dict[scan_id] = scan_index
                    self._id_list.append(scan_id)
                file_offset += len(line)
            self._bytes_read = file_offset

    def values(self):
        return [self._scan_dict[i] for i in self._id_list]


class ScanIndex(object):

    @property
    def name(self):
        return self._scan_name

    @property
    def id(self):
        return self._scan_id

    def __init__(self, scan_name, scan_id, file_name, file_offset):
        self._scan_name = scan_name
        self._scan_id = scan_id
        self._file_name = file_name
        self._file_offset = file_offset


