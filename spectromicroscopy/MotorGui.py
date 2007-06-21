"""
This program is a Graphical User interface for X-ray Spectroscopy
"""

###############################################################################################
"""Use this to set the mode of the program"""
DEBUG=0       #if set to 1 it deactivates spec commands
Rollcall=2    #if set to 1 it auto starts spec -s on roll.chess.cornell.edu and connects
              #if set to 2 it wont autostart but will autoconnect 

##############################################################################################

#file Manipulation
import sys, os, codecs
from os.path import isfile
if sys.platform=="win32":
    OS="windows"
    import subprocess as sp
    DEBUG=1
    Rollcall=0
else:
    OS="linux"
    from pexpect import run


if DEBUG==1:
    if OS!="windows":
        path=os.path.join(os.path.expanduser("~"),"workspace/SpectroMicroscoPy/scripts")
    else:
        path=os.path.join(os.path.expanduser("~"),"My Documents/labwork/SpectroMicroscoPy/scripts")
    os.system("pyuic4 %s/GearHead.ui>%s/GearHead.py"%(path,path))
    

#GUI
from PyQt4 import QtCore, QtGui    
from GearHead import Ui_MotorHead
from time import localtime, strftime
strftime("%a, %d %b %Y %H:%M:%S", localtime())    

#SpecClient
import SpecClient
SpecClient.setLoggingOff()
from SpecClient import SpecMotor, Spec, SpecEventsDispatcher, SpecVariable, SpecCommand
stateStrings = ['NOTINITIALIZED', 'UNUSABLE', 'READY', 'MOVESTARTED', 'MOVING', 'ONLIMIT']

################################################################################################



class StartQT4(QtGui.QMainWindow):
    """Any and all things GUI"""
    command="none"
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MotorHead()
        self.ui.setupUi(self)
        self.ui.Motors.setColumnCount(1)
        self.ui.Motors.setHeaderLabel("motors")
    #Connects to the diffrent buttons
        QtCore.QObject.connect(self.ui.ChangeFile, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.saver,QtCore.SIGNAL("clicked()"), self.file_save)
        QtCore.QObject.connect(self.ui.saveras,QtCore.SIGNAL("clicked()"), self.file_saveas)
        QtCore.QObject.connect(self.ui.ClearLog, QtCore.SIGNAL("clicked()"), self.clearlog)
        QtCore.QObject.connect(self.ui.Runner,QtCore.SIGNAL("clicked()"),self.runner)
        QtCore.QObject.connect(self.ui.MacroSave, QtCore.SIGNAL("clicked()"),self.macro)
        QtCore.QObject.connect(self.ui.changer,QtCore.SIGNAL("clicked()"),self.change)
    #Sets up Response/log Window
        if OS=="windows":
            self.path=os.path.join(os.path.expanduser("~"),"My Documents/labwork/testing/src")
        else:
            self.path=os.path.join(os.path.expanduser("~"),"workspace/SpectroMicroscoPy/scripts")
        self.filename=os.path.join(self.path,"log.txt")
        s=codecs.open(self.filename,'r','utf-8').read()
        self.ui.Responses.setPlainText(s)
    #Sets up the Menus:
        #TODO: setup menus more
        self.ui.Bar.addAction("New Macro",self.Macro)
        self.ui.Bar.addAction("Old Macro",self.tester)
    
