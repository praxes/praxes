"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import codecs
import os
import sys
import tempfile
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyMca import ClassMcaTheory , ConcentrationsTool 
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from configuresmp import ConfigureSmp
from mplwidgets import MplCanvas
from ui_scanio2 import Ui_ScanIO
from scancontrols import ScanControls
from scanfeedback import ScanFeedback
from spectromicroscopy.smpcore import SpecRunner, getPymcaConfig,\
    getPymcaConfigFile, getSmpConfig

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

DEBUG = 2 # ??


class ScanIO(Ui_ScanIO, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        self.DEBUG=DEBUG
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        self.setupUi(self)
        
        # TODO: this is for debugging, needs fixing
        if True:
            self.specrunner = SpecRunner(self, DEBUG,
                                         'f3.chess.cornell.edu', 'xrf')
        else:
            self.specrunner = SpecRunner(self, DEBUG,
                                         self.__server, self.__port)
#        self.specrunner.exc("NPTS=0")
        
        self.scanControls = ScanControls(self)
        self.gridlayout.addWidget(self.scanControls,0,0,1,1)

        self.scanFeedback = ScanFeedback(self)
        self.gridlayout.addWidget(self.scanFeedback,0,1,1,1)
        
        # TODO: This probably needs to go in the main app window?
        self.timer = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer,
                               QtCore.SIGNAL("timeout()"),
                               self.specrunner.update)
        self.timer.start(20)

    def config_smp(self):
#        print self.__server,self.__port
        editor = ConfigureSmp(self)
        editor.exec_()
        smpConfig = getSmpConfig()
        self.__server = smpConfig['session']['server']
        self.__port = smpConfig['session']['port']
        print "***",self.__server,self.__port
    
    def set_config_file(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.pymcaConfigFile = "%s"%fd.getOpenFileName()
            config = getPymcaConfig(self.pymcaConfigFile)
            self.__peaks = config["peaks"]
            self.ElementSelect.clear()
            for peak in self.__peaks:
                self.ElementSelect.addItem(peak)
        except:
            print "come on now"

    def config(self):
        smpConfig = getSmpConfig()
        try:
            self.__server = smpConfig['session']['server']
            self.__port = smpConfig['session']['port']
        except KeyError:
            self.config_smp()
        
        # TODO: break this into a new method
        self.pymcaConfigFile = getPymcaConfigFile()
        reader = getPymcaConfig()
        self.__peaks = []
        try:
            elements = reader["peaks"]
            for key in elements.keys():
                self.__peaks.append("%s %s"%(key,elements[key]))
        except KeyError:
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ScanIO()
    myapp.show()
    sys.exit(app.exec_())
