#!/usr/bin/pythonw
"""
This program is a Graphical User interface for X-ray Spectroscopy
"""

###############################################################################################
######################Use this to set the mode of the program##################################
DEBUG=0       #if set to 1 it deactivates spec commands
Rollcall=1    #if set to 1 it auto starts spec -s on roll.chess.cornell.edu and connects
              #if set to 2 it wont autostart but will autoconnect 
OS="linux"    #set to linux or windows

##############################################################################################
  
#file Manipulation
import sys, os, codecs
from os.path import isfile
import subprocess as sp
if sys.platform=="win32":
    OS="windows"
    DEBUG=1
    Rollcall=0
else:
    from pexpect import run


if DEBUG==1:
    if OS!="windows":
        path=os.path.join(os.path.expanduser("~"),"workspace/spectromicroscopy/spectromicroscopy/")
    else:
        path=os.path.join(os.path.expanduser("~"),"My Documents/labwork/spectromicroscopy/spectromicroscopy/")
    os.system("pyuic4 %s/GearHead.ui>%s/GearHead.py"%(path,path))
    

#GUI
from PyQt4 import QtCore, QtGui    
from GearHead import Ui_MotorHead
from time import localtime, strftime
from SpecRunner import SpecRunner




################################################################################################
       

class MyUI(Ui_MotorHead,QtGui.QMainWindow):
    """Any and all things GUI"""
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.Motors.setColumnCount(1)
        self.Motors.setHeaderLabel("motors")
    #Connects to the diffrent buttons
        QtCore.QObject.connect(self.ChangeFile, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.saver,QtCore.SIGNAL("clicked()"), self.file_save)
        QtCore.QObject.connect(self.saveras,QtCore.SIGNAL("clicked()"), self.file_saveas)
        QtCore.QObject.connect(self.ClearLog, QtCore.SIGNAL("clicked()"), self.clearlog)
        QtCore.QObject.connect(self.Runner,QtCore.SIGNAL("clicked()"),self.konsole)
        QtCore.QObject.connect(self.MacroSave, QtCore.SIGNAL("clicked()"),self.macrosave)
        QtCore.QObject.connect(self.changer,QtCore.SIGNAL("clicked()"),self.change)       
        QtCore.QObject.connect(self.EStop,QtCore.SIGNAL("clicked()"),self.EmergencyStop)
        QtCore.QObject.connect(self.ReStart,QtCore.SIGNAL("clicked()"),self.reStart)
        QtCore.QObject.connect(self.CommandLine, QtCore.SIGNAL("returnPressed()"),self.input)
        QtCore.QObject.connect(self.Motors,QtCore.SIGNAL("itemSelectionChanged ()"),self.motorselect)
    #Sets up Response/log Window
        if OS=="windows":
            self.path=os.path.join(os.path.expanduser("~"),"My Documents/labwork/testing/src")
        else:
            self.path=os.path.join(os.path.expanduser("~"),\
                                   "workspace/spectromicroscopy/spectromicroscopy")
        self.filename=os.path.join(self.path,"log.txt")
        s=codecs.open(self.filename,'r','utf-8').read()
        self.Responses.setPlainText(s)
    #Sets up the Menus:
        #TODO: setup menus more
        self.Bar.addAction("New Macro",self.macro)
        self.Bar.addAction("Old Macro",self.tester) 
    #SETS UP THE RUN
        self.command=''
        sys.stdout=self
        self.specrun=SpecRunner(DEBUG,Rollcall,self)
        time=strftime("%a, %d %b %Y %H:%M:%S", localtime())
        print "\n New Session started (%s)\n Enter spec server hostname: "%time
        

            
    def runspec(self):

        if not self.specrun.getspechost():
            self.specrun.setspechost(self.command)
            print " Host set as %s \n Select a Port"%self.command
        elif not self.specrun.getspecport():
            self.specrun.setspecport(self.command)
            print " Port set as %s"%self.command
        elif not self.specrun.serverconnect():
            print " Invalid Host or Server"
        elif not self.specrun.getmotors():
            print " Connected to %s on %s"%(self.specrun.getspechost(),\
                                              self.specrun.getspecport())
            self.specrun.readmotors()
            readmotors=self.specrun.getmotors()
            for i in range(len(readmotors)):
                self.specrun.readvariables(readmotors[i])
            #self.motorselect()
        elif not self.specrun.getmotor():
            print " Select a motor"
            self.specrun.setmotor(self.command)
        elif not self.specrun.getvar():
            print " **%s selected**\n Select a variable"%self.specrun.getmotor()
            self.setvar(self.command)
        elif not self.specrun.getcmd():
            print " %s to be monitored \n Select  a command to run asynchronously: "%self.var
            self.specrun.setcmd(self.command)
            self.specrun.runcmd() 
        else:
            pass
        

    def input(self):
        """converts a string from the textbox into motors and variables"""
        self.command=self.CommandLine.text()
        self.CommandLine.clear()
        print "\n>>>>%s"%self.command
        self.runspec()
        
    def write(self,string):
        """stdout for program, displays on the Responses screen"""
        if isfile (self.filename):
            if string!="\n":
                s = codecs.open(self.filename,'a','utf-8')
                s.write(unicode(string))
                self.last_written=string
                sys.stdout=sys.__stdout__
                print self.last_written
                sys.stdout=self
                s.close()
                s=codecs.open(self.filename,'r','utf-8').read()
                self.Responses.append(string)

    def EmergencyStop(self):
        self.specrun.EmergencyStop() 
    
