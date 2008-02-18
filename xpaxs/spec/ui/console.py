#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import codecs
import os
import pexpect
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from SpecClient import Spec, SpecMotor

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

import ui_console, ui_motorconfig

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------

class Console(ui_console.Ui_Kontrol, QtGui.QMainWindow):

    """Establishes a custom Console for interacting with the Computer"""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.runButton,
                     QtCore.SIGNAL("clicked()"),
                     self.run)
        self.connect(self.macroSaveButton,
                     QtCore.SIGNAL("clicked()"),
                     self.macroSave)
        self.connect(self.changeDirButton,
                     QtCore.SIGNAL("clicked()"),
                     self.changeDir)
        self.connect(self.dirLineEdit,
                     QtCore.SIGNAL("editingFinnished()"),
                     self.manualChangeDir)
        self.connect(self.specConnectButton,
                     QtCore.SIGNAL('clicked()'),
                     self.specConnect)

    def macroSave(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        s = codecs.open(self.filename,'w','utf-8')
        s.write(unicode(self.textEditKonsole.toPlainText()))
        s.close()

    def changeDir(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.path = "%s"%fd.getExistingDirectory()
            os.chdir(self.path)
            self.dirLineEdit.setText(self.path)
        except: 
            os.system("dir")
    def manualChangeDir(self,dir):
        try:
            os.chdir(dir)
            self.path=dir
        except:
            self.changeDir()

    def run(self):
        self.textDisplay.append(">>>"+self.textEditKonsole.toPlainText())
        Kommands=self.textEditKonsole.toPlainText().split(";")
        for i in range(len(Kommands)):
            Kommand="%s"%Kommands[i]
            doingit=pexpect.run(Kommand)
            self.textDisplay.append(doingit)

    def specConnect(self):
        server='%s'%self.specServerEdit.text()
        port='%s'%self.specPortEdit.text()
        self.specVersion=server+":"+port
#        self.specVersion='roll.chess.cornell.edu:spec'
        self.Motornames=[]
        try:
            spec=Spec.Spec(self.specVersion,500)
            self.Motornames=spec.getMotorsMne() 
            #self.specServerEdit.setReadOnly(True)
            self.specServerEdit.setDisabled(True)
            #self.specPortEdit.setReadOnly(True)
            self.specPortEdit.setDisabled(True)
        except:
           self.specServerEdit.clear()
           self.specPortEdit.clear()
        for i in self.Motornames:
            motorcontrol=MotorTab(self.Motornames[i].keys()[0],self.specVersion, self.motorTab)
            self.motorTab.addTab(motorcontrol,self.Motornames[i].keys()[0])
        self.motorTab.removeTab(0)
        


    


#-----------------------------------------------------------------
# Motor Tab Code
#-----------------------------------------------------------------

ParameterList=['sign','offset','position','low_limit','high_limit','step_size',
               'acceleration','base_rate','backlash','slew_rate']

class MotorTab(ui_motorconfig.Ui_Widget, QtGui.QWidget):
    def __init__(self,motorname,specVersion,parent=None ):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.motor=SpecMotor.SpecMotorA(motorname,specVersion)
        self.name=motorname
        self.WidgetList=[self.signSpin,self.offsetSpin,self.positionSpin,
            self.lowerLimitSpin,self.upperLimitSpin,self.stepSizeSpin,
            self.accelSpin,self.baseRateSpin,self.backlashSpin,self.speedSpin]
        self.getProperties()
        #self.connectWidgets()
        

        
    def connectWidgets(self):
        for widget in self.WidgetList:
            self.connect(widget,
                         QtCore.SIGNAL('valueChanged(int)'),
                         self.setProperties())
    def getProperties(self):
#        self.stepSizeSpin.setValue(self.motor.getParameter('slew_rate'))
        for i in range(0, len(self.WidgetList)):
            self.WidgetList[i].setValue(self.motor.getParameter(ParameterList[i]))
        
    def setProperties(self):
        for i in range(0, len(self.WidgetList)):
            self.motor.setParameter(ParameterList[i],self.WidgetList[i].getValue())
    
            
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = Console()
    myapp.show()
    sys.exit(app.exec_())
