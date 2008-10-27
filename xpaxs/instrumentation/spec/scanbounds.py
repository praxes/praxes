#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# GUI imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_gamepad
from xpaxs.instrumentation.spec import TEST_SPEC
from xpaxs.instrumentation.spec.motorwidget import MotorWidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanBounds(object):

    def __init__(self, start=None, stop=None):
        self.start = start
        self.stop = stop


class ScanBoundsDict(dict):

    def __getitem__(self, item):
        if not item in self:
            self[item] = ScanBounds()
        return super(ScanBoundsDict, self).__getitem__(item)

    def __setitem__(self, item, val):
        assert isinstance(val, ScanBounds)

        super(ScanBoundsDict, self).__setitem__(item, val)