#Most of the Methods are self explanitory
    def clearlog(self):
        if isfile(self.filename):
            self.ui.Responses.clear()
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.ui.Responses.toPlainText()))
            self.writethis(self.last_written)
            self.ui.Responses.scrollToAnchor(self.last_written)
    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        if isfile(self.filename):
            s = codecs.open(self.filename,'r','utf-8').read()
            self.ui.Responses.setPlainText(s)
    def file_save(self):
        if isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.ui.Responses.toPlainText()))
            s.close()
    def file_saveas(self):
        self.currentfile=self.filename
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        if isfile(self.filename):
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.ui.Responses.toPlainText()))
            s.close()
            self.filename=self.currentfile
    def writethis(self,string):
        if isfile (self.filename):
            s = codecs.open(self.filename,'a','utf-8')
            s.write(unicode(string))
            self.last_written=string
            s.close()
            s=codecs.open(self.filename,'r','utf-8').read()
            self.ui.Responses.setPlainText(s)     

    def runner(self):
        self.ui.Display.append(">>>"+self.ui.KonsoleEm.toPlainText())
        Kommands=self.ui.KonsoleEm.toPlainText().split(";")
        if OS=="windows":#long way around pexpect not working with Windows
            for i in range(len(Kommands)):
                cmd="%s"%Kommands[i]
                try:
                    p=sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE)
                    result=p.communicate()[0]
                    self.ui.Display.append(result)
                except:
                    oldpath=self.path
                    newpath=os.path.join(os.path.expanduser("~"),"My Documents\labwork\\testing\\src")
                    self.path=os.path.join(self.path,newpath)
                    os.chdir(self.path)
                    program="python SubKonsole.py"
                    input=cmd+","+oldpath
                    p=sp.Popen(program,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE)
                    (result,error)=p.communicate(input)
                    self.ui.Display.append(result)
                    self.ui.Display.append(error)
                    os.chdir(oldpath)
                    
        else:
            for i in range(len(Kommands)):
                Kommand="%s"%Kommands[i]
                doingit=run(Kommand)
                self.ui.Display.append(doingit)
                      
    def Macro(self):
        if OS=="windows":
            print "signal sent"
        else:
            os.system("gedit")
        
    def macro(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName()
        s = codecs.open(self.filename,'w','utf-8')
        s.write(unicode(self.ui.KonsoleEm.toPlainText()))
        s.close()
            
    def change(self):
        try:
            fd = QtGui.QFileDialog(self)
            self.path = "%s"%fd.getExistingDirectory()
            os.chdir(self.path)
        except: 
            os.system("dir")
    def tester(self):
        #used to see if a signal is received
        self.writethis("\n :P")

"""

    Section for actual Motor Control Mockup
    These are the things set up by Danny
***********ACTUAL MOTOR CONTROLS FOLLOW**********

"""


class TestSpecMotor(SpecMotor.SpecMotorA):
    def connected(self):
        self.__connected__ = True
        StartQT4.writethis(myapp,'Motor %s connected'%self.specName)
    def disconnected(self):
        self.__connected__ = False
        StartQT4.writethis(myapp, 'Motor %s disconnected'%self.specName)
    def motorLimitsChanged(self):
        limits = self.getLimits()
        limitString = "(" + str(limits[0])+", "+ str(limits[1]) + ")"
        StartQT4.writethis(myapp, "Motor %s limits changed to %s"%self.specName,limitString)
    def motorPositionChanged(self, absolutePosition):
        StartQT4.writethis(myapp, "Motor %s position changed to %s"%self.specName,absolutePosition)
    def syncQuestionAnswer(self, specSteps, controllerSteps):
        StartQT4.writethis(myapp,"Motor %s syncing"%self.specName)
    def motorStateChanged(self, state):
        StartQT4.writethis(myapp,"Motor %s state changed to"%self.specName,stateString[state])
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)

class TestSpecVariable(SpecVariable.SpecVariableA):
    def connected(self):
        self.__connected__ = True
        StartQT4.writethis(myapp,'Variable %s connected'%self.getVarName())
    def disconnected(self):
        self.__connected__ = False
        StartQT4.writethis(myapp, "Variable %s disconnected"%self.getVarName())
    def update(self, value):
        StartQT4.writethis(myapp, "Variable %s updated to %s"%self.getVarName(),value)
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    def getVarName(self):
        return self.channelName[4:len(self.channelName)]

class TestSpecCommand(SpecCommand.SpecCommandA):
    def beingWait(self):
        StartQT4.writethis(myapp, 'Command %s was sent'%self.command)
    def replyArrived(self, reply):
        if (reply.error):
            StartQT4.writethis(myapp, "command %s received an error message: "%self.command,reply.data)
        else:
            StartQT4.writethis(myapp,"Command %s received a reply: %s"%self.command,reply.data)


