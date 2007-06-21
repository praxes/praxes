from pylab import *
from PyQt4 import QtGui, QtCore

from matplotlib.numerix import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure




class Testplot(QtGui.QWidget):
    __pyqtSignals__ = ("plotDone(QImage)")
    def __init__(self,parent):
        QtGui.QWidget.__init__(self, parent)
        plot([1,2,3,4])
        show()
        

class TestplotPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent = None):
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self)
        self.initialized = False
    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True
    def isInitialized(self):
        return self.initialized
    def createWidget(self, parent):
        return Testplot(parent)
    def name(self):
        return "Testplot"
    def group(self):
        return "Display Widgets"
    def icon(self):
        return QtGui.QIcon(_logo_pixmap)
    def toolTip(self):
        return ""
    def whatsThis(self):
        return ""
    def isContainer(self):
        return False
    def includeFile(self):
        return "Testplot"
