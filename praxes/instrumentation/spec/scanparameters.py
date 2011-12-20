"""
"""
import exceptions
import gc
import os

from PyQt4 import QtCore, QtGui

from .ui.ui_scanparameterswidget import Ui_ScanParametersWidget
from .scan import QtSpecScanA
from .scanmotorwidget import (
    AScanMotorWidget, DScanMotorWidget, MeshMotorWidget
    )


class SpecfileError(exceptions.Exception):

    def __init__(self, requested, current):
        self._requested = requested
        self._current = current

    def __str__(self):
        str = 'Spec was unable to create the requested file: %s. Perhaps there \
            is a permissions issue. The current spec file is %s".'\
            %(self._requested, self._current)
        return str


# TODO: default to previous motors using QSettings
class ScanParameters(QtGui.QWidget):

    _cmd = ''
    _AxisWidget = None

    scanReady = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self._axes = []

    @property
    def AxisWidget(self):
        return self._AxisWidget

    @property
    def cmd(self):
        return self._command

    def _connectSignals(self):
        for axis in self._axes:
            axis.motorReady.connect(self.checkScanReady)

    def _getAxisWidget(self):
        raise NotImplementedError

    def getScanArgs(self):
        raise NotImplementedError

    def getDefaultAxes(self):
        raise NotImplementedError

    def checkScanReady(self):
        for axis in self._axes:
            if not axis.isReady:
                self.scanReady.emit(False)
                return
        self.scanReady.emit(True)


class AScanParameters(ScanParameters):

    _cmd = 'ascan'
    _AxisWidget = AScanMotorWidget

    def __init__(self, specRunner, parent=None):
        ScanParameters.__init__(self, parent)

        axis = self.getDefaultAxes()[0]
        layout = self.layout()
        self._axis = self.AxisWidget(specRunner, '', axis, self)
        layout.addWidget(self._axis)

        self._axes = [self._axis]

        self._connectSignals()

    def getScanArgs(self):
        args = [self._cmd]
        args.extend(self._axis.getScanArgs(steps=True))
        return args

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))

        axis = settings.value('axis').toString()
        return [axis]


class A2ScanParameters(AScanParameters):

    _cmd = 'a2scan'

    def __init__(self, specRunner, parent=None):
        ScanParameters.__init__(self, parent)

        axis1, axis2 = self.getDefaultAxes()
        layout = self.layout()
        self._axis1 = self.AxisWidget(specRunner, 'Axis 1', axis1, self)
        layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(specRunner, 'Axis 2', axis2, self)
        layout.addWidget(self._axis2)

        self._axes = [self._axis1, self._axis2]

        self._connectSignals()

    def _connectSignals(self):
        AScanParameters._connectSignals(self)
        for axis in self._axes:
            axis.stepSpinBox.valueChanged[int].connect(self._syncSteps)

    def getScanArgs(self):
        args = [self._cmd]
        args.extend(self._axis1.getScanArgs(steps=False))
        args.extend(self._axis2.getScanArgs(steps=True))
        return args

    def _syncSteps(self, val):
        for axis in self._axes:
            axis.stepSpinBox.setValue(val)

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))

        axis1 = settings.value('axis1').toString()
        axis2 = settings.value('axis2').toString()
        return [axis1, axis2]


class A3ScanParameters(A2ScanParameters):

    _cmd = 'a3scan'

    def __init__(self, specRunner, parent=None):
        ScanParameters.__init__(self, parent)

        axis1, axis2, axis3 = self.getDefaultAxes()
        layout = self.layout()
        self._axis1 = self.AxisWidget(specRunner, 'Axis 1', axis1, self)
        layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(specRunner, 'Axis 2', axis2, self)
        layout.addWidget(self._axis2)
        self._axis3 = self.AxisWidget(specRunner, 'Axis 3', axis3, self)
        layout.addWidget(self._axis3)

        self._axes = [self._axis1, self._axis2, self._axis3]

        self._connectSignals()

    def getScanArgs(self):
        args = [self._cmd]
        args.extend(self._axis1.getScanArgs(steps=False))
        args.extend(self._axis2.getScanArgs(steps=False))
        args.extend(self._axis3.getScanArgs(steps=True))
        return args

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))

        axis1 = settings.value('axis1').toString()
        axis2 = settings.value('axis2').toString()
        axis3 = settings.value('axis3').toString()
        return [axis1, axis2, axis3]


