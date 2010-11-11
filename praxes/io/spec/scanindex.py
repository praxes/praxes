class ScanIndex(object):

    _dirty = True
    @property
    def dirty(self):
        return self._dirty
    @dirty.setter
    def dirty(self, val):
        self._dirty = val

    def __init__(self, file_name, file_offset):
        self._file_name = file_name
        self._file_offset = file_offset

    def update(self):
        self.dirty = False
