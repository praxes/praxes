

class FileIndex(object):

    def __init__(self, file_name):
        self._file_name = file_name
        self._bytes_read = 0
        # would be nice to use python-2.7's ordered dict:
        self._scan_list = []
        self._scan_dict = {}

        self.update()

    def __getitem__(self, item):
        "should accept either a string or an integer"
        raise NotImplementedError

    def __len__(self):
        return len(self._scan_list)

    def __iter__(self):
        return iter(self._scan_list)

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
                    self._scan_list.append(scan_index)
                file_offset += len(line)
            self._bytes_read = file_offset


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


