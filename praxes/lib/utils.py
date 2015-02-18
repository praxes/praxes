import os


class ResourceManager(object):

    def __init__(self, __file__):
        self._root = os.path.split(__file__)[0]

    def __getitem__(self, key):
        return os.path.join(self._root, key)
