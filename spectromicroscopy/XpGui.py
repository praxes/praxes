#!/usr/bin/env python
import sys, os, codecs
from os.path import isfile
os.system("pyuic4 Xp.ui>Xp.py")
DEBUG=2

#GUI
from PyQt4 import QtCore, QtGui
from Xp import Ui_XPrun
from SpecRunner import SpecRunner
import numpy
from tempfile import TemporaryFile


class MyXP(Ui_XPrun,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.xprun=SpecRunner(self,DEBUG,"f3.chess.cornell.edu","xrf")
        self.buffer=TemporaryFile( 'w+b')
        if DEBUG!=1:
            QtCore.QObject.connect(self.Mv,
                                   QtCore.SIGNAL("clicked()"),self.Move)
            QtCore.QObject.connect(self.Xname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Yname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Zname, 
                                    QtCore.SIGNAL("editingFinished()"), self.Motor_Connect)
            QtCore.QObject.connect(self.Run,QtCore.SIGNAL("clicked()"),self.run_scan)
        
    def Motor_Connect(self):
        names =["%s"%self.Xname.text(),"%s"%self.Yname.text(),"%s"%self.Zname.text()]
        self.xprun.readmotors(names)
        MotorX=self.xprun.get_motor("%s"%self.Xname.text())
        MotorY=self.xprun.get_motor("%s"%self.Yname.text())
        MotorZ=self.xprun.get_motor("%s"%self.Zname.text())
        self.X=Spinner_Slide_Motor(self.Xslide,self.SpinX,MotorX,self.Xmin,self.Xmax)
        self.Y=Spinner_Slide_Motor(self.Yslide,self.SpinY,MotorY,self.Ymin,self.Ymax)
        self.Z=Spinner_Slide_Motor(self.Zslide,self.SpinZ,MotorZ,self.Zmin,self.Zmax)


    def Move(self):
        self.X.move()
        self.Y.move()
        self.Z.move()
    
    def run_scan(self):
        self.data=numpy.memmap(self.buffer.name,dtype=float,mode='w+',shape=(5,2048))
        self.xprun.exc("SetMon")
        self.xprun.set_var('MCA_DATA_BUFFER')
        self.xprun.set_cmd("tseries 5 1")
        self.xprun.run_cmd()
        while not self.xprun.get_cmd_reply():
            self.xprun.update()
            (value,index,actual)=self.xprun.get_values()
            if actual:
                i=0
                print index
                for i in range(2048):
                    self.data[index,i]=value[0][i]
                    i+=1
        print "data collected"
        print self.data
        for i in range(5):
            n=input("col number")
            print i, self.data[4][n]


class Spinner_Slide_Motor:
    def __init__(self,Slide,Spin, Motor,Min,Max):
        self.Spin=Spin
        self.Slide=Slide
        self.Motor=Motor
        self.Min=Min
        self.Max=Max
        QtCore.QObject.connect(self.Slide,QtCore.SIGNAL("sliderReleased()"),
                               self.slide)
        QtCore.QObject.connect(self.Spin,
                               QtCore.SIGNAL("editingFinished()"),self.spin)
        self.get_params()
        self.run()
    def get_params(self):
        self.values=[]
        params=['position','offset','sign',"low_limit","high_limit","step_size"]
        for param in params:
            try: 
                self.values.append(self.Motor.getParameter(param))
            except:
                self.values.append("unable to get value")
            
    def run(self):
        values=self.values
        min =values[2]*values[3]+values[1]
        max=values[2]*values[4]+values[1]
        self.Max.setRange(min,max)
        self.Min.setRange(min,max)
        self.Max.setValue(max)
        self.Min.setValue(min)
        self.Spin.setRange(min,max)
        self.Slide.setRange(min*values[5],max*values[5])
        self.Spin.setValue(self.values[0])
        self.Slide.setTickInterval(20*values[5])
        self.spin()
    def slide(self):
        self.Spin.setValue(self.Slide.value()/self.values[5])
    def spin(self):
        self.Slide.setValue(self.Spin.value()*self.values[5])
    def Move(self):
        self.self.Motor.move(self.Spin.getValue()-self.values[1])
        


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
