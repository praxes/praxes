#!/usr/bin/env python
import sys, os, codecs
from os.path import isfile
os.system("pyuic4 XpSetup.ui>XpSetup.py")
DEBUG=2

#GUI
from PyQt4 import QtCore, QtGui
from XpSetup import Ui_XpSetter
from SpecRunner import SpecRunner

class MyXP(Ui_XpSetter,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        self.setupUi(self)
        self.ScanBox.addItem("tseries")
        self.ScanBox.addItem("mesh")
        self.xprun=SpecRunner(self,DEBUG,"f3.chess.cornell.edu","xrf")
        self.Motor_Connect()
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
        self.xprun.readmotors(names,"Async")
        MotorX=self.xprun.get_motor("%s"%self.Xname.text())
        MotorY=self.xprun.get_motor("%s"%self.Yname.text())
        MotorZ=self.xprun.get_motor("%s"%self.Zname.text())
        self.X=Spinner_Slide_Motor(self.Xslide,self.SpinX,MotorX,self.Xmin,self.Xmax,self.Xstep)
        self.Y=Spinner_Slide_Motor(self.Yslide,self.SpinY,MotorY,self.Ymin,self.Ymax,self.Ystep)
        self.Z=Spinner_Slide_Motor(self.Zslide,self.SpinZ,MotorZ,self.Zmin,self.Zmax,self.Zstep)


    def Move(self):
        self.X.Move()
        self.Y.Move()
        self.Z.Move()

    def run_scan(self):
        self.processed=[]
        max_index_x=self.X.get_settings()[2]
        max_index_y=self.Y.get_settings()[2]
        max_index =max_index_x*max_index_y
        if self.parent:
            self.parent.max_index=max_index
            self.parent.x_index=max_index_x
            self.parent.y_index=max_index_y
        count_time=self.Counter.value()
        if "%s"%self.ScanBox.currentText()=="tseries":
            self.xprun.set_cmd("tseries %s %s"%(max_index,count_time))
        else:
            x = self.X.get_motor_name()
            y = self.Y.get_motor_name()
            (xmin, xmax, xstep)=self.X.get_settings()
            (ymin, ymax, ystep)=self.Y.get_settings()
            self.xprun.set_cmd("mesh motor %s %s %s %s %s %s %s"\
                        %(x,xmin,xmax,xstep,y,ymin,ymax,ystep,count_time))
        self.xprun.run_cmd()



class Spinner_Slide_Motor:
    def __init__(self,Slide,Spin, Motor,Min,Max,Step):
        self.Spin=Spin
        self.Slide=Slide
        self.Motor=Motor
        self.Min=Min
        self.Max=Max
        self.Step=Step
        QtCore.QObject.connect(self.Slide,QtCore.SIGNAL("sliderReleased()"),
                               self.slide)
        QtCore.QObject.connect(self.Spin,
                               QtCore.SIGNAL("editingFinished()"),self.spin)
        self.get_params()
        self.setup()
    def get_params(self):
        self.values=[]
        params=['position','offset','sign',"low_limit","high_limit","step_size"]
        for param in params:
            try: 
                self.values.append(self.Motor.getParameter(param))
            except:
                self.values.append("unable to get value")
            
    def setup(self):
        values=self.values
        min =values[2]*values[3]+values[1]
        max=values[2]*values[4]+values[1]
        motor_step_size=values[5]
        self.Step.setRange(-100000,100000)
        self.Step.setValue(1)
        self.Max.setRange(min,max)
        self.Min.setRange(min,max)
        self.Max.setValue(max)
        self.Min.setValue(min)
        self.Spin.setRange(min,max)
        self.Slide.setRange(min*motor_step_size,max*motor_step_size)
        self.Spin.setValue(self.values[0])
        self.Slide.setTickInterval(20*motor_step_size)
        self.spin()
    def slide(self):
        self.Spin.setValue(self.Slide.value()/self.values[5])
    def spin(self):
        self.Slide.setValue(self.Spin.value()*self.values[5])
    def Move(self):
        self.Motor.move(self.Spin.value())
    def get_settings(self):
        return (self.Min.value(),self.Max.value(),self.Step.value())
    def get_motor_name(self):
        return self.motor.specName
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyXP()
    myapp.show()
    sys.exit(app.exec_())
