import __builtin__
import copy
import operator
import posixpath


def sequential(values):
    print values
    def key(value):
        if 'start_time' in value.attrs:
            return value.attrs['start_time']
        elif 'end_time' in value.attrs:
            return value.attrs['end_time']
        else:
            try:
            	return posixpath.split(value.name[-1])
            except AttributeError:
                return value

    return __builtin__.sorted(values, key=key)
