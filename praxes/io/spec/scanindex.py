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