class DScanParameters(AScanParameters):

    _cmd = 'dscan'
    _AxisWidget = DScanMotorWidget


class D2ScanParameters(A2ScanParameters):

    _cmd = 'd2scan'
    _AxisWidget = DScanMotorWidget


class D3ScanParameters(A3ScanParameters):

    _cmd = 'd3scan'
    _AxisWidget = DScanMotorWidget


class MeshParameters(ScanParameters):

    _cmd = 'mesh'
    _AxisWidget = MeshMotorWidget

    def __init__(self, specRunner, parent=None):
        ScanParameters.__init__(self, parent)

        fastAxis, slowAxis = self.getDefaultAxes()
        layout = self.layout()
        self._fastAxis = self.AxisWidget(specRunner, 'fastAxis', fastAxis, self)
        layout.addWidget(self._fastAxis)
        self._slowAxis = self.AxisWidget(specRunner, 'slowAxis', slowAxis, self)
        layout.addWidget(self._slowAxis)

        self._connectSignals()

    def getScanArgs(self):
        args = [self._cmd]
        args.extend(self._fastAxis.getScanArgs(steps=True))
        args.extend(self._slowAxis.getScanArgs(steps=True))
        return args

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup(str(self.__class__))

        slowAxis = settings.value('slowAxis').toString()
        fastAxis = settings.value('fastAxis').toString()
        return [fastAxis, slowAxis]


class ZZMeshParameters(MeshParameters):
    _cmd = 'zzmesh'


class EScanParameters(ScanParameters):
    pass


class TSeriesParameters(ScanParameters):
    pass


class ScanParametersWidget(Ui_ScanParametersWidget, QtGui.QWidget):

    """Dialog for setting spec scan options"""

    _scanParametersClasses = {}
    _scanParametersClasses[''] = None
    _scanParametersClasses['ascan'] = AScanParameters
    _scanParametersClasses['a2scan'] = A2ScanParameters
    _scanParametersClasses['a3scan'] = A3ScanParameters
    _scanParametersClasses['dscan'] = DScanParameters
    _scanParametersClasses['d2scan'] = D2ScanParameters
    _scanParametersClasses['d3scan'] = D3ScanParameters
    _scanParametersClasses['mesh'] = MeshParameters
    _scanParametersClasses['zzmesh'] = ZZMeshParameters
