"""

"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import exceptions
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_scanparameterswidget
from xpaxs.instrumentation.spec.scanbounds import ScanBoundsDict
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

    def __init__(self, specRunner, scanBounds=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
#        self.setWindowFlags(QtCore.Qt.WA_DeleteOnClose)

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

    def getDefaultAxes(self):
        raise NotImplementedError


class AScanParameters(ScanParameters):

    _cmd = 'ascan'
    _AxisWidget = scanmotorwidget.AScanMotorWidget

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        axis1 = self.getDefaultAxes()[0]
        layout = self.layout()
        self._axis = self.AxisWidget(specRunner, '', axis1, scanBounds, self)
        layout.addWidget(self._axis)

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend([self._axis.start, self._axis.stop, self._axis.steps])
        return ' '.join(cmdList)

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup("AScanParameters")

        axis = settings.value('axis').toString()
        return [axis]


class A2ScanParameters(AScanParameters):

    _cmd = 'a2scan'

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        axis1, axis2 = self.getDefaultAxes()
        layout = self.layout()
        self._axis1 = self.AxisWidget(
            specRunner, 'Axis 1', axis1, scanBounds, self
        )
        layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(
            specRunner, 'Axis 2', axis2, scanBounds, self
        )
        layout.addWidget(self._axis2)

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

    def _syncSteps(self, val):
        for axis in self._axes:
            axis1.steps = val

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup("A2ScanParameters")

        axis1 = settings.value('axis1').toString()
        axis2 = settings.value('axis2').toString()
        return [axis1, axis2]


class A3ScanParameters(A2ScanParameters):

    _cmd = 'a3scan'

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        axis1, axis2, axis3 = self.getDefaultAxes()
        layout = self.layout()
        self._axis1 = self.AxisWidget(
            specRunner, 'Axis 1', axis1, scanBounds, self
        )
        layout.addWidget(self._axis1)
        self._axis2 = self.AxisWidget(
            specRunner, 'Axis 2', axis2, scanBounds, self
        )
        layout.addWidget(self._axis2)
        self._axis3 = self.AxisWidget(
            specRunner, 'Axis 3', axis3, scanBounds, self
        )
        layout.addWidget(self._axis3)

        self._axes = [self._axis1, self._axis2, self._axis3]

        self._connectSignals()

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend([self._axis1.start, self._axis1.stop])
        cmdList.extend([self._axis2.start, self._axis2.stop])
        cmdList.extend([self._axis3.start, self._axis3.stop, self._axis3.steps])
        return ' '.join(cmdList)

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup("A3ScanParameters")

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
    _AxisWidget = scanmotorwidget.AScanMotorWidget

    def __init__(self, specRunner, scanBounds=None, parent=None):
        ScanParameters.__init__(self, specRunner, scanBounds, parent)

        fastAxis, slowAxis = self.getDefaultAxes()
        layout = self.layout()
        self._fastAxis = self.AxisWidget(
            specRunner, 'fastAxis', fastAxis, scanBounds, self
        )
        layout.addWidget(self._fastAxis)
        self._slowAxis = self.AxisWidget(
            specRunner, 'slowAxis', slowAxis, scanBounds, self
        )
        layout.addWidget(self._slowAxis)

    def getCommand(self):
        cmdList = [self.cmd]
        cmdList.extend(
            [self._fastAxis.start, self._fastAxis.stop, self._fastAxis.steps]
        )
        cmdList.extend(
            [self._slowAxis.start, self._slowAxis.stop, self._slowAxis.steps]
        )
        return ' '.join(cmdList)

    def getDefaultAxes(self):
        settings = QtCore.QSettings()
        settings.beginGroup("MeshParameters")

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
    _scanParametersClasses['ascan'] = AScanParameters
    _scanParametersClasses['a2scan'] = A2ScanParameters
    _scanParametersClasses['a3scan'] = A3ScanParameters
    _scanParametersClasses['dscan'] = DScanParameters
    _scanParametersClasses['d2scan'] = D2ScanParameters
    _scanParametersClasses['d3scan'] = D3ScanParameters
    _scanParametersClasses['mesh'] = MeshParameters
#    _scanParametersClasses['Escan'] = EScanParameters
#    _scanParametersClasses['tseries'] = TSeriesParameters

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner
        self._scanBounds = ScanBoundsDict()

        self.scanTypeComboBox.addItems(sorted(self._scanParametersClasses))
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
    def scanBounds(self):
        return self._scanBounds

    @QtCore.pyqtSignature("")
    def on_pauseButton_clicked(self):
        self.stackedLayout.setCurrentWidget(self.resumeButton)

    @QtCore.pyqtSignature("")
    def on_resumeButton_clicked(self):
        self.stackedLayout.setCurrentWidget(self.pauseButton)

    @QtCore.pyqtSignature("")
    def on_specFileNameEdit_editingFinished(self):
        fullname = str(self.specFileNameEdit.text()).rstrip('.h5').rstrip('.hdf5')
        truncated = os.path.split(fullname)[-1]
        self.specFileNameEdit.setText(truncated)

        self._setSpecFileName(truncated)

    @QtCore.pyqtSignature("")
    def on_scanButton_clicked(self):
        print 'Need to implement scan starting'
        self.scanStarted()

    @QtCore.pyqtSignature("QString")
    def on_scanTypeComboBox_currentIndexChanged(self, val):
        try:
            self._scanParameters.close()
        except AttributeError:
            pass
        ScanParameters = self._scanParametersClasses[str(val)]
        self._scanParameters = ScanParameters(
            self.specRunner, self._scanBounds, self
        )
        self.scanParametersLayout.addWidget(self._scanParameters)

    def _specFileError(self, requested, current):
        exception = SpecfileError(requested, current)

        error = QtGui.QErrorMessage()
        error.showMessage(str(SpecfileError(requested, current)))
        error.exec_()

        raise exception

    def _setSpecFileName(self, filename):
        self.specRunner('newfile %s'%fileName)
        specfile = self.specRunner.getVarVal('DATAFILE')

        specCreated = os.path.split(specfile)[-1]
        if fileName != specCreated:
            self._specFileError(fileName, specfile)

    def scanStarted(self):
        self.scanProgressBar.setValue(0)
        self.stackedLayout.setCurrentWidget(self.scanProgressBar)
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)

    def scanFinished(self):
        self.stackedLayout.setCurrentWidget(self.scanButton)

    @QtCore.pyqtSignature("bool")
    def on_actionPause_triggered(self):
        print 'paused'
        self.actionPause.setVisible(False)
        self.actionResume.setVisible(True)

    @QtCore.pyqtSignature("bool")
    def on_actionResume_triggered(self):
        print 'resumed'
        self.actionPause.setVisible(True)
        self.actionResume.setVisible(False)

    @QtCore.pyqtSignature("bool")
    def on_actionAbort_triggered(self):
        print 'aborted'
        self.stackedLayout.setCurrentWidget(self.scanButton)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
