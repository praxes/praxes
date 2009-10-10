"""
"""

from __future__ import with_statement

from functools import wraps


def sync(f):
    @wraps(f)
    def g(self, *args, **kwargs):
        with self.plock:
            return f(self, *args, **kwargs)
    return g


def with_doc(method, use_header=''):
    pass

class with_doc:

    """
    This decorator combines the docstrings of the provided and decorated objects
    to produce the final docstring for the decorated object.
    """

    def __init__(self, method, use_header=True):
        self.method = method
        if use_header:
            self.header = \
    """

    Specific to phynx:
    """
        else:
            self.header = ''

    def __call__(self, new_method):
        new_doc = new_method.__doc__
        original_doc = self.method.__doc__
        header = self.header

        if original_doc and new_doc:
            new_method.__doc__ = """
    %s
    %s
    %s
        """ % (original_doc, header, new_doc)

        elif original_doc:
            new_method.__doc__ = original_doc

        return new_method