#    _scanParametersClasses['Escan'] = EScanParameters
#    _scanParametersClasses['tseries'] = TSeriesParameters

    _scanTypes = \
        ['',
         'ascan', 'a2scan', 'a3scan',
         'dscan', 'd2scan', 'd3scan',
         'mesh', 'zzmesh'
        ]

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self._specRunner = specRunner

        self._scan = QtSpecScanA(self.specRunner.specVersion, parent=self)
        self._scan.scanLength.connect(self._newScanLength)
        self._scan.scanData.connect(self._newScanData)
        self._scan.started.connect(self.scanStarted)
        self._scan.paused.connect(self.scanPaused)
        self._scan.resumed.connect(self.scanResumed)
        self._scan.finished.connect(self.scanFinished)

        self.scanTypeComboBox.addItems(self._scanTypes)

        settings = QtCore.QSettings()
        settings.beginGroup("ScanParameters")
        scantype = settings.value('ScanType').toString()
        i = self.scanTypeComboBox.findText(scantype)
        if i != -1:
            self.scanTypeComboBox.setCurrentIndex(i)

        self.scanProgressBar.addActions(
            [self.actionPause, self.actionResume, self.actionAbort]
        )

        self.stackedLayout = QtGui.QStackedLayout(self.scanProgressFrame)
        self.stackedLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedLayout.addWidget(self.scanButton)
        self.stackedLayout.addWidget(self.scanProgressBar)

        val = os.path.split(self.specRunner.getVarVal('DATAFILE'))[-1]
        self.specFileNameEdit.setText(val)

    @property
    def scan(self):
        return self._scan

    @property
    def specRunner(self):
        return self._specRunner

    @QtCore.pyqtSignature("bool")
    def on_actionPause_triggered(self):
        self._scan.pause()

    @QtCore.pyqtSignature("bool")
    def on_actionResume_triggered(self):
        self._scan.resume()

    @QtCore.pyqtSignature("bool")
    def on_actionAbort_triggered(self):
        self._scan.abort()

    @QtCore.pyqtSignature("")
    def on_specFileNameEdit_editingFinished(self):
        fullname = str(self.specFileNameEdit.text()).rstrip('.h5').rstrip('.hdf5')
        newFile = fullname.split(os.path.sep)[-1]

        oldFile = self.specRunner.getVarVal('DATAFILE')
        if oldFile != newFile:
            if ChangeSpecFileDialog(oldFile, newFile).exec_():
                self._setSpecFileName(newFile)

    @QtCore.pyqtSignature("")
    def on_scanButton_clicked(self):
        args = self._scanParameters.getScanArgs()
        if not isinstance(self._scanParameters, ZZMeshParameters):
            args.append(self.integrationTimeSpinBox.value())
        cmd = ' '.join(str(i) for i in args)

        self._scan(cmd)

    @QtCore.pyqtSignature("QString")
    def on_scanTypeComboBox_currentIndexChanged(self, val):
        try:
            self._scanParameters.close()
        except AttributeError:
            pass
        ScanParameters = self._scanParametersClasses[str(val)]
        if ScanParameters:
            self._scanParameters = ScanParameters(self.specRunner, self)
            self.scanParametersLayout.addWidget(self._scanParameters)

            self._scanParameters.scanReady.connect(self.scanButton.setEnabled)
            self._scanParameters.checkScanReady()

            settings = QtCore.QSettings()
            settings.beginGroup("ScanParameters")
            settings.setValue(
                'ScanType',
                QtCore.QVariant(self.scanTypeComboBox.currentText())
            )
        else:
            self.scanButton.setEnabled(False)

    def _newScanLength(self, length):
        self.scanProgressBar.setValue(0)
        self.scanProgressBar.setMaximum(int(length)-1)

    def _newScanData(self, i):
        self.scanProgressBar.setValue(i+1)

    def _specFileError(self, requested, current):
        exception = SpecfileError(requested, current)

        error = QtGui.QErrorMessage()
        error.showMessage(str(SpecfileError(requested, current)))
        error.exec_()

        raise exception

    def _setSpecFileName(self, fileName):
        self.specRunner('newfile %s'%fileName, asynchronous=False)
        specCreated = self.specRunner.getVarVal('DATAFILE')

        if fileName != specCreated:
            self._specFileError(fileName, specCreated)

        self.specFileNameEdit.setText(specCreated)

    def scanPaused(self):
        self.actionPause.setVisible(False)
        self.actionResume.setVisible(True)

    def scanResumed(self):
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)

    def scanStarted(self):
        self.stackedLayout.setCurrentWidget(self.scanProgressBar)
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)
        self.scanParamsWidget.setDisabled(True)

    def scanFinished(self):
        self.stackedLayout.setCurrentWidget(self.scanButton)
        self.scanParamsWidget.setEnabled(True)


class ChangeSpecFileDialog(QtGui.QDialog):

    def __init__(self, old, new, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowTitle("Spec Data File")

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        msg = """Change spec datafile from "%s" to "%s"?
(the new file will be created in spec's current working directory)"""%(old, new)
        label = QtGui.QLabel(msg)
        layout.addWidget(label)

        buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
        )
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Praxes')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
