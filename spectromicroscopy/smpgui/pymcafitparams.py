"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import copy
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyMca import ConfigDict, Elements, FitParam, PyMca_Icons, PyMcaDirs
from PyQt4 import QtGui, QtCore

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class PyMcaFitParams(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.initDir = None
        layout = QtGui.QVBoxLayout(self)
        layout.setMargin(5)
        layout.setSpacing(5)

        self.fitparam = FitParam.FitParamWidget(self)
#        self.fitparam.peakTable.setSizePolicy(QtGui.QSizePolicy.Expanding,
#                                              QtGui.QSizePolicy.Expanding)
        layout.addWidget(self.fitparam)

        buts = QtGui.QGroupBox(self)
        buts.layout = QtGui.QHBoxLayout(buts)
        load = QtGui.QPushButton(buts)
        load.setText("Load")
        save = QtGui.QPushButton(buts)
        save.setText("Save")
        accept = QtGui.QPushButton(buts)
        accept.setText("OK")

        buts.layout.addWidget(load)
        buts.layout.addWidget(save)
        buts.layout.addWidget(accept)
        layout.addWidget(buts)

#        maxheight = QtGui.QDesktopWidget().height()
#        maxwidth = QtGui.QDesktopWidget().width()
        self.setMaximumWidth(950)
        self.setMaximumHeight(700)
#        self.resize(100, 100)
        self.fitparam.peakTable.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                              QtGui.QSizePolicy.MinimumExpanding)

        self.connect(load, QtCore.SIGNAL("clicked()"), self.load)
        self.connect(save, QtCore.SIGNAL("clicked()"), self.save)
        self.connect(accept, QtCore.SIGNAL("clicked()"), self.configChanged)

    def configChanged(self):
        self.emit(QtCore.SIGNAL("configChanged(PyQt_PyObject)"),
                  self.getParameters())

    def setParameters(self, pars):
        self.fitparam.setParameters(pars)

    def getParameters(self):
        return self.fitparam.getParameters()

    def loadParameters(self, filename, sections=None):
        cfg= ConfigDict.ConfigDict()
        if sections is not None:
            if 'attenuators' in sections:
                sections.append('materials')
                sections.append('multilayer')
        try:
            cfg.read(filename, sections)
            self.initDir = os.path.dirname(filename)
        except:
            QtGui.QMessageBox.critical(self, "Load Parameters",
                "ERROR while loading parameters from\n%s"%filename, 
                QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
            return 0
        self.setParameters(copy.deepcopy(cfg))
        return 1


    def __copyElementsMaterial(self):
        pars = {}
        for material in Elements.Material.keys():
            pars[material] = {}
            for key in Elements.Material[material].keys():
                pars[material][key] = Elements.Material[material][key]      
        return pars
        
    def saveParameters(self, filename, sections=None):
        pars= self.getParameters()
        if sections is None:
            pars['materials'] = self.__copyElementsMaterial()
        elif 'attenuators' in sections:
            pars['materials'] = self.__copyElementsMaterial()
            sections.append('materials')
            sections.append('multilayer')
        cfg= ConfigDict.ConfigDict(initdict=pars)
        if sections is not None:
            for key in cfg.keys():
                if key not in sections:
                    del cfg[key]            
        try:
            cfg.write(filename, sections)
            self.initDir = os.path.dirname(filename)
            return 1
        except:
            QtGui.QMessageBox.critical(self, "Save Parameters", 
                "ERROR while saving parameters to\n%s"%filename,
                QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)
            return 0

    def load(self):

        if self.initDir is None:
            self.initDir = PyMcaDirs.inputDir
        
        filedialog = QtGui.QFileDialog(self)
        filedialog.setFileMode(filedialog.ExistingFiles)
        filedialog.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(PyMca_Icons.IconDict["gioconda16"])))
        initdir = os.path.curdir
        if self.initDir is not None:
            if os.path.isdir(self.initDir):
                initdir = self.initDir
        filename = filedialog.getOpenFileName(
                    self,
                    "Choose fit configuration file",
                    initdir,
                    "Fit configuration files (*.cfg)\nAll Files (*)")
        filename = str(filename)
        if len(filename):
            self.loadParameters(filename, None)
            self.initDir = os.path.dirname(filename)


    def save(self):
        if self.initDir is None:
            self.initDir = PyMcaDirs.outputDir

        filedialog = QtGui.QFileDialog(self)
        filedialog.setFileMode(filedialog.AnyFile)
        filedialog.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(PyMca_Icons.IconDict["gioconda16"])))
        initdir = os.path.curdir
        if self.initDir is not None:
            if os.path.isdir(self.initDir):
                initdir = self.initDir
        filename = filedialog.getSaveFileName(
                    self,
                    "Enter output fit configuration file",
                    initdir,
                    "Fit configuration files (*.cfg)\nAll Files (*)")
        filename = str(filename)
        if len(filename):
            if len(filename) < 4:
                filename = filename+".cfg"
            elif filename[-4:] != ".cfg":
                filename = filename+".cfg"
            self.saveParameters(filename, None)
            self.initDir = os.path.dirname(filename)
