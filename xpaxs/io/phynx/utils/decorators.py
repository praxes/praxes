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
