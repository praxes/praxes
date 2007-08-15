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
numpy.seterr(all='ignore')

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class QtMplCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        self.useLogScale = False
        self.autoscale = False
    
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

#        self.computeInitialFigure()

        FigureCanvasQTAgg.__init__(self, self.figure)
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

    def enableLogscale(self, value):
        self.useLogScale = value
        self.updateFigure()

    def enableAutoscale(self, value):
        self.autoscale = value
        self.updateFigure()

    def clear(self):
        raise NotImplementedError

#    def computeInitialFigure(self)
#        pass


class McaSpectrum(QtMplCanvas):

    def __init__(self, parent=None):
        self.useLogScale = False
        self.fitData = {}
        self.autoscale = False
        
        self.figure = Figure()
        self.spectrumAxes = self.figure.add_axes([.1, .4, .85, .55])
        # We want the spectrumAxes cleared every time plot() is called
        self.spectrumAxes.hold(False)
        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')
        
        self.residualsAxes = self.figure.add_axes([.1, .15, .85, .225], 
                                               sharex=self.spectrumAxes)
        # We want the residualsAxes cleared every time plot() is called
        self.residualsAxes.set_yticks([-1, 0, 1])
        self.residualsAxes.set_ylim(-2, 2)
        self.residualsAxes.hold(False)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def updateFigure(self, fitData=None):
        
        if self.fitData =={}: autoscale = True
        else: autoscale = self.autoscale
        
        if fitData: self.fitData = fitData
        else: fitData = self.fitData
        
        x = fitData['energy'].copy()
        y = fitData['ydata'].copy()
        yfit = fitData['yfit'].copy()
        
        if self.useLogScale:
            self.spectrumAxes.set_yscale('log')
            plot = self.spectrumAxes.semilogy
            residuals = fitData['logresiduals'].copy()
        else:
            self.spectrumAxes.set_yscale('linear')
            plot = self.spectrumAxes.plot
            residuals = fitData['residuals'].copy()
        
        plot(x, y, 'b', linewidth=1.5, scalex=autoscale, scaley=autoscale)
        self.spectrumAxes.hold(True)
        plot(x, yfit, 'k', linewidth=1.5, scalex=autoscale, scaley=autoscale)
        xlims = self.spectrumAxes.get_xlim()
        self.spectrumAxes.hold(False)

        self.residualsAxes.plot(x, residuals, 'k', linewidth=1.5, 
                                scalex=autoscale, scaley=autoscale)
        ytick = self.residualsAxes.get_yticks()[0]
        self.residualsAxes.set_yticks([ytick, 0, -ytick])
        
        self.draw()
    
    def enableLogscale(self, value):
        self.useLogScale = value
        self.updateFigure()

    def clear(self):
        self.spectrumAxes.cla()
        self.residualsAxes.cla()


class ElementImage(QtMplCanvas):

    def __init__(self, parent=None):
        QtMplCanvas.__init__(self, parent)
        self._image = None
        
        self._imageData = None
        self._colorbar = None
        
        self.autoscale = True
        
        self._vmin = 0
        self._vmax = 1
        self._extent = [0, 1, 0, 1]

    def computeInitialFigure(self, imageData):
        self._imageData = imageData
        self._image = self.axes.imshow(imageData, extent=self._extent, 
                                       aspect='equal')
        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)
        self._colorbar = self.figure.colorbar(self._image)

    def updateFigure(self, imageData=None):
        if self._image is None:
            self.computeInitialFigure(imageData)
        else:
            if imageData is None: imageData = self._imageData
            else: self._imageData = imageData
            self._image.set_data(imageData)
            
        if self.autoscale:
            self._image.autoscale()
            self._vmin, self._vmax = self._image.get_clim()
            self.emit(QtCore.SIGNAL("imageMin(PyQt_PyObject)"), self._vmin)
            self.emit(QtCore.SIGNAL("imageMax(PyQt_PyObject)"), self._vmax)
        else:
            self._image.set_clim(self._vmin, self._vmax)

        self.axes.set_aspect('equal')
        self.draw()

    def setImageMin(self, val):
        self._vmin = val
        self.updateFigure()

    def setImageMax(self, val):
        self._vmax = val
        self.updateFigure()

    def clear(self):
#        self.axes.cla()
#        self._image = None
#        self._imageData = None
#        self._colorbar = None
        pass
    
    def setXLabel(self, label):
        self._xlabel = label
    
    def setXLims(self, lims):
        self._extent[:2] = lims

    def setYLabel(self, label):
        self._ylabel = label
    
    def setYLims(self, lims):
        self._extent[2:] = lims
