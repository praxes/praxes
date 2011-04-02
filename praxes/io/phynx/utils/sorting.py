import copy
import operator
import posixpath


def sequential(values):
    def key(value):
        if 'start_time' in value.attrs:
            return value.attrs['start_time']
        elif 'end_time' in value.attrs:
            return value.attrs['end_time']
        else:
            try:
            	return value.name
            except AttributeError:
                return value

    return sorted(values, key=key)
