"""
"""

import os

from xpaxs.configutils import qrc2py

qrc2py(os.path.split(__file__)[0])

del(os, qrc2py)
