from collections import OrderedDict
import re

_parser = re.compile("([A-Z][a-z]?)([\d\.]*)")


def load(s):
    return Composition(s)


class Composition(OrderedDict):

    """A dictionary representation of a stoichiometry or weight percent"""

    def __init__(self, s):
        super(Composition, self).__init__()
        temp = _parser.findall(s)
        for k, v in temp:
            v = 1.0 if not v else float(v)
            self[k] = self.setdefault(k, 0) + v

    def __str__(self):
        res = ''
        for k, v in self.items():
            res += "%s%g" % (k, v)
        return res
