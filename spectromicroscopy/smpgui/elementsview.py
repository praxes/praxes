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

from spectromicroscopy.smpgui import ui_elementsdata, mplwidgets

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


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


class ElementImageCanvas(ElementCanvas):

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


class ElementPlotCanvas(ElementCanvas):

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


class ElementsImage(ui_elementsdata.Ui_ElementsData, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self.elementDataPlot = mplwidgets.ElementImage(self)
        self.gridlayout2.addWidget(self.elementDataPlot, 0, 0, 1, 1)
        self.elementToolbar = mplwidgets.Toolbar(self.elementDataPlot, self)
        self.gridlayout2.addWidget(self.elementToolbar, 1, 0, 1, 1)
        
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMax(PyQt_PyObject)"),
                     self.maxSpinBox.setValue)
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMin(PyQt_PyObject)"),
                     self.minSpinBox.setValue)
        self.connect(self.maxSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMax)
        self.connect(self.minSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMin)
        self.connect(self.dataAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.elementDataPlot.enableAutoscale)
        self.connect(self.interpolationComboBox, 
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.elementDataPlot.setInterpolation)
        self.connect(self.imageOriginComboBox, 
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.elementDataPlot.setImageOrigin)

    def __getattr__(self, attr):
        return getattr(self.elementDataPlot, attr)


class ElementsPlot(ui_elementsplot.Ui_ElementsPlot, QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self.elementDataPlot = mplwidgets.ElementPlot(self)
        self.gridlayout2.addWidget(self.elementDataPlot, 0, 0, 1, 1)
        self.elementToolbar = mplwidgets.Toolbar(self.elementDataPlot, self)
        self.gridlayout2.addWidget(self.elementToolbar, 1, 0, 1, 1)
        
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMax(PyQt_PyObject)"),
                     self.maxSpinBox.setValue)
        self.connect(self.elementDataPlot,
                     QtCore.SIGNAL("dataMin(PyQt_PyObject)"),
                     self.minSpinBox.setValue)
        self.connect(self.maxSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMax)
        self.connect(self.minSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setDataMin)
        self.connect(self.dataAutoscaleButton, 
                     QtCore.SIGNAL("clicked(bool)"),
                     self.elementDataPlot.enableAutoscale)

    def __getattr__(self, attr):
        return getattr(self.elementDataPlot, attr)
