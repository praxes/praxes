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
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg\
    as Toolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import numpy

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------


mpl.rcdefaults()
mpl.rcParams['axes.formatter.limits'] = [-4, 4]
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['legend.fontsize'] = 'small'
Toolbar.margin = 4
numpy.seterr(all='ignore')



def locateClosest(point, points):
    compare = numpy.abs(points-point)
    return numpy.nonzero(numpy.ravel(compare==compare.min()))[0]


class ImageCursor(QtCore.QObject, Cursor):

    def __init__(self, im, useblit=False, parent=None, **lineprops):
        Cursor.__init__(self, im.axes, useblit, **lineprops)
        QtCore.QObject.__init__(self, parent)


        self.canvas.mpl_connect('button_release_event', self.onpick)

        xmin, xmax, ymin, ymax = im.get_extent()
        if im.origin == 'upper': ymin, ymax = ymax, ymin

        self.im = im

        imarray = im.get_array()

        self.indices = numpy.arange(len(im.get_array().flat))
        self.indices.shape = im.get_array().shape

        xshape, yshape = im.get_size()
        self.xPixelLocs = numpy.linspace(xmin, xmax, xshape)
        self.yPixelLocs = numpy.linspace(ymin, ymax, yshape)

    def onpick(self, event):
        if event.inaxes is self.ax:
            xIndex = locateClosest(event.xdata, self.xPixelLocs)
            yIndex = locateClosest(event.ydata, self.yPixelLocs)

            self.emit(QtCore.SIGNAL('pickEvent'), self.indices[yIndex, xIndex])


class QtMplCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        self.figure = Figure()

        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def _createInitialFigure(self, *args, **kwargs):
        raise NotImplementedError

    def enableAutoscale(self, *args, **kwargs):
        raise NotImplementedError

    def enableLogscale(self, *args, **kwargs):
        raise NotImplementedError

    def minimumSizeHint(self):
        return QtCore.QSize(0, 0)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def updateFigure(self, *args, **kwargs):
        raise NotImplementedError


class ElementCanvas(QtMplCanvas):

    _xlabel = ''
    _ylabel = ''
    _xlims = [0, 1]
    _ylims = [0, 1]

    def __init__(self, parent=None):
        QtMplCanvas.__init__(self, parent)
        self.axes = self.figure.add_subplot(111)

    def setXLabel(self, label):
        self._xlabel = label

    def setXLims(self, lims):
        self._xlims = lims

    def setYLabel(self, label):
        self._ylabel = label

    def setYLims(self, lims):
        self._ylims = lims


class ElementImage(ElementCanvas):

    autoscale = True

    def __init__(self, parent=None):
        ElementCanvas.__init__(self, parent)

        self._clim = [0, 1]
        self._image = None
        self._elementData = None
        self._colorbar = None

    def _createInitialFigure(self, elementData):
        self._elementData = elementData
        extent = []
        extent.extend(self._xlims)
        extent.extend(self._ylims)
        self._image = self.axes.imshow(elementData, extent=extent,
                                       aspect=1/1.414, interpolation='nearest',
                                       origin='lower')
        self._colorbar = self.figure.colorbar(self._image)

        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)

    def enableAutoscale(self, val):
        self.autoscale = val
        self.updateFigure()

    def setDataMax(self, val):
        self._clim[1] = val
        self.updateFigure()

    def setDataMin(self, val):
        self._clim[0] = val
        self.updateFigure()

    def setImageAspect(self, aspect):
        self.axes.set_aspect(1/aspect)
        self.updateFigure()

    def setInterpolation(self, val):
        self._image.set_interpolation('%s'%val)
        self.draw()

    def setImageOrigin(self, val):
        self._image.origin = '%s'%val
        self.draw()

    def updateFigure(self, elementData=None):
        if self._image is None:
            self._createInitialFigure(elementData)
        else:
            if elementData is None: elementData = self._elementData
            else: self._elementData = elementData
            self._image.set_data(elementData)

        if self.autoscale:
            self._image.autoscale()
            self._clim = list(self._image.get_clim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._clim[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._clim[1])
        else:
            self._image.set_clim(self._clim)
        self.draw()


class ElementPlot(ElementCanvas):

    def __init__(self,parent=None):
        ElementCanvas.__init__(self, parent)

        self._elementData = None
        self._autoscale = True

    def _createInitialFigure(self, elementData):
        self._elementData = elementData

        self._elementPlot, = self.axes.plot(elementData, 'b')
        self.axes.set_xlabel(self._xlabel)
        self.axes.set_ylabel(self._ylabel)

    def enableAutoscale(self, val):
        self.axes.enable_autoscale_on(val)
        self.updateFigure()

    def setDataMax(self, val):
        self._ylims[1]=val
        self.updateFigure()

    def setDataMin(self, val):
        self._ylims[0]=val
        self.updateFigure()

    def updateFigure(self, elementData=None):
        if self._elementData is None:
            self._createInitialFigure(elementData)
        else:
            if elementData is None: elementData = self._elementData
            else: self._elementData = elementData

            self._elementPlot.set_ydata(elementData)
            self.axes.relim()
            self.axes.autoscale_view()

        self._elementData = elementData

        if self.axes.get_autoscale_on():
            self._ylims = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._ylims[0])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._ylims[1])
        else:
            self.axes.set_ylim(self._ylims)

        self.draw()
