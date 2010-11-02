"""
"""

import cStringIO
import tokenize

import numpy as np


__all__ = ['simple_eval']


def _iterable(next, terminator):
    out = []
    token = next()
    while token[1] != terminator:
        out.append(_atom(next, token))
        token = next()
        if token[1] == ",":
            token = next()
    return out

def _dictable(next):
    out = []
    token = next()
    while token[1] != '}':
        k = _atom(next, token)
        token = next()
        token = next()
        v = _atom(next, token)
        out.append((k, v))
        token = next()
        if token[1] == ",":
            token = next()
    return dict(out)

def _atom(next, token):
    if token[1] == "(":
        return tuple(_iterable(next, ')'))
    if token[1] == "[":
        return list(_iterable(next, ']'))
    if token[1] == "{":
        return _dictable(next)
    if token[1] == "array":
        token = next()
        return np.array(*_iterable(next, ')'))
    elif token[0] is tokenize.STRING:
        return token[1][1:-1].decode("string-escape")
    elif token[0] is tokenize.NUMBER:
        try:
            return int(token[1], 0)
        except ValueError:
            return float(token[1])
    elif token[1] == "-":
        token = list(next())
        token[1] = "-" + token[1]
        return _atom(next, token)
    elif token[0] is tokenize.NAME:
        if token[1] == 'None':
            return None
        raise ValueError('tokenize NAME: %s unrecognized' % token[1])
    elif not token[0]:
        return
    for i, v in tokenize.__dict__.iteritems():
        if v == token[0]:
            raise ValueError("tokenize.%s unrecognized: %s" % (i, token[1]))

def simple_eval(source):
    """a safe version of the builtin eval function, """
    src = cStringIO.StringIO(source).readline
    src = tokenize.generate_tokens(src)
    return _atom(src.next, src.next())
