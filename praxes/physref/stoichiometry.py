from collections import OrderedDict
import re

_parser = re.compile("([A-Z][a-z]?)([\d\.]*)")

def parse(s):
    """returns a dictionary representation of the stoichiometry"""
    temp = _parser.findall(s)
    res = OrderedDict()
    for k, v in temp:
        v = 1.0 if not v else float(v)
        res[k] = res.setdefault(k, 0) + v
    return res
