"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from ui_scanfeedback import Ui_ScanFeedback

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanFeedback(Ui_ScanFeedback, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
