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


class ElementsData(ui_elementsdata.Ui_ElementsData, QtGui.QWidget):
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
        self.connect(self.interpolationComboBox, 
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.elementDataPlot.setImageOrigin)

    def __getattr__(self, attr):
        return getattr(self.elementDataPlot, attr)
