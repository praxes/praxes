"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import numpy
from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from xpaxs import plotwidgets
from xpaxs.spectromicroscopy.ui import ui_elementsimage, ui_elementsplot

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.spectromicroscopy.elementsview')
DEBUG = True

def locateClosest(point, points):
    compare = numpy.abs(points-point)
    return numpy.nonzero(numpy.ravel(compare==compare.min()))[0]


class ElementBaseFigure(plotwidgets.QtMplCanvas):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementBaseFigure, self).__init__(parent)

        self.scanData = scanData
        self.autoscale = True

        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])

        self._elementData = self.window().getElementMap()
        self._createInitialFigure()

        self.connect(self.scanData,
                     QtCore.SIGNAL("elementDataChanged"),
                     self.updateFigure)

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


        self.indices = numpy.arange(len(self.image.get_array().flatten()))
        self.indices.shape = self.image.get_array().shape

        yshape, xshape = self.image.get_size()
        self.xPixelLocs = numpy.linspace(xmin, xmax, xshape)
        self.yPixelLocs = numpy.linspace(ymin, ymax, yshape)

    def _createInitialFigure(self):
        extent = []
        xlim = self.scanData.getScanRange(self.scanData.getScanAxis(0, 0))
        extent.extend(xlim)
        ylim = self.scanData.getScanRange(self.scanData.getScanAxis(1, 0))
        extent.extend(ylim)
        self.image = self.axes.imshow(self._elementData, extent=extent,
                                       interpolation='nearest',
                                       origin='lower')
        self._colorbar = self.figure.colorbar(self.image)

        self.axes.set_xlabel(self.scanData.getScanAxis(0, 0))
        try: self.axes.set_ylabel(self.scanData.getScanAxis(1, 0))
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
            self.emit(QtCore.SIGNAL("dataMin"), self._clim[0])
            self.emit(QtCore.SIGNAL("dataMax"), self._clim[1])
        else:
            self.image.set_clim(self._clim)

        self.draw()


class ElementPlotFigure(ElementBaseFigure):

    def __init__(self, scanData, parent=None):
        super(ElementPlotFigure, self).__init__(scanData, parent)

        self._updatePixelMap()

    def _createInitialFigure(self):
        self._elementPlot, = self.axes.plot(self._elementData, 'b')

        self.axes.set_xlabel(self.scanData.getScanAxis(0, 0))
        try: self.axes.set_ylabel(self.scanData.getScanAxis(1, 0))
        except IndexError: pass

    def _updatePixelMap(self):
        xmin, xmax = self.axes.get_xlim()

        data = self.axes.get_lines()[0].get_xdata()

        self.indices = numpy.arange(len(data))
        self.indices.shape = (1, len(data))

        self.xPixelLocs = numpy.linspace(xmin, xmax, len(data))
        self.yPixelLocs = [0]

    def enableAutoscale(self, val):
        self.axes.set_autoscale_on(val)
        self.updateFigure()

    def setDataMax(self, val):
        self._ylims[1]=val
        self.updateFigure()

    def setDataMin(self, val):
        self._ylims[0]=val
        self.updateFigure()

    def updateFigure(self, elementData=None):
        if elementData is None: elementData = self._elementData
        else: self._elementData = elementData

        self._elementPlot.set_ydata(elementData)
        self.axes.relim()
        self.axes.autoscale_view()

        if self.axes.get_autoscale_on():
            self._ylims = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin"), self._ylims[0])
            self.emit(QtCore.SIGNAL("dataMax"), self._ylims[1])
        else:
            self.axes.set_ylim(self._ylims)

        self.draw()


class ElementWidget(QtGui.QWidget):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementWidget, self).__init__(parent)
        self.scanData = scanData

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def connectSignals(self):
        self.connect(self.figure,
                     QtCore.SIGNAL("dataMax"),
                     self.maxSpinBox.setValue)
        self.connect(self.figure,
                     QtCore.SIGNAL("dataMin"),
                     self.minSpinBox.setValue)
        self.connect(self.maxSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.figure.setDataMax)
        self.connect(self.minSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.figure.setDataMin)
        self.connect(self.dataAutoscaleButton,
                     QtCore.SIGNAL("clicked(bool)"),
                     self.figure.enableAutoscale)
        self.connect(self.dataTypeBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.window().setCurrentMapType)
        self.connect(self.window(),
                     QtCore.SIGNAL("elementDataChanged"),
                     self.updateFigure)
        self.connect(self.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.window().setCurrentElement)
        self.connect(self.toolbar,
                     QtCore.SIGNAL("pickEvent"),
                     self.figure.onPick)
        self.connect(self.figure,
                     QtCore.SIGNAL("pickEvent"),
                     self, QtCore.SIGNAL("pickEvent"))

    def setAvailablePeaks(self, peaks):
        self.xrfbandComboBox.clear()
        self.xrfbandComboBox.addItems(peaks)

    def enableInteraction(self):
        pass


class ElementImage(ui_elementsimage.Ui_ElementsImage, ElementWidget):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementImage, self).__init__(scanData, parent)
        self.setupUi(self)

        self.xrfbandComboBox.addItems(self.window().getPeaks())
        self.normalizationComboBox.addItems(scanData.getNormalizationChannels())

        self.figure = ElementImageFigure(scanData, self)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout1.addWidget(self.toolbar, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.figure, 1, 0, 1, 1)

        self.connectSignals()
        self.updateFigure()

    def connectSignals(self):
        ElementWidget.connectSignals(self)
        self.connect(self.interpolationComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setInterpolation)
        self.connect(self.imageOriginComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setImageOrigin)
        self.connect(self.normalizationComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.window().setNormalizationChannel)


class ElementPlot(ui_elementsplot.Ui_ElementsPlot, ElementWidget):
    """Establishes a Experiment controls    """
    def __init__(self, scanData, parent=None):
        super(ElementPlot, self).__init__(scanData, parent)
        self.setupUi(self)

        self.xrfbandComboBox.addItems(self.window().getPeaks())

        self.figure = ElementPlotFigure(scanData, self)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout1.addWidget(self.toolbar, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.figure, 1, 0, 1, 1)

        self.connectSignals()
        self.updateFigure()
