"""
"""
from __future__ import absolute_import

from PyQt4 import QtCore, QtGui

from .ui.ui_plotoptions import Ui_PlotOptions


class PlotOptions(Ui_PlotOptions, QtGui.QGroupBox):

    def __init__(self, scan_data, figure, parent=None):
        super(PlotOptions, self).__init__(parent)
        self.setupUi(self)

        self._figure = figure

        if len(scan_data.acquisition_shape) != 2:
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
        try:
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
        except AttributeError:
            pass

    @QtCore.pyqtSignature("bool")
    def on_dataAutoscaleButton_toggled(self, toggled):
        self.maxSpinBox.setDisabled(toggled)
        self.minSpinBox.setDisabled(toggled)
