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
        
        self._xlabel = ''
        self._ylabel = ''
        self._xlims = [0, 1]
        self._ylims = [0, 1]
    
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

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
        raise NotImplementedError

    def enableAutoscale(self, value):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def setXLabel(self, label):
        self._xlabel = label
    
    def setXLims(self, lims):
        self._xlims = lims

    def setYLabel(self, label):
        self._ylabel = label
    
    def setYLims(self, lims):
        self._ylims = lims


class McaSpectrum(QtMplCanvas):

    def __init__(self, parent=None):
        self.fitData = {}

        self.figure = Figure()
        self.spectrumAxes = self.figure.add_axes([.1, .4, .85, .55])
        self.spectrumAxes.xaxis.set_visible(False)
        self.spectrumAxes.set_ylabel('Counts')
        
        self.residualsAxes = self.figure.add_axes([.1, .15, .85, .225], 
                                                  sharex=self.spectrumAxes)
        # We want the residualsAxes cleared every time plot() is called
        self.residualsAxes.set_yticks([-1, 0, 1])
        self.residualsAxes.set_ylim(-2, 2)
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')

        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def createInitialFigure(self, fitData):
        self.dataLine, = self.spectrumAxes.plot(fitData['energy'],
                                               fitData['ydata'],
                                               'b', linewidth=1.5)
        self.fitLine, = self.spectrumAxes.plot(fitData['energy'],
                                              fitData['yfit'],
                                              'k', linewidth=1.5)
        self.spectrumAxes.set_ylabel('Counts')
        
        self.resLine, = self.residualsAxes.plot(fitData['energy'],
                                               fitData['residuals'],
                                               'k', linewidth=1.5)
        ytick = self.residualsAxes.get_yticks()[0]
        self.residualsAxes.set_yticks([ytick, 0, -ytick])
        self.residualsAxes.set_ylabel('Res.')
        self.residualsAxes.set_xlabel('Energy (KeV)')
        
        self.fitData = fitData
        self.draw()

    def updateFigure(self, fitData=None):
        if self.fitData == {}:
            self.createInitialFigure(fitData)
            return
        
        if not fitData: fitData = self.fitData
        
        self.dataLine.set_ydata(fitData['ydata'])
        self.fitLine.set_ydata(fitData['yfit'])
        if self.spectrumAxes.get_yscale() == 'log':
            self.resLine.set_ydata(fitData['logresiduals'])
        else:
            self.resLine.set_ydata(fitData['residuals'])
        
        self.fitData = fitData
        
        self.spectrumAxes.relim()
        self.spectrumAxes.autoscale_view()
        
        self.residualsAxes.relim()
        self.residualsAxes.autoscale_view()
        ytick = self.residualsAxes.get_yticks()[0]
        self.residualsAxes.set_yticks([ytick, 0, -ytick])
        
        self.draw()

    def enableAutoscale(self, val):
        self.spectrumAxes.set_autoscale_on(val)
        self.residualsAxes.set_autoscale_on(val)
        self.updateFigure()

    def enableLogscale(self, val):
        if val:
            isAutoscaled = self.spectrumAxes.get_autoscale_on()
            self.spectrumAxes.set_autoscale_on(True)
            self.spectrumAxes.set_yscale('log')
            self.updateFigure()
            self.spectrumAxes.set_autoscale_on(isAutoscaled)
        else:
            self.spectrumAxes.set_yscale('linear')
            self.updateFigure()


class ElementImage(QtMplCanvas):

    def __init__(self, parent=None):
        QtMplCanvas.__init__(self, parent)
        
        self.autoscale = True
        self._lim = [0, 1]

        self._image = None
        self._imageData = None
        self._colorbar = None
        
    def computeInitialFigure(self, imageData):
        self._imageData = imageData
        extent = []
        extent.extend(self._xlims)
        extent.extend(self._ylims)
        self._image = self.axes.imshow(imageData, extent=extent, 
                                       aspect=1/1.414)
        if self._colorbar is None:
            self._colorbar = self.figure.colorbar(self._image)
        else:
            self._colorbar.ax.cla()
            self._colorbar = self.figure.colorbar(self._image,
                                                  self._colorbar.ax)
        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)

    def updateFigure(self, imageData=None):
        if self._image is None:
            self.computeInitialFigure(imageData)
        else:
            if imageData is None: imageData = self._imageData
            else: self._imageData = imageData
            self._image.set_data(imageData)
            
        if self.autoscale:
            self._image.autoscale()
            self._clim = list(self._image.get_clim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._clim[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._clim[1])
        else:
            print self._clim
            self._image.set_clim(self._clim)
        self.draw()

    def setDataMin(self, val):
        self._clim[0] = val
        self.updateFigure()

    def setDataMax(self, val):
        self._clim[1] = val
        self.updateFigure()

    def setImageAspect(self, aspect):
        self.axes.set_aspect(1/aspect)
        self.updateFigure()


class ElementPlot(ElementImage):
    def __init__(self,parent=None):
        QtMplCanvas.__init__(self, parent)
        
        self._ylim = [0, 1]
        self._plot = None
        self.autoscale = True

    def computeInitialFigure(self, imageData):
        self._imageData = imageData
        self._plot = self.axes.plot(imageData,"b-")
        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)
        
    def updateFigure(self, imageData=None):
        if self._plot is None:
            self.computeInitialFigure(imageData)
        else:
            if imageData is None: imageData = self._imageData
            else: self._imageData = imageData
            self._plot=self.axes.plot(imageData,"b-")
            
        if self.autoscale:
            self._ylim = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._ylim[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._ylim[1])
        else:
            self.axes.set_ylim(self._ylim[0], self._ylim[1])
        self.draw()

    def setDataMin(self, val):
        self._ylim[0]=val
        self.updateFigure()

    def setDataMax(self, val):
        self._ylim[1]=val
        self.updateFigure()
