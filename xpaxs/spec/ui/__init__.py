"""
"""

import os

from xpaxs.configutils import ui2py

ui2py(os.path.split(__file__)[0])

del(os, ui2py)