"""
This section is what actualy causes the GUI to run and interact with the motors
"""



class Runthis:
    """Connects ot important GUI widgets and set key values"""
    count=0 # for input control
    clicked=0# for Motorselect control
    varnames = () # TODO: finish these commands
    spec = None
    specPort=None
    specHost=None
    UI=None
    selected=None
    var=None
    cmd=None

    def __init__(self,UI):
        time=strftime("%a, %d %b %Y %H:%M:%S", localtime())
        UI.writethis("\n New Session started ("+time+")\n Enter spec server hostname: ")        
        self.UI=UI
        QtCore.QObject.connect(self.UI.ui.EStop,QtCore.SIGNAL("clicked()"),self.EStop)
        QtCore.QObject.connect(self.UI.ui.ReStart,QtCore.SIGNAL("clicked()"),self.reStart)
        QtCore.QObject.connect(self.UI.ui.CommandLine, QtCore.SIGNAL("returnPressed()"),self.input)
    def input(self):
        """converts a string from the textbox into motors and variables"""
        command=self.UI.ui.CommandLine.text()
        self.UI.ui.CommandLine.clear()
        self.UI.writethis("\n>>>>%s"%command)

        if not self.specHost:
            self.specHost=command
            self.UI.writethis("\n %s is spec host"%self.specHost)
            self.UI.writethis("\n Enter spec server port: ")
        elif not self.specPort:
            try:
                self.specPort=command
                self.UI.writethis("\n %s is the spec server port: "%self.specPort)     
                if DEBUG==1:
                    self.spec=("motor0","motor1","motor2")
                    varnames=("variable1","number 2","Shalosh")  
                else:
                    if Rollcall==1 or Rollcall==2:
                        self.specHost="roll.chess.cornell.edu"
                        self.specPort="spec"
                    self.spec = Spec.Spec(self.specHost + ":" + self.specPort, 500)
            except:
                self.specHost=None
                self.specPort=None
                self.UI.writethis("\n Invalid Host or Port")
            self.ReadMotors()
        elif not self.selected:
            self.selected=command
            dict={}
            for i in range(len(self.motordisplay)):
                dict[self.motordisplay[i].text(0)]=self.motornames[i]
            if self.selected in dict.keys():
                self.UI.writethis("\n **%s selected**"%self.selected)
                self.selected=dict[self.selected]
            else:
                self.UI.writethis("\n select a motor please")
            if DEBUG==1:
                min = 30
                max = 100
            else:
                (min,max)=self.selected.getLimits()
            self.UI.ui.MoveBar.setRange(min,max)
            self.UI.ui.Positioner.setRange(min,max)
            self.UI.writethis("\n Select a Variable")
        
        elif not self.var:
            self.var=command
            self.UI.writethis("\n %s to be monitored \n Select  a command to run asynchronously: "%self.var)
        elif not self.cmd:
            self.cmd =command
            self.cmd=self.cmd.split(' ')
            if DEBUG==1:
                print self.selected
                self.UI.writethis('\n yay it worked')
                for i in range(len(self.cmd)):
                    self.UI.writethis("\n**It will %s**"%self.cmd[i])
            else:
                motorMon = TestSpecMotor(self.selected, self.specHost+":"+self.specPort)
                variableMon = TestSpecVariable(self.var, self.specHost+":"+self.specPort)
                commandMon = TestSpecCommand(self.cmd[0], self.specHost+":"+self.specPort)
                commandMon(self.cmd[1])
                while motorMon.isConnected() and variableMon.isConnected():
                    SpecEventsDispatcher.dispatch()
                if DEBUG!=1:
                    X=None
                    Y=None
                    Z=None
                    XPthis(self.UI,X,Y,Z)
            self.count=5
        else:
            self.UI.writethis("\n No command needed at the moment")
                
    def ReadMotors(self):
        self.motornames = []
        self.motordisplay =[]
        self.vardisplay=[]
        self.variables=[]
        k=0
        if DEBUG!=1:
            motors=self.spec.getMotorsMne()
        else:
            motors=("motor0","motor1","motor2")
            self.varname=("one","two","three")
            print self.varname
        for i in range(len(motors)):
            if DEBUG==1:
                self.motornames.append(self.spec[i])#test only
                NameString=motors[i]
            else:
                self.motornames.append(SpecMotor.SpecMotor(self.spec.motor_name(i),self.specHost + ":" + self.specPort, 500))
                NameString=self.spec.motor_name(i) #"%s"%self.motornames[i]
            self.motordisplay.append(QtGui.QTreeWidgetItem(self.UI.ui.Motors))
            self.motordisplay[i].setText(0,NameString)
            for j in range(len(self.varnames)):
                self.variables.append(self.varnames[j])
                self.vardisplay.append(QtGui.QTreeWidgetItem(self.motordisplay[i]))
                VarString=self.variables[j]
                self.vardisplay[k].setText(0,VarString)
                k+=1
        QtCore.QObject.connect(self.UI.ui.Motors,QtCore.SIGNAL("itemSelectionChanged ()"),self.MotorSelected)
        self.UI.writethis("\n Select a Motor")        
    def MotorSelected(self):
        # TODO: rework to be based on selectedItems()[0] rather than clicked
        if not self.selected:        
            dict={}
            for i in range(len(self.motordisplay)):
                dict[self.motordisplay[i]]=self.motornames[i]
            if self.UI.ui.Motors.selectedItems()[0] in dict.keys():
                self.selected=dict[self.UI.ui.Motors.selectedItems()[0]]
                self.UI.writethis("\n **%s selected**"%self.UI.ui.Motors.selectedItems()[0].text(0))
                if DEBUG==1:            
                    min = 30
                    max = 100
                else:
                    (min,max)=self.selected.getLimits()
                self.UI.ui.MoveBar.setRange(min,max)
                self.UI.ui.Positioner.setRange(min,max)
                self.UI.writethis("\n Select a Variable")
            else:
                self.UI.writethis("\n select a motor first")
                 
                
        elif not self.var:
            dict={}
            for i in range(len(self.variables)):
                dict[self.vardisplay[i]]=self.variables[i]
            if self.UI.ui.Motors.selectedItems()[0] in dict.keys():
                self.var=dict[self.UI.ui.Motors.selectedItems()[0]]
                self.UI.writethis("\n **%s to be monitored** \n Select  a command to run asynchronously: "%self.var)
                QtCore.QObject.connect(self.UI.ui.Mover,QtCore.SIGNAL("clicked()"),self.cmdMove)
    def EStop(self):
        if self.cmd:
            if DEBUG!=1:
                os.abort()
            self.cmd=None
            self.input("stop()")
            self.cmd=None
            self.UI.writethis("\n %%%%%%%%%%%%ALL STOP%%%%%%%%%")
    def cmdMove(self):
        cmd="move(%s)"%self.UI.ui.Positioner.value()
        self.input(cmd)
    def reStart(self):
        self.spec=None
        if DEBUG==1:
            self.spec=("motor0","motor1","motor2")#test only
        self.specHost=None
        self.specPort=None
        self.motornames = []
        self.motordisplay =[]
        self.vardisplay=[]
        self.variables=[]
        self.UI.ui.Motors.clear()
        self.clicked=0
        self.UI.writethis("\n Enter spec server hostname: ")
        self.UI.clearlog()
    def tester(self):
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
    myapp = StartQT4()
    myapp.show()
    myrun = Runthis(myapp)
    if Rollcall==1: 
        import pxssh
        s = pxssh.pxssh()
        if not s.login ('roll.chess.cornell.edu', 'specuser', 'CThrooMe'):
            myapp.writethis("SSH session failed on login.")
            myapp.writethis(str(s))
        else:
            myapp.writethis("SSH session login successful")
            s.sendline ('spec -S')
    if DEBUG==1:
        X=None
        Y=None
        Z=None
        myxp=XPthis(myapp,X,Y,Z)
    sys.exit(app.exec_())