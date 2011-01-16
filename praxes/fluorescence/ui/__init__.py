"""
"""

import os

from praxes.config import qrc2py, ui2py

qrc2py(os.path.split(__file__)[0])
ui2py(os.path.split(__file__)[0])

del(os, qrc2py, ui2py)
