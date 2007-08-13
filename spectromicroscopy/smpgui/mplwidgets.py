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

        self.computeInitialFigure()

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

    def computeInitialFigure(self):
         self.mcaData, = self.axes.plot([0, 1024], [1, 1], '.')

    def updateFigure(self, fitData):
        x = fitData['xdata']
        y = fitData['ydata']
        yfit = fitData['yfit']
        residuals = yfit - y
        offset = numpy.amax(residuals)
        self.axes.plot(x, y, 'ob')
        self.axes.hold(True)
        self.axes.plot(x, yfit, 'k', linewidth=2)
        # TODO: break resdiuals into a separate linear (not semilog) plot, with
        # residuals = log(yfit)-log(y)
        self.axes.plot(x, residuals - 1.5*offset, 'k', linewidth=2)
        self.axes.hold(False)
        self.draw()


class ElementImage(QtMplCanvas):

    def computeInitialFigure(self):
         self.axes.imshow(numpy.random.rand(100, 100))

    def updateFigure(self, image):
        vmax = numpy.amax(image)
        self.axes.imshow(image, vmin=0, vmax=vmax)

        self.draw()
