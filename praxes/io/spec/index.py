from copy import copy


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

    def _create_scan_index(self, scan_name, file_offset):
        scan_id = self.get_unique_id(scan_name)
        scan_index = ScanIndex(
            scan_name,
            scan_id,
            self._file_name,
            file_offset
            )
        self._scan_dict[scan_id] = scan_index
        self._id_list.append(scan_id)

    def get_unique_id(self, scan_name):
        scan_id = scan_name
        dup = 1
        while scan_id in self._scan_dict:
            dup += 1
            scan_id = '%s.%d' % (scan_name, dup)
        return scan_id

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
        with open(self._file_name, 'r+b') as f:
            if len(self._id_list):
                # updating an existing file index, will probably have
                # to mark the last scan index as dirty so the data can
                # be updated
                f.seek(0, 2)
                if f.tell() > self._bytes_read:
                    # assume new data has been appended to the previous scan
                    # might be able to improve this
                    self._scan_dict[self._id_list[-1]].dirty = True

            f.seek(self._bytes_read)
            file_offset = f.tell()
            for line in f:
                if line[:2] == '#S':
                    self._create_scan_index(line.split()[1], file_offset)
                file_offset += len(line)

            self._bytes_read = file_offset

    def values(self):
        return [self._scan_dict[i] for i in self._id_list]


class ScanIndex(object):

    _dirty = True
    @property
    def dirty(self):
        return self._dirty
    @dirty.setter
    def dirty(self, val):
        self._dirty = val

    @property
    def id(self):
        return self._scan_id

    @property
    def name(self):
        return self._scan_name

    def __init__(self, scan_name, scan_id, file_name, file_offset):
        self._scan_name = scan_name
        self._scan_id = scan_id
        self._file_name = file_name
        self._file_offset = file_offset

    def update(self):
        self.dirty = False
