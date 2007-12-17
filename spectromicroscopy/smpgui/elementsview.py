"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import mplwidgets, ui_elementsimage, \
    ui_elementsplot

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ElementBaseFigure(mplwidgets.QtMplCanvas):

    """
    """

    def __init__(self, parent=None):
        super(ElementBaseFigure, self).__init__(parent)

        self._xlabel = ''
        self._ylabel = ''
        self._extent = [0, 1, 0, 1]

        self.axes = self.figure.add_subplot(111)

    def setXLabel(self, label):
        self._xlabel = label

    def setXLims(self, lims):
        self._extent[:2] = lims

    def setYLabel(self, label):
        self._ylabel = label

    def setYLims(self, lims):
        self._extent[-2:] = lims

    def setExtent(self, lims):
        self._extent = lims


class ElementImageFigure(ElementBaseFigure):

    autoscale = True

    def __init__(self, parent=None):
        super(ElementImageFigure, self).__init__(parent)

        self._clim = [0, 1]
        self._image = None
        self._elementData = None
        self._colorbar = None

    def _createInitialFigure(self, elementData):
        self._elementData = elementData
        self._image = self.axes.imshow(elementData, extent=self._extent,
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


class ElementPlotFigure(ElementBaseFigure):

    def __init__(self,parent=None):
        super(ElementPlotFigure, self).__init__(parent)

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
            self._extent[2:] = list(self.axes.get_ylim())
            self.emit(QtCore.SIGNAL("dataMin(PyQt_PyObject)"), self._extent[2])
            self.emit(QtCore.SIGNAL("dataMax(PyQt_PyObject)"), self._ylims[3])
        else:
            self.axes.set_ylim(self._extent[2:])

        self.draw()


class ElementWidget(QtGui.QWidget):

    """
    """

    def __init__(self, scan, parent=None):
        super(ElementWidget, self).__init__(parent)
        self.parent = parent
        self._scan = scan

    def __getattr__(self, attr):
        return getattr(self.figure, attr)

    def connectSignals(self):
        self.connect(self.figure,
                     QtCore.SIGNAL("dataMax(PyQt_PyObject)"),
                     self.maxSpinBox.setValue)
        self.connect(self.figure,
                     QtCore.SIGNAL("dataMin(PyQt_PyObject)"),
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
                     self._scan.setCurrentDataType)
        self.connect(self._scan,
                     QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                     self.updateView)
        self.connect(self.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self._scan.setCurrentElement)
        self.connect(self._scan,
                     QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                     self.enableInteraction)
        self.connect(self.saveDataButton,
                     QtCore.SIGNAL("clicked()"),
                     self._scan.saveData)

    def formatFigure(self):
        self.figure.setXLabel(self._scan.getAxisName(0))
        self.figure.setExtent(self._scan.getExtent())
        if self._scan.getScanType() == '2D':
            self.figure.setYLabel(self._scan.getAxisName(1))
        else:
            self.figure.setYLabel('%s'%self.dataTypeBox.currentText())

    def updateView(self, data):
        self.figure.updatePlot(data)

    def viewConcentrations(self, val):
        if self._scan.checkConcentrations():
            self.dataTypeBox.addItem('Mass Fraction')

    def enableInteraction(self):
        pass


class ElementImage(ui_elementsimage.Ui_ElementsImageView, ElementWidget):

    """
    """

    def __init__(self, scan, parent=None):
        super(ElementImage, self).__init__(scan, parent)
        self.setupUi(self)

        self.figure = ElementImageFigure(self)
        self.gridlayout2.addWidget(self.figure, 0, 0, 1, 1)
        self.toolbar = mplwidgets.Toolbar(self.figure, self)
        self.gridlayout2.addWidget(self.toolbar, 1, 0, 1, 1)

        self.formatFigure()
        self.connectSignals()

    def connectSignals(self):
        ElementWidget.connectSignals(self)
        self.connect(self.interpolationComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setInterpolation)
        self.connect(self.imageOriginComboBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.figure.setImageOrigin)


class ElementPlot(ui_elementsplot.Ui_ElementsPlotView, ElementWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, scan, parent=None):
        super(ElementImage, self).__init__(scan, parent)
        self.setupUi(self)

        self._scan = scan

        self.figure = ElementPlotFigure(self)
        self.gridlayout2.addWidget(self.figure, 0, 0, 1, 1)
        self.toolbar = mplwidgets.Toolbar(self.figure, self)
        self.gridlayout2.addWidget(self.toolbar, 1, 0, 1, 1)

        self.formatFigure()
        self.connectSignals()
