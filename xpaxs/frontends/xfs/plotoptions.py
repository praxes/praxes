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

from xpaxs.frontends.xfs.ui.ui_plotoptions import Ui_PlotOptions

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class PlotOptions(Ui_PlotOptions, QtGui.QWidget):

    def __init__(self, scanData, figure, parent=None):
        super(PlotOptions, self).__init__(parent)
        self.setupUi(self)

        self._figure = figure

        if scanData.getNumScanDimensions() != 2:
            self.imageSettingsWidget.setVisible(False)

        self.connect(
            self._figure,
            QtCore.SIGNAL("maxValueChanged"),
            self.maxSpinBox.setValue
        )
        self.connect(
            self._figure,
            QtCore.SIGNAL("minValueChanged"),
            self.minSpinBox.setValue
        )
        self.connect(
            self.maxSpinBox,
            QtCore.SIGNAL("valueChanged(double)"),
            self._figure.setDataMax
        )
        self.connect(
            self.minSpinBox,
            QtCore.SIGNAL("valueChanged(double)"),
            self._figure.setDataMin
        )
        self.connect(
            self.dataAutoscaleButton,
            QtCore.SIGNAL("clicked(bool)"),
            self._figure.enableAutoscale
        )
        self.connect(
            self.imageOriginComboBox,
            QtCore.SIGNAL("currentIndexChanged(QString)"),
            self._figure.setImageOrigin
        )
        self.connect(
            self.interpolationComboBox,
            QtCore.SIGNAL("currentIndexChanged(QString)"),
            self._figure.setInterpolation
        )

    @QtCore.pyqtSignature("bool")
    def on_dataAutoscaleButton_toggled(self, toggled):
        self.maxSpinBox.setDisabled(toggled)
        self.minSpinBox.setDisabled(toggled)
