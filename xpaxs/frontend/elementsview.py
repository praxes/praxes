"""
"""
from __future__ import absolute_import

import logging

import numpy as np
from PyQt4 import QtCore, QtGui

from .plotwidgets import QtMplCanvas, Toolbar
from .plotoptions import PlotOptions


logger = logging.getLogger(__file__)
DEBUG = False

def locateClosest(point, points):
    compare = np.abs(points-point)
    return np.nonzero(np.ravel(compare==compare.min()))[0]


class ElementBaseFigure(QtMplCanvas):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementBaseFigure, self).__init__(parent)

        self.scanData = scanData
        self.autoscale = True

        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])

        self._elementData = self.window().getElementMap()
        self._createInitialFigure()

    def _createInitialFigure(self):
        raise NotImplementedError

    def getIndices(self, xdata, ydata):
        xIndex = locateClosest(xdata, self.xPixelLocs)
        yIndex = locateClosest(ydata, self.yPixelLocs)
        return xIndex, yIndex

    def onPick(self, xstart, ystart, xend, yend):
        xstart_i, ystart_i = self.getIndices(xstart, ystart)
        xend_i, yend_i = self.getIndices(xend, yend)

        if xstart_i > xend_i: xstart_i, xend_i = xend_i, xstart_i
        if ystart_i > yend_i: ystart_i, yend_i = yend_i, ystart_i

        try:
            indices = self.indices[ystart_i:yend_i+1, xstart_i:xend_i+1]
            self.emit(QtCore.SIGNAL('pickEvent'), indices.flatten())
        except TypeError:
            # This occurs when args to onPick are len > 1. How can this happen?
            pass

    def setXLabel(self, label):
        self._xlabel = label

    def setXLims(self, lims):
        self._xlims = lims

    def setYLabel(self, label):
        self._ylabel = label

    def setYLims(self, lims):
        self._ylims = lims


class ElementImageFigure(ElementBaseFigure):

    def __init__(self, scanData, parent=None):
        super(ElementImageFigure, self).__init__(scanData, parent)

        min, max = self._elementData.min(), self._elementData.max()
        self._clim = [min, max or float(max==0)]
        self._updatePixelMap()

    def _updatePixelMap(self):
        xmin, xmax, ymin, ymax = self.image.get_extent()
        if self.image.origin == 'upper': ymin, ymax = ymax, ymin

        imarray = self.image.get_array()


        self.indices = np.arange(len(self.image.get_array().flatten()))
        self.indices.shape = self.image.get_array().shape

        yshape, xshape = self.image.get_size()
        self.xPixelLocs = np.linspace(xmin, xmax, xshape)
        self.yPixelLocs = np.linspace(ymin, ymax, yshape)

    def _createInitialFigure(self):
        extent = []
        sd = self.scanData['scalar_data']
        x_axis = sd.get_sorted_axes_list(1)[0]
        y_axis = sd.get_sorted_axes_list(2)[0]
        extent.extend(x_axis.range)
        extent.extend(y_axis.range)
        self.image = self.axes.imshow(self._elementData, extent=extent,
                                       interpolation='nearest',
                                       origin='lower')
        self._colorbar = self.figure.colorbar(self.image)

        self.axes.set_xlabel(x_axis.name)
        try: self.axes.set_ylabel(y_axis.name)
        except IndexError: pass

    def enableAutoscale(self, val):
        self.autoscale = val
        self.updateFigure()

    def setDataMax(self, val):
        self._clim[1] = val
        self.updateFigure()

    def setDataMin(self, val):
        self._clim[0] = val
        self.updateFigure()

    def setInterpolation(self, val):
        self.image.set_interpolation('%s'%val)
        self.draw()

    def setImageOrigin(self, val):
        self.image.origin = '%s'%val
        self._updatePixelMap()
        self.updateFigure()

    def updateFigure(self, elementData=None):
        if elementData is None: elementData = self._elementData
        else: self._elementData = elementData
        self.image.set_data(elementData)

        if self.autoscale:
            self.image.autoscale()
            self._clim = list(self.image.get_clim())
            self.emit(QtCore.SIGNAL("minValueChanged"), self._clim[0])
            self.emit(QtCore.SIGNAL("maxValueChanged"), self._clim[1])
        else:
            self.image.set_clim(self._clim)

        self.draw()


class ElementPlotFigure(ElementBaseFigure):

    def __init__(self, scanData, parent=None):
        super(ElementPlotFigure, self).__init__(scanData, parent)

        self._updatePixelMap()

    def _createInitialFigure(self):
        try:
            self.x_data = self.scanData['scalar_data'].get_sorted_axes_list(1)[0]
            self._elementPlot, = self.axes.plot(self.xdata, self._elementData)
            self.axes.set_xlabel(x_axis.name)
            self.axes.set_xlim(self.x_data.range)
        except:
            self._elementPlot, = self.axes.plot(self._elementData)

    def _updatePixelMap(self):
        xmin, xmax = self.axes.get_xlim()

        data = self.axes.get_lines()[0].get_xdata()

        self.indices = np.arange(len(data))
        self.indices.shape = (1, len(data))

        self.xPixelLocs = np.linspace(xmin, xmax, len(data))
        self.yPixelLocs = [0]

    def enableAutoscale(self, val):
        self.axes.set_autoscale_on(val)
        self.updateFigure()

    def setDataMax(self, val):
        self._ylims[1] = val
        self.updateFigure()

    def setDataMin(self, val):
        self._ylims[0] = val
        self.updateFigure()

    def updateFigure(self, elementData=None):
        if elementData is None: elementData = self._elementData
        else: self._elementData = elementData


        self._elementPlot.set_xdata(self.x_data.value[:self.x_data.acquired])
        self._elementPlot.set_ydata(elementData[:self.x_data.acquired])
        self.axes.relim()
        self.axes.autoscale_view()

        if self.axes.get_autoscale_on():
            self._ylims = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("minValueChanged"), self._ylims[0])
            self.emit(QtCore.SIGNAL("maxValueChanged"), self._ylims[1])
        else:
            self.axes.set_ylim(self._ylims)

        self.draw()


class ElementsView(QtGui.QGroupBox):

    def __init__(self, scanData, parent=None):
        super(ElementsView, self).__init__(parent)
        self.setObjectName("elementsView")
        self.setTitle('Elements View')

        layout = QtGui.QVBoxLayout()

        if len(scanData.acquisition_shape) == 2:
            self.figure = ElementImageFigure(scanData, self)

        else:
            self.figure = ElementPlotFigure(scanData, self)

        self.toolbar = Toolbar(self.figure, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.figure)
        self.setLayout(layout)

        self._plotOptions = PlotOptions(scanData, self.figure)

        self.connect(
            self.toolbar,
            QtCore.SIGNAL("pickEvent"),
            self.figure.onPick
        )
        self.connect(
            self.figure,
            QtCore.SIGNAL("pickEvent"),
            self,
            QtCore.SIGNAL("pickEvent")
        )

    @property
    def plotOptions(self):
        return self._plotOptions

    def __getattr__(self, attr):
        return getattr(self.figure, attr)
