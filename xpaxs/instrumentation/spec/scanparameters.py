"""

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import exceptions
import gc
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_scanparameterswidget
from xpaxs.instrumentation.spec import scanmotorwidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


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
            self.connect(
                axis,
                QtCore.SIGNAL("motorReady(PyQt_PyObject)"),
                self.scanReady
            )

    def _getAxisWidget(self):
        raise NotImplementedError

    def getScanArgs(self):
        raise NotImplementedError

    def getDefaultAxes(self):
        raise NotImplementedError

    def scanReady(self):
        for axis in self._axes:
            if not axis.motorReady:
                self.emit(QtCore.SIGNAL("scanReady(PyQt_PyObject)"), False)
                return
        self.emit(QtCore.SIGNAL("scanReady(PyQt_PyObject)"), True)


class AScanParameters(ScanParameters):

    _cmd = 'ascan'
    _AxisWidget = scanmotorwidget.AScanMotorWidget

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
            self.connect(
                axis.stepSpinBox,
                QtCore.SIGNAL('valueChanged(int)'),
                self._syncSteps
            )

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
    _AxisWidget = scanmotorwidget.DScanMotorWidget


class D2ScanParameters(A2ScanParameters):

    _cmd = 'd2scan'
    _AxisWidget = scanmotorwidget.DScanMotorWidget


class D3ScanParameters(A3ScanParameters):

    _cmd = 'd3scan'
    _AxisWidget = scanmotorwidget.DScanMotorWidget


class MeshParameters(ScanParameters):

    _cmd = 'mesh'
    _AxisWidget = scanmotorwidget.MeshMotorWidget

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


class EScanParameters(ScanParameters):
    pass


class TSeriesParameters(ScanParameters):
    pass


class ScanParametersWidget(
    ui_scanparameterswidget.Ui_ScanParametersWidget,
    QtGui.QWidget
):

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
#    _scanParametersClasses['Escan'] = EScanParameters
#    _scanParametersClasses['tseries'] = TSeriesParameters

    _scanTypes = \
        ['',
         'ascan', 'a2scan', 'a3scan',
         'dscan', 'd2scan', 'd3scan',
         'mesh'
        ]

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self._specRunner = specRunner
        self.specRunner('clientploton', asynchronous=False)
        self.specRunner('clientdataon', asynchronous=False)

        from xpaxs.instrumentation.spec.scan import QtSpecScanA
        self._scan = QtSpecScanA(self.specRunner.specVersion, parent=self)

        self.connect(
            self._scan,
            QtCore.SIGNAL("newScanLength"),
            self._newScanLength
        )
        self.connect(
            self._scan,
            QtCore.SIGNAL("newScanPoint"),
            self._newScanPoint
        )
        self.connect(
            self._scan,
            QtCore.SIGNAL("scanStarted()"),
            self.scanStarted
        )
        self.connect(
            self._scan,
            QtCore.SIGNAL("scanFinished()"),
            self.scanFinished
        )

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
        self.actionPause.setVisible(False)
        self.actionResume.setVisible(True)
        self.scan.pause()

    @QtCore.pyqtSignature("bool")
    def on_actionResume_triggered(self):
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)
        self.scan.resume()

    @QtCore.pyqtSignature("bool")
    def on_actionAbort_triggered(self):
        self.stackedLayout.setCurrentWidget(self.scanButton)
        self.scan.abort()

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
        args.append(self.integrationTimeSpinBox.value())
        cmd = ' '.join(str(i) for i in args)

        self.scan(cmd)

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

            self.connect(
                self._scanParameters,
                QtCore.SIGNAL("scanReady(PyQt_PyObject)"),
                self.scanButton.setEnabled
            )
            self._scanParameters.scanReady()

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

    def _newScanPoint(self, i):
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

    def scanStarted(self):
        self.stackedLayout.setCurrentWidget(self.scanProgressBar)
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)
        self.scanParamsWidget.setDisabled(True)
        self.emit(QtCore.SIGNAL("specBusy"), True)

    def setBusy(self, busy):
        if not self._scan.isScanning():
            self.scanParamsWidget.setDisabled(busy)
            self.scanButton.setDisabled(busy)

    def scanFinished(self):
        self.stackedLayout.setCurrentWidget(self.scanButton)
        self.scanParamsWidget.setEnabled(True)
        self.emit(QtCore.SIGNAL("specBusy"), False)

    def closeEvent(self, event):
        self.specRunner('clientplotoff', asynchronous=False)
        self.specRunner('clientdataoff', asynchronous=False)

        return event.accept()


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

        self.connect(
            buttonBox,
            QtCore.SIGNAL("accepted()"),
            self,
            QtCore.SLOT("accept()")
        )
        self.connect(
            buttonBox,
            QtCore.SIGNAL("rejected()"),
            self,
            QtCore.SIGNAL("reject()")
        )


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
