"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



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


class ElementBaseFigure(plotwidgets.QtMplCanvas):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementBaseFigure, self).__init__(parent)

        self.scanData = scanData
        self.autoscale = True

        self.axes = self.figure.add_subplot(111)

        self._elementData = self.window().getElementMap()
        self._createInitialFigure()

        self.connect(self.scanData,
                     QtCore.SIGNAL("elementDataChanged"),
                     self.updateFigure)

    def _createInitialFigure(self):
        raise NotImplementedError

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

        cursor = plotwidgets.ImageCursor(self.image, useblit=True, parent=self, color='w')
        self.connect(cursor, QtCore.SIGNAL('pickEvent'), self.window().plotSpectrum)

        min, max = self._elementData.min(), self._elementData.max()
        self._clim = [min, max or float(max==0)]

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

        xlim = self.scanData.getScanRange(self.scanData.getScanAxis(0, 0))
        ylim = self.scanData.getScanRange(self.scanData.getScanAxis(1, 0))
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

        self.draw()


class ElementPlotFigure(ElementBaseFigure):

    def __init__(self, scanData, parent=None):
        super(ElementPlotFigure, self).__init__(scanData, parent)

    def _createInitialFigure(self, elementData):
        self._elementPlot, = self.axes.plot(self._elementData, 'b')

        self.axes.set_xlabel(self.scanData.getScanAxis(0, 0))
        try: self.axes.set_ylabel(self.scanData.getScanAxis(1, 0))
        except IndexError: pass

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
        if elementData is None: elementData = self._elementData
        else: self._elementData = elementData

        self._elementPlot.set_ydata(elementData)
        self.axes.relim()
        self.axes.autoscale_view()

        if self.axes.get_autoscale_on():
            self._extent[2:] = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin"), self._extent[2])
            self.emit(QtCore.SIGNAL("dataMax"), self._ylims[3])
        else:
            self.axes.set_ylim(self._extent[2:])

        self.draw()


class ElementWidget(QtGui.QWidget):

    """
    """

    def __init__(self, scanData, parent=None):
        super(ElementWidget, self).__init__(parent)
        self.setParent(parent)
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
        self.connect(self.scanData,
                     QtCore.SIGNAL("enableDataInteraction"),
                     self.enableInteraction)

    def setAvailablePeaks(self, peaks):
        self.xrfbandComboBox.clear()
        self.xrfbandComboBox.addItems(peaks)

#    def formatFigure(self):
#        self.figure.setXLabel(self.scanData.getScanAxis(0, 0))
#        try:
#            self.figure.setYLabel(self.scanData.getScanAxis(1, 0))
#        except IndexError:
#            self.figure.setYLabel('%s'%self.dataTypeBox.currentText())

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
    """Establishes a Experimenbt controls    """
    def __init__(self, scanData, parent=None):
        super(ElementPlot, self).__init__(scanData, parent)
        self.setupUi(self)

        self.xrfbandComboBox.addItems(scanData.getPeaks())

        self.figure = ElementPlotFigure(scanData, self)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout1.addWidget(self.toolbar, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.figure, 1, 0, 1, 1)

        self.connectSignals()
        self.updateFigure()
