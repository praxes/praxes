"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from ui_scancontrols import Ui_ScanControls

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanMotor(Ui_ScanMotor, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self,parent=None):
        self.DEBUG=DEBUG
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        self.setupUi(self)
