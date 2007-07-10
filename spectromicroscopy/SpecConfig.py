import codecs
import sys,os
os.system("pyuic4 SpecSetter.ui>SpecSetter.py")
print "on"
from PyQt4 import QtGui, QtCore
from SpecSetter import Ui_SpecSetter 
class SpecConfig(QtGui.QWidget,Ui_SpecSetter):
    
    __pyqtSignals__ =("configChanged()")
    
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        print "setup"
        self.stdout=self
        self._Master=''
        self.Names=[]
        QtCore.QObject.connect(self.Setter, QtCore.SIGNAL("clicked()"),
                               self.set)
        QtCote.QObject.connect(self.Complie, QtCore.SIGNAL("clicked()"),
                                self.Create)
    def set(self):
        Accel=self.Accel.getValue()
        BR=self.BR.getValue()
        BLash=self.Blash.getValue()
        LL=self.LL.getValue()
        Name=self.Name.getText()
        Sign=self.Sign.getValue()
        Speed=self.Speed.getValue()
        UL=self.UL.getValue()
        offset=self.Offset.getValue()
        SS=self.StepSize.getValue()
        Motor=MotorConfig(Name,SS,Speed,BR,Accel,Blash,LL,UL,Sign,Offset)
        self.Names.append(name)
        if Name is self.Names:
            i=find(self.Names,Name)
            self.Motors[i]=Motor
        else:
            self.Motors.append(Motor)
        
    def write(self,string):
        self._Master.append(string)
        
    def Create(self):
        Commands=''
        for motor in self.Motors:
            Commands.append(motor.get_string())
        print "#!/usr/bin/env/python"
        print "\n import os"
        print "Command_string='%s'"%Commands
        print "\n os.system('killall spec')"
        print "\n os.system('spec')"
        print "\n for cmd in Command_string.split(';'):"
        print "\n    os.system(cmd)"
        print "\n os.system('exit')"
        s = codecs.open("Config",'w','utf-8')
        s.write(self._Master)
        s.close()
        

class MotorConfig:
    def __init__(self,name,ss,ssr,br,at,blash,ll,ul,sign,offset):        
        self.stdout=self
        s=["step_size", "acceleration", "base_rate", "velocity", "backlash"]
        sv =[ss,at,br,ssr,blash]
        for i in range(len(s)):
            print "motor_par(%s"%name
            print ", %s"%s[i]
            print "[, %s];"%sv[i]
        print "set_lim(%s"%name
        print ", "+ll+", "+ul+");"
        print "chg_offset(%s"%name
        print ", "+offset+");"
        #cannot fing command to set sign

    def write(self,string):
        self._cmdstring.append(string)
    
    def get_string(self):
        return self._cmdstring


class SpecConfigPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent = None):
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self)
        self.initialized = False        
    def initialize(self, core):
        if self.initialized:
            return 
        self.initialized = True
    def isInitialized(self):
        return self.initialized
    def createWidget(self, parent):
        return SpecConfig(parent)
    def name(self):
        return "SpecConfig"
    def group(self):
        return "PyQt Examples"
    def icon(self):
        return QtGui.QIcon(_logo_pixmap)
    def toolTip(self):
        return ""
    def whatsThis(self):
        return ""
    def isContainer(self):
        return True
    def includeFile(self):
        return "SpecSetter"
    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SpecConfig()
    myapp.show()
    sys.exit(app.exec_())
