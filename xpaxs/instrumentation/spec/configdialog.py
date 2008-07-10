#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_motordialog, ui_motorconfig

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.instrumentation.spec.configdialog')


class ConfigDialog(ui_motordialog.Ui_Dialog, QtGui.QDialog):

    """
    """

    def __init__(self, specRunner, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.specRunner = specRunner
        QtCore.QTimer.singleShot(0, self.specConnect)
        self.settings = QtCore.QSettings()
        self.settings.beginGroup('SpecConfig/%s'%specRunner.specVersion)
        self.connect(self.restore, QtCore.SIGNAL("clicked()"), self.reset)
        self.show()

    def reset(self):
        warning=QtGui.QMessageBox.question(self,
                                  "Clear spec configurations",
                                  "This will Clear are personal spec configurations,\
                                  Are you sure you continue?",
                                  QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
        if warning == QtGui.QMessageBox.Cancel:
            pass
        elif warning == QtGui.QMessageBox.Yes:
            logger.warning('Spec Configuration reset')
            self.settings.remove('')
            self.reject()


    def specConnect(self):
        logger.debug('Getting Motors')
        motors = self.specRunner.getMotorsMne()
        progressbar=self.motorProgressBar
        progressbar.setMaximum(len(motors))
        steps=0
        for motorName in motors:
            motorControl=MotorTab(motorName, self)
            self.motorTab.addTab(motorControl,motorName)
            steps+=1
            progressbar.setValue(steps)
        self.motorTab.removeTab(0)
    def  accept(self):
        for i in range(0, self.motorTab.count()):
            self.motorTab.widget(i).setProperties()
        self.settings.endGroup()
        QtGui.QDialog.accept(self)


class MotorTab(ui_motorconfig.Ui_Widget, QtGui.QWidget):
    def __init__(self,motorname,parent):
        QtGui.QWidget.__init__(self, parent)
        self.settings=parent.settings
        self.setupUi(self)
        self.specRunner=parent.specRunner
        try:
            self.motor=self.specRunner.getMotor(motorname)
            logger.debug('aquired motor for tab')
        except:
            logger.error('Could not aquire motor')
            self.__init(motorname.parent)
        self.name=motorname
        self.change={}
        self.ParamDict={'sign':self.signSpin,'offset':self.offsetSpin,'position':self.positionSpin,
                                'low_limit':self.lowerLimitSpin,'high_limit':self.upperLimitSpin,'step_size':self.stepSizeSpin,
                                'acceleration':self.accelSpin,'base_rate':self.baseRateSpin,'backlash':self.backlashSpin,'slew_rate':self.speedSpin}
        self.getProperties()
        self.connectWidgets()

    def connectWidgets(self):
        for Param in self.ParamDict.keys():
            widget=self.ParamDict[Param]
            self.connect(widget,
                         QtCore.SIGNAL('valueChanged(double)'),
                         self.addToChageList)

    def getProperties(self):
        logger.debug('getting %s Properties',self.name)
        for param in self.ParamDict.keys():
            self.ParamDict[param].setValue(self.motor.getParameter(param))

    def addToChageList(self,value):
        widget=self.sender()
        self.change[widget]=value

    def loadPropertiesFromFile(self):
        pass


    def setProperties(self):
        self.settings.beginGroup(self.name)
        for widget in self.change.keys():
            param=widget.accessibleName()
            value=self.change[widget]
            self.settings.setValue('%s'%param, QtCore.QVariant(value))
            self.motor.setParameter("%s"%param,value)
            logger.debug( "%s changed parameter %s to %s",self.name, param,value)
        self.settings.endGroup()

if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ConfigDialog()
    myapp.show()
    sys.exit(app.exec_())
