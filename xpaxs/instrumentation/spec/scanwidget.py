"""

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import exceptions

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_scanwidget

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


class ScanParameters(QtGui.QWidget):

    _cmd = ''
    _AxisWidget = None

    def __init__(self, specRunner, scanBounds=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)

        self._specRunner = specRunner

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

    @property
    def cmd(self):
        return self._command

    @property
    def AxisWidget(self):
        return self._AxisWidget

    def _getAxisWidget(self):
        raise NotImplementedError

    def getCommand(self):
        raise NotImplementedError


class AScanParameters(ScanParameters):

    _cmd = 'ascan'
    _AxisWidget = AScanMotorWidget

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        layout = self.layout()
        self._axis = self.AxisWidget(specRunner, '', scanBounds[0], self)
        self.layout.addWidget(self._axis)

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend([self._axis.start, self._axis.stop, self._axis.steps])
        return ' '.join(cmdList)


class A2ScanParameters(AScanParameters):

    _cmd = 'a2scan'

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        layout = self.layout()
        self._axis1 = self.AxisWidget(specRunner, 'Axis 1', scanBounds[0], self)
        self.layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(specRunner, 'Axis 2', scanBounds[1], self)
        self.layout.addWidget(self._axis2)

        self._axes = [self._axis1, self._axis2]

        self._connectSignals()

    def _connectSignals(self):
        for axis in self._axes:
            self.connect(
                axis.stepSpinBox,
                QtCore.SIGNAL('valueChanged(int)'),
                self._syncSteps
            )

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend([self._axis1.start, self._axis1.stop])
        cmdList.extend([self._axis2.start, self._axis2.stop, self._axis2.steps])
        return ' '.join(cmdList)

    def syncSteps(self, val):
        for axis in self._axes:
            axis1.steps = val


class A3ScanParameters(A2ScanParameters):

    _cmd = 'a3scan'

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        layout = self.layout()
        self._axis1 = self.AxisWidget(specRunner, 'Axis 1', scanBounds[0], self)
        self.layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(specRunner, 'Axis 2', scanBounds[1], self)
        self.layout.addWidget(self._axis2)
        self._axis3 = self.AxisWidget(specRunner, 'Axis 3', scanBounds[2], self)
        self.layout.addWidget(self._axis3)

        self._axes = [self._axis1, self._axis2, self._axis3]

        self._connectSignals()

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend([self._axis1.start, self._axis1.stop])
        cmdList.extend([self._axis2.start, self._axis2.stop])
        cmdList.extend([self._axis3.start, self._axis3.stop, self._axis3.steps])
        return ' '.join(cmdList)


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
    _AxisWidget = AScanMotorWidget

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        layout = self.layout()
        self._fastAxis = ScanMotorWidget(
            specRunner, 'fastAxis', scanBounds[0], self
        )
        self.layout.addWidget(self._fastAxis)
        self._slowAxis = ScanMotorWidget(
            specRunner, 'slowAxis', scanBounds[1], self
        )
        self.layout.addWidget(self._slowAxis)

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend(
            [self._fastAxis.start, self._fastAxis.stop, self._fastAxis.steps]
        )
        cmdList.extend(
            [self._slowAxis.start, self._slowAxis.stop, self._slowAxis.steps]
        )
        return ' '.join(cmdList)


class EScanParameters(ScanParameters):
    pass


class TSeriesParameters(ScanParameters):
    pass


class ScanWidget(ui_scanwidget.Ui_Dialog, QtGui.QWidget):

    """Dialog for setting spec scan options"""

    _scanParameterClasses = {}
    _scanParametersClasses['ascan'] = AScanParameters
    _scanParametersClasses['a2scan'] = A2ScanParameters
    _scanParametersClasses['a3scan'] = A3ScanParameters
    _scanParametersClasses['dscan'] = DScanParameters
    _scanParametersClasses['d2scan'] = D2ScanParameters
    _scanParametersClasses['d3scan'] = D3ScanParameters
    _scanParametersClasses['mesh'] = MeshParameters
    _scanParametersClasses['Escan'] = EScanParameters
    _scanParametersClasses['tseries'] = TSeriesParameters

    def __init__(self, specRunner, scanBounds=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner
        if scanBounds:
            self._scanBounds = scanBounds
        else:
            raise NotImplementedError

        settings = QtCore.QSettings()
        settings.beginGroup("SpecScanOptions")

        val = os.path.split(self.specRunner.getVarVal('DATAFILE'))[-1]
        self.fileNameEdit.setText(val)

    @QtCore.pyqtSignature("")
    def on_specFileNameEdit_editingFinished(self):
        fullname = str(self.fileNameEdit.text()).rstrip('.h5').rstrip('.hdf5')
        self.fileNameEdit.setText(os.path.split(fullname)[-1])

    @QtCore.pyqtSignature("QString")
    def on_scanTypeComboBox_currentIndexChanged(self, val):
        self._scanParameters.close()
        ScanParameters = self._scanParametersClasses[val]
        self._scanParameters = ScanParameters(
            self.specRunner, self.scanBounds, self
        )
        self.scanParametersLayout.addWidget(self._scanParameters)

    def _specFileError(self, requested, current):
        exception = SpecfileError(requested, current)

        error = QtGui.QErrorMessage()
        error.showMessage(str(SpecfileError(requested, current)))
        error.exec_()

        raise exception

    def _setSpecFileName(self):
        fileName = str(self.fileNameEdit.text())

        self.specRunner('newfile %s'%fileName)
        specfile = self.specRunner.getVarVal('DATAFILE')

        specCreated = os.path.split(specfile)[-1]
        if fileName != specCreated:
            self._specFileError(fileName, specfile)

    def startScan(self):
        self._setSpecFileName()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
