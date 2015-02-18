"""
"""
from __future__ import absolute_import

from PyQt4 import QtCore, QtGui, uic
from matplotlib import rcParams, cm

from .ui import resources


class PlotOptions(QtGui.QGroupBox):

    colorMapChanged = QtCore.pyqtSignal(object)

    def __init__(self, scan_data, figure, parent=None):
        super(PlotOptions, self).__init__(parent)
        uic.loadUi(resources['plotoptions.ui'], self)

        self._figure = figure

        if len(scan_data.entry.acquisition_shape) != 2:
            self.imageSettingsWidget.setVisible(False)

        self._figure.maxValueChanged.connect(self.maxSpinBox.setValue)
        self._figure.minValueChanged.connect(self.minSpinBox.setValue)
        self.maxSpinBox.valueChanged.connect(self._figure.setDataMax)
        self.minSpinBox.valueChanged.connect(self._figure.setDataMin)
        self.dataAutoscaleButton.clicked.connect(self._figure.enableAutoscale)
        try:
            cmaps = sorted(cm._cmapnames)
            self.colorMapComboBox.addItems(cmaps)
            cmap = rcParams['image.cmap']
            self.colorMapComboBox.setCurrentIndex(cmaps.index(cmap))
            self.imageOriginComboBox.currentIndexChanged['QString'].connect(
                self._figure.setImageOrigin
                )
            self.interpolationComboBox.currentIndexChanged['QString'].connect(
                self._figure.setInterpolation
                )
            self.colorMapComboBox.currentIndexChanged['QString'].connect(
                self.setColorMap
                )
            self.reverseColorMapCheckBox.toggled.connect(self.setColorMap)
            self.colorMapChanged.connect(self._figure.setColorMap)
        except AttributeError:
            pass

    def setColorMap(self, val):
        cmap = str(self.colorMapComboBox.currentText())
        if self.reverseColorMapCheckBox.isChecked():
            cmap = cmap + "_r"
        self.colorMapChanged.emit(cm.cmap_d[cmap])

    @QtCore.pyqtSignature("bool")
    def on_dataAutoscaleButton_toggled(self, toggled):
        self.maxSpinBox.setDisabled(toggled)
        self.minSpinBox.setDisabled(toggled)
