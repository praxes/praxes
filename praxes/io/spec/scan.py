import numpy as np

class Index(object):

    def __init__(self, **kwargs):
        self._attrs = dict(**kwargs)

    def __contains__(self, item):
        return item in self._attrs

    def __getitem__(self, item):
        return self._attrs[item]

    def __iter__(self):
        return iter(self._attrs)

    def __len__(self):
        return len(self._attrs)

    def items(self):
        "Return a new view of the scan's attributes' ``(key, val)`` pairs."
        return self._attrs.viewitems()

    def keys(self):
        "Return a new view of the scan's attributes' keys."
        return self._attrs.viewkeys()

    def values(self):
        "Return a new view of the scan's attributes' values."
        return self._attrs.viewvalues()


class SpecScan(object):

    __index_finalized = False

    @property
    def attrs(self):
        return self.__attrs

    @property
    def file_offsets(self):
        return self.__file_offset, self.__bytes_read

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def __init__(self, name, id, file, offset, **kwargs):
        self.__name = name
        self.__id = id
        self.__file_name = file.name
        self.__file_offset = offset
        self.__bytes_read = offset

        self.__attrs = Index(**kwargs)
        attrs = self.__attrs._attrs

        attrs['epoch_offset'] = kwargs.get('epoch_offset', 0)
        attrs['file_origin'] = kwargs.get('file_origin', '')
        attrs['positioners'] = kwargs.get('positioners', [])
        attrs['program'] = kwargs.get('program', '')
        attrs['user'] = kwargs.get('user', '')

        self.__data_index = []
        self.__index = {}
        self.__mca_index = {}

        self.update()

    def __contains__(self, item):
        return item in self.__index

    def __getitem__(self, item):
        return self.__index[item]

    def __iter__(self):
        return iter(self.__index)

    def __len__(self):
        return len(self.__index)

    def items(self):
        "Return a new view of the scan's attributes' ``(key, val)`` pairs."
        return self.__index.viewitems()

    def keys(self):
        "Return a new view of the scan's attributes' keys."
        return self.__index.viewkeys()

    def values(self):
        "Return a new view of the scan's attributes' values."
        return self.__index.viewvalues()


    def update(self):
        if self.__index_finalized:
            return

        with open(self.__file_name, 'rb') as f:
            attrs = self.__attrs._attrs
            f.seek(self.__bytes_read)
            file_offset = f.tell()
            line = f.readline()
            while line:
                if line[0].isdigit() or line[0] == '-':
                    self.__data_index.append(file_offset)
                elif line[0] == '@':
                    key = line.split()[0][1:]
                    try:
                        self.__mca_index[key].append(file_offset)
                    except KeyError:
                        self.__mca_index[key] = [file_offset]
                elif line[:2] == '#S':
                    if 'command' in attrs:
                        self.__index_finalized = True
                        break
                    attrs['command'] = ' '.join(line.split()[2:])
                elif line[:2] == '#D':
                    attrs['date'] = line[3:-1]
                elif line[:2] in ('#T', '#M'):
                    x, val, key = line.split()
                    key = key[1:-1]
                    attrs['duration'] = (key, float(val))
                    if x == '#M':
                        attrs['monitor'] = key
                elif line[:2] == '#G':
                    orientations = attrs.setdefault('orientations', [])
                    orientations.append(
                        [float(i) for i in line.split()[1:]]
                        )
                elif line[:2] == '#Q':
                    attrs['hkl'] = [float(i) for i in line.split()[1:]]
                elif line[:2] == '#P':
                    positions = attrs.setdefault('positions', [])
                    positions.extend(
                        [float(i) for i in line.split()[1:]]
                        )
                elif line[:2] == '#C':
                    comments = attrs.setdefault('comments', [])
                    comments.append(line[3:-1])
                elif line[:2] == '#U':
                    user_comments = attrs.setdefault('user_comments', [])
                    user_comments.append(line[3:-1])
                elif line[:2] == '#L':
                    attrs['labels'] = labels = line.split()[1:]
                    for column, label in enumerate(labels):
                        # TODO: Need to write the proxy interface for the data
                        # the proxy constructor should accept the data_index and
                        # the column index
                        self.__index[label] = ScalarProxy(
                            self.__file_name, label, column, self.__data_index
                            )

                file_offset = f.tell()
                line = f.readline()

            self.__bytes_read = f.tell()

        if 'positioners' in attrs:
            positioners = attrs.pop('positioners')
            positions = attrs.pop('positions')
            attrs['positions'] = dict(zip(positioners, positions))


class ScalarProxy(object):

    @property
    def name(self):
        return self.__name

    def __init__(self, file_name, name, column, data_index):
        self.__file_name = file_name
        self.__name = name
        self.__column = column
        self.__data_index = data_index

    def __len__(self):
        return len(self.__data_index)

    def __iter__(self):
        raise NotImplementedError

    def __getitem__(self, args):
        with open(self.__file_name) as f:
            if isinstance(args, int):
                f.seek(self.__data_index[args])
                l = f.readline()
                return np.fromstring(l, dtype='d', sep=' ')[self.__column]
            if isinstance(args, slice):
                args = xrange(args.start or 0, args.stop or len(self), args.step or 1)
            elif args is Ellipsis:
                args = xrange(len(self))
            temp = []
            for i in args:
                f.seek(self.__data_index[i])
                l = f.readline()
                temp.append(np.fromstring(l, dtype='f', sep=' ')[self.__column])
            return np.asarray(temp)
