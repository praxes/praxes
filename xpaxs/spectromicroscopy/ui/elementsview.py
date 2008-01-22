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

    def __init__(self, controller, parent=None):
        super(ElementBaseFigure, self).__init__(parent)

        self.controller = controller

        self.axes = self.figure.add_subplot(111)
        self._elementData = numpy.zeros(self.controller.getScanShape(), 'f')
        self._createInitialFigure()

        self.connect(self.controller,
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

    autoscale = True

    def __init__(self, controller, parent=None):
        super(ElementImageFigure, self).__init__(controller, parent)

        self._clim = [0, 1]

    def _createInitialFigure(self):
        extent = []
        xlim = self.controller.getScanRange(self.controller.getScanAxis(0, 0))
        extent.extend(xlim)
        ylim = self.controller.getScanRange(self.controller.getScanAxis(1, 0))
        extent.extend(ylim)
        self._image = self.axes.imshow(self._elementData, extent=extent,
                                       aspect=1/1.414, interpolation='nearest',
                                       origin='lower')
        self._colorbar = self.figure.colorbar(self._image)

        self.axes.set_xlabel(self.controller.getScanAxis(0, 0))
        try: self.axes.set_ylabel(self.controller.getScanAxis(1, 0))
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


class ElementPlotFigure(ElementBaseFigure):

    def __init__(self, controller, parent=None):
        super(ElementPlotFigure, self).__init__(controller, parent)

        self._elementData = None
        self._autoscale = True

    def _createInitialFigure(self, elementData):
        self._elementPlot, = self.axes.plot(self._elementData, 'b')

        self.axes.set_xlabel(self.controller.getScanAxis(0, 0))
        try: self.axes.set_ylabel(self.controller.getScanAxis(1, 0))
        except IndexError: pass

    def enableAutoscale(self, val):
        self.axes.enable_autoscale_on(val)
        self.updateFigure()

#    def setDataMax(self, val):
#        self._ylims[1]=val
#        self.updateFigure()
#
#    def setDataMin(self, val):
#        self._ylims[0]=val
#        self.updateFigure()

    def updateFigure(self, elementData=None):
        if elementData is None: elementData = self._elementData
        else: self._elementData = elementData

        self._elementPlot.set_ydata(elementData)
        self.axes.relim()
        self.axes.autoscale_view()

#        if self.axes.get_autoscale_on():
#            self._extent[2:] = list(self.axes.get_ylim())
#            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._extent[2])
#            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._ylims[3])
#        else:
#            self.axes.set_ylim(self._extent[2:])

        self.draw()


class ElementWidget(QtGui.QWidget):

    """
    """

    def __init__(self, controller, parent=None):
        super(ElementWidget, self).__init__(parent)
        self.parent = parent
        self.controller = controller

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def connectSignals(self):
#        self.connect(self.maxSpinBox,
#                     QtCore.SIGNAL("valueChanged(double)"),
#                     self.figure.setDataMax)
#        self.connect(self.minSpinBox,
#                     QtCore.SIGNAL("valueChanged(double)"),
#                     self.figure.setDataMin)
        self.connect(self.dataAutoscaleButton,
                     QtCore.SIGNAL("clicked(bool)"),
                     self.figure.enableAutoscale)
        self.connect(self.dataTypeBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.controller.setCurrentDataType)
        self.connect(self.controller,
                     QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                     self.updateView)
        self.connect(self.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.controller.setCurrentElement)
        self.connect(self.controller,
                     QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                     self.enableInteraction)
        self.connect(self.saveDataButton,
                     QtCore.SIGNAL("clicked()"),
                     self.controller.saveData)

#    def formatFigure(self):
#        self.figure.setXLabel(self.controller.getScanAxis(0, 0))
#        try:
#            self.figure.setYLabel(self.controller.getScanAxis(1, 0))
#        except IndexError:
#            self.figure.setYLabel('%s'%self.dataTypeBox.currentText())

    def updateView(self, data):
        self.figure.updateFigure(data)

    def viewConcentrations(self, val):
        if self.controller.checkConcentrations():
            self.dataTypeBox.addItem('Mass Fraction')
            self.controller.setCurrentDataType('Mass Fraction')

    def enableInteraction(self):
        pass


class ElementImage(ui_elementsimage.Ui_ElementsImage, ElementWidget):

    """
    """

    def __init__(self, controller, parent=None):
        super(ElementImage, self).__init__(controller, parent)
        self.setupUi(self)

        self.xrfbandComboBox.addItems(controller.getPeaks())
        self.normalizationComboBox.addItems(controller.getNormalizationChannels())

        self.figure = ElementImageFigure(controller, self)
        self.gridlayout2.addWidget(self.figure, 0, 0, 1, 1)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout2.addWidget(self.toolbar, 1, 0, 1, 1)

        self.connectSignals()

    def connectSignals(self):
        ElementWidget.connectSignals(self)
#        self.connect(self.figure,
#                     QtCore.SIGNAL("dataMax(PyQt_PyObject)"),
#                     self.maxSpinBox.setValue)
#        self.connect(self.figure,
#                     QtCore.SIGNAL("dataMin(PyQt_PyObject)"),
#                     self.minSpinBox.setValue)
        self.connect(self.interpolationComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setInterpolation)
        self.connect(self.imageOriginComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setImageOrigin)
        self.connect(self.normalizationComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.controller.setNormalizationChannel)


class ElementPlot(ui_elementsplot.Ui_ElementsPlot, ElementWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, controller, parent=None):
        super(ElementPlot, self).__init__(controller, parent)
        self.setupUi(self)

        self.xrfbandComboBox.addItems(controller.getPeaks())

        self.figure = ElementPlotFigure(controller, self)
        self.gridlayout2.addWidget(self.figure, 0, 0, 1, 1)
        self.toolbar = plotwidgets.Toolbar(self.figure, self)
        self.gridlayout2.addWidget(self.toolbar, 1, 0, 1, 1)

        self.connectSignals()
