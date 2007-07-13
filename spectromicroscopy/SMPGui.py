#!/usr/bin/env python

################################################################################
######################Use this to set the mode of the program###################
DEBUG=0      #if set to 1 it deactivates spec commands
Rollcall=2      #if set to 1 it auto starts spec -s on f3.chess.cornell.edu
                        #and connects if set to 2 it wont autostart but will autoconnect
                        #if set to 3 it will autoconnect and start spec on roll

################################################################################

import os,sys
os.system("pyuic4 SMP.ui>SMP.py")
os.system("pyuic4 Xp.ui>Xp.py")
os.system("pyuic4 GearTester.ui>GearTester.py")
from SpecRunner import SpecRunner
from PyQt4 import QtCore, QtGui    
from SMP import Ui_Main
from MotorGui import MyUI
from KonsoleGui import MyKon
from XpGui import MyXP


class MySMP(Ui_Main,QtGui.QMainWindow):
    """Establishes a Experiment controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.Opener=QtGui.QMenu("New",self.Bar)
        self.Opener.addAction("Motor Control",self.NewMotor)
        self.Opener.addAction("Console",self.NewKon)
        self.NewMotor()
        self.XP=self.NewXP()
        self.NewKon()
        self.Tabby.removeTab(0)
    def NewMotor(self):
        self.Bar.clear()
        self.Bar.addMenu(self.Opener)
        self.Motor=MyUI(self)
        self.Tabby.addTab(self.Motor.centralWidget(),"Motor Controler")
        QtCore.QObject.connect(self.Motor.Closer,QtCore.SIGNAL("clicked()"),\
                                 self.Del)
    
    def NewKon(self):
        self.Kon=MyKon(self)
        self.Tabby.addTab(self.Kon.centralWidget(),"Console")
        QtCore.QObject.connect(self.Kon.Closer,QtCore.SIGNAL("clicked()"),\
                                 self.Del)
    
    def NewXP(self):
        self.XP=MyXP(self)
        self.Tabby.addTab(self.XP.centralWidget(),"Experiment Controls")
    
    def Del(self):
        Index=self.Tabby.currentIndex()
        if self.Tabby.tabText(Index)=="Motor Controler":
            self.Motor=None
        elif self.Tabby.tabText(Index)=="Console":
            self.Kon=None
        self.Tabby.removeTab(Index)
    def get_specrun(self):
        return self.Motor.get_specrun()
        
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MySMP()
    myapp.show()
    sys.exit(app.exec_())
