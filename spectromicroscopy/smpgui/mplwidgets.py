"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
import matplotlib as mpl
mpl.rcdefaults()
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg\
    as Toolbar
from matplotlib.figure import Figure
import numpy

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class QtMplCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(0, 0)


class McaSpectrum(QtMplCanvas):

    def compute_initial_figure(self):
         self.mcaData, = self.axes.semilogy([0, 1024], [1, 1], '.')

    def update_figure(self, temp):
        self.axes.semilogy(*temp['MCA_DATA'])

        self.draw()


class ElementImage(QtMplCanvas):

    def compute_initial_figure(self):
         self.axes.imshow(numpy.random.rand(100, 100))

    def update_figure(self, temp):
        self.axes.imshow(numpy.random.rand(100, 100))

        self.draw()