#Most of the Methods are self explanitory
    def clearlog(self):
        if isfile(self.filename):
            self.Responses.clear()
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.Responses.toPlainText()))
            s.close()
            self.write(self.last_written)
    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        if isfile(self.filename):
            s = codecs.open(self.filename,'r','utf-8').read()
            self.Responses.setPlainText(s)
    def file_save(self):
        if isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.Responses.toPlainText()))
            s.close()
    def file_saveas(self):
        self.currentfile=self.filename
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        if isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.Responses.toPlainText()))
            s.close()
            self.filename=self.currentfile   

    def konsole(self):
        self.Display.append(">>>"+self.KonsoleEm.toPlainText())
        Kommands=self.KonsoleEm.toPlainText().split(";")
        if OS=="windows":#long way around pexpect not working with Windows
            for i in range(len(Kommands)):
                cmd="%s"%Kommands[i]
                try:
                    p=sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE)
                    result=p.communicate()[0]
                    self.Display.append(result)
                except:
                    oldpath=self.path
                    newpath=os.path.join(os.path.expanduser("~"),"My Documents\labwork\\testing\\src")
                    self.path=os.path.join(self.path,newpath)
                    os.chdir(self.path)
                    program="python SubKonsole.py"
                    input=cmd+","+oldpath
                    p=sp.Popen(program,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE)
                    (result,error)=p.communicate(input)
                    self.Display.append(result)
                    self.Display.append(error)
                    os.chdir(oldpath)
                    
        else:
            for i in range(len(Kommands)):
                Kommand="%s"%Kommands[i]
                doingit=run(Kommand)
                self.Display.append(doingit)
                      
    def macro(self):
        if OS=="windows":
            print "signal sent"
        else:
            os.system("gedit")
        
    def macrosave(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        s = codecs.open(self.filename,'w','utf-8')
        s.write(unicode(self.KonsoleEm.toPlainText()))
        s.close()
            
    def change(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.path = "%s"%fd.getExistingDirectory()
            os.chdir(self.path)
        except: 
            os.system("dir")

    def motorselect(self):
        # TODO: rework work with new design
        dict={}
        for i in range(len(self.specrun.getmotors())):
            dict[self.motordisplay[i]]=self.motorwidget[i]
        if self.Motors.selectedItems()[0] in dict.keys():
            self.selected=dict[self.UI.ui.Motors.selectedItems()[0]]
            self.UI.write("\n **%s selected**"%self.UI.ui.Motors.selectedItems()[0].text(0))
            if DEBUG==1:            
                min = 30
                max = 100
            else:
                (min,max)=self.selected.getLimits()
            self.UI.ui.MoveBar.setRange(min,max)
            self.UI.ui.Positioner.setRange(min,max)
            self.UI.write("\n Select a Variable")
        else:
            self.UI.write("\n select a motor first")

    def varselect(self):
        if not self.var:
            dict={}
            for i in range(len(self.variables)):
                dict[self.vardisplay[i]]=self.variables[i]
            if self.UI.ui.Motors.selectedItems()[0] in dict.keys():
                self.var=dict[self.UI.ui.Motors.selectedItems()[0]]
                self.UI.write("\n **%s to be monitored** \n Select  a command to run asynchronously: "%self.var)
                QtCore.QObject.connect(self.UI.ui.Mover,QtCore.SIGNAL("clicked()"),self.cmdMove)
    def cmdMove(self):
        cmd="move(%s)"%self.Positioner.value()
        self.specrun.setcmd(cmd)
        self.specrun.runcmd()
            
    def reStart(self):
        self.specrun=SpecRunner()
        self.Motors.clear()
        self.write("\n Enter spec server hostname: ")
        self.clearlog()
        
    def tester(self):
        #used to see if a signal is received
        self.write("\n :P")

        print "signaled"
        
class XPthis:
    def __init__(self,UI,MotorX,MotorY,MotorZ):
        self.UI=UI
        QtCore.QObject.connect(self.UI.ui.X,QtCore.SIGNAL("sliderReleased()"),self.X)
        QtCore.QObject.connect(self.UI.ui.Y,QtCore.SIGNAL("sliderReleased()"),self.Y)
        QtCore.QObject.connect(self.UI.ui.Z,QtCore.SIGNAL("sliderReleased()"),self.Z)
        QtCore.QObject.connect(self.UI.ui.SpinX, QtCore.SIGNAL("editingFinished()"),self.SpinX)
        QtCore.QObject.connect(self.UI.ui.SpinY, QtCore.SIGNAL("editingFinished()"),self.SpinY)
        QtCore.QObject.connect(self.UI.ui.SpinZ, QtCore.SIGNAL("editingFinished()"),self.SpinZ)
        QtCore.QObject.connect(self.UI.ui.Stepper,QtCore.SIGNAL("editingFinished()"),self.Step)
        QtCore.QObject.connect(self.UI.ui.Stepper,QtCore.SIGNAL("clicked()"),self.Move)
        self.UI.ui.Namer.setMaxLength(1)
        self.dict={}
        self.dict["X"]=(self.UI.ui.X,self.UI.ui.SpinX,MotorX)
        self.dict["Y"]=(self.UI.ui.Y,self.UI.ui.SpinY,MotorY)
        self.dict["Z"]=(self.UI.ui.Z,self.UI.ui.SpinZ,MotorZ)
        # TODO: rework all this XYZ code to work with motors
        if DEBUG==1:
            self.UI.ui.X.setRange(0,10000)
            self.UI.ui.SpinX.setRange(0,100)
            self.UI.ui.Y.setRange(0,10000)
            self.UI.ui.SpinY.setRange(0,100) 
            self.UI.ui.Z.setRange(0,10000)
            self.UI.ui.SpinZ.setRange(0,100)
            self.Xsize=100.00
            self.Ysize=100.00
            self.Zsize=100.00
            self.UI.ui.X.setTickInterval(1000.00)
            self.UI.ui.Y.setTickInterval(1000.00)
            self.UI.ui.Z.setTickInterval(1000.00)
        else:
            pass
            #TODO: set up ticks = (Max-Min)stepsize
            """self.UI.ui.X.setTickInterval()
            self.UI.ui.Y.setTickInterval()
            self.UI.ui.Z.setTickInterval()"""
        self.X()
        self.Y()
        self.Z()
        

    def X(self):
        if DEBUG!=1:
            Xsize=MotorX.getOFFset()
            (Xmin,Xmax)=MotorX.getlimits()
            self.UI.ui.SpinX.setRange(Xmin,Xmax)
            self.UI.ui.X.setRange(Xmin,Xmax)
        self.UI.ui.SpinX.setValue(self.UI.ui.X.value()/self.Xsize)
    def Y(self):
        if DEBUG!=1:
            self.Ysize=MotorY.getOFFset()
            (Ymin,Ymax)=MotorY.getlimits()
            self.UI.ui.SpinY.setRange(Ymin,Ymax)
            self.UI.ui.Y.setRange(Ymin,Ymax)
        self.UI.ui.SpinY.setValue(self.UI.ui.Y.value()/self.Ysize)
    def Z(self):
        if DEBUG!=1:
            Zsize=MotorZ.getOFFset()
            (Zmin,Zmax)=MotorZ.getlimits()
            self.UI.ui.SpinZ.setRange(Zmin,Zmax)
            self.UI.ui.Z.setRange(Zmin,Zmax)
        self.UI.ui.SpinZ.setValue(self.UI.ui.Z.value()/self.Zsize)
    def SpinX(self):
        self.UI.ui.X.setValue(self.UI.ui.SpinX.value()*self.Xsize)
    def SpinY(self):
        self.UI.ui.Y.setValue(self.UI.ui.SpinY.value()*self.Ysize)
    def SpinZ(self):
        self.UI.ui.Z.setValue(self.UI.ui.SpinZ.value()*self.Zsize)
    
    def Step(self):
        Axis="%s"%self.UI.ui.Namer.text()
        Axis=Axis.capitalize()
        if Axis in self.dict.keys():
            (selectAxis,Spin,motor)=self.dict[Axis]
            if DEBUG==1:
                viable=True
                stepsize=100
            else:
                viable=self.UI.ui.Stepper.value()<motor.getOffset()
                stepsize=motor.setOffset(self.UI.ui.Stepper.value())
            if viable:
                selectAxis.setTickInterval(self.UI.ui.Stepper.value()*stepsize)
                selectAxis.setSingleStep(self.UI.ui.Stepper.value()*stepsize)
                Spin.setSingleStep(self.UI.ui.Stepper.value())
                
                
    def Move(self):
        if DEBUG==1:
            print "moved"
        else:
            MotorX.move(self.UI.ui.X.getValue())
            MotorY.move(self.UI.ui.Y.getValue())
            MotorZ.move(self.UI.ui.Z.getValue())

        
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if Rollcall==1: 
        import pxssh
        s = pxssh.pxssh()
        if not s.login ('roll.chess.cornell.edu', 'specuser', 'CThrooMe'):
            if DEBUG!=2:
                print"SSH session failed on login."
                print str(s)
            else:
                print "SSH login failed"
        else:
            if DEBUG!=2:
                print "SSH session login successful"
                s.sendline ('spec -S')
            else:
                print "DEBUG=2 +Connect"
    myapp = MyUI()
    myapp.show()
    sys.exit(app.exec_())