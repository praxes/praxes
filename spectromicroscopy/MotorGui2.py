#!/usr/bin/env python
"""
This program is a Graphical User interface for X-ray Spectroscopy
"""

################################################################################
######################Use this to set the mode of the program###################
DEBUG=2       #if set to 1 it deactivates spec commands
Rollcall=2    #if set to 1 it auto starts spec -s on roll.chess.cornell.edu
              #and connects if set to 2 it wont autostart but will autoconnect
OS="linux"    #set to linux or windows

################################################################################
  
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


if DEBUG!=2:
    if OS!="windows":
        path=os.path.join(os.path.expanduser("~"),
            "workspace/spectromicroscopy/spectromicroscopy/")
    else:
        path=os.path.join(os.path.expanduser("~"),
            "My Documents/labwork/spectromicroscopy/spectromicroscopy/")
    os.system("pyuic4 %s/GearHead.ui>%s/GearHead.py"%(path,path))
    

#GUI
from PyQt4 import QtCore, QtGui    
from GearHead import Ui_MotorHead
from time import localtime, strftime
from SpecRunner import SpecRunner




################################################################################
       

class MyUI(Ui_MotorHead,QtGui.QMainWindow):
    """Any and all things GUI"""
    
    def __init__(self, parent=None):
        if Rollcall==1:
            import pxssh
            self.sesh = pxssh.pxssh()
            if not self.sesh.login ('roll.chess.cornell.edu', 'specuser', 'CThrooMe'):
                if DEBUG!=2:
                    print"SSH session failed on login."
                    print str(self.sesh)
                else:
                    print "SSH login failed"
            else:
                if DEBUG!=2:
                    print "SSH session login successful"
                    self.sesh.sendline ('spec -S')
                    self.sesh.prompt()
                    print self.sesh.before
                else:
                    print "DEBUG=2?"
        else:
            self.sesh=None
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
    #Connects to the diffrent buttons
        QtCore.QObject.connect(self.ChangeFile, QtCore.SIGNAL("clicked()"),
                               self.file_dialog)
        QtCore.QObject.connect(self.saveras,QtCore.SIGNAL("clicked()"),
                               self.file_saveas)
        QtCore.QObject.connect(self.ClearLog, QtCore.SIGNAL("clicked()"),
                               self.clearlog)
        QtCore.QObject.connect(self.Runner, QtCore.SIGNAL("clicked()"),
                               self.konsole)
        QtCore.QObject.connect(self.MacroSave, QtCore.SIGNAL("clicked()"),
                               self.macrosave)
        QtCore.QObject.connect(self.changer, QtCore.SIGNAL("clicked()"),
                               self.change)
        QtCore.QObject.connect(self.EStop, QtCore.SIGNAL("clicked()"),
                               self.EmergencyStop)
        QtCore.QObject.connect(self.ReStart, QtCore.SIGNAL("clicked()"),
                               self.reStart)
        QtCore.QObject.connect(self.CommandLine, 
                               QtCore.SIGNAL("returnPressed()"), self.input)
        QtCore.QObject.connect(self.MotorsTree,
                               QtCore.SIGNAL("itemSelectionChanged ()"),
                               self.motorselect)
        QtCore.QObject.connect(self.Mover, QtCore.SIGNAL("clicked()"),
                               self.cmdMove)
        QtCore.QObject.connect(self.Closer,QtCore.SIGNAL("clicked()"),\
                                 self.endsesh)
    #Sets up the Menus:
        #TODO: setup menus more
        self.Bar.addAction("New Macro",self.macro)
        self.Bar.addAction("Old Macro",self.tester) 
    #SETS UP THE RUN
        self.filename=''
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
            try:
                connection=self.specrun.serverconnect()
                print " Connected to %s on %s"%(self.specrun.getspecport(),
                                                self.specrun.getspechost())
            except:
                print " Invalid Host or Server"
            if connection:
                self.specrun.readmotors()
                readmotors=self.specrun.getmotors()
                for i in range(len(readmotors)):
                    self.specrun.readvariables(readmotors[i])
                self.motorget()
        #TODO: update here till end of 
        elif not self.specrun.getmotor():
            print " Select a motor"
            self.specrun.setmotor(self.command)
        elif not self.specrun.getvar():
            print " **%s selected**\n Select a variable"%self.specrun.getmotor()
            self.specrun.setvar(self.specrun.getmotor(),self.command)
        elif not self.specrun.getcmd():
            print " %s to be monitored \n Select  a command to run \
asynchronously: "%self.var
            self.specrun.setcmd(self.command)
            self.specrun.runcmd() 
        else:
            print ":P"
        

    def input(self):
        """converts a string from the textbox into motors and variables"""
        self.command=self.CommandLine.text()
        self.CommandLine.clear()
        print "\n>>>>%s"%self.command
        self.runspec()
        
    def write(self,string):
        """stdout for program, displays on the Responses screen"""
        if string!="\n":
            self.last_written=string
            sys.stdout=sys.__stdout__
            print self.last_written
            sys.stdout=self
            if isfile (self.filename):
                s = codecs.open(self.filename,'a','utf-8')
                s.write(unicode(string))
                s.close()
            self.Responses.append(string)

    def EmergencyStop(self):
        self.specrun.EmergencyStop() 
    
    def clearlog(self):
        self.Responses.clear()
        if isfile(self.filename):
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
                    newpath=os.path.join(os.path.expanduser("~"),
                        "My Documents/labwork/testing/src")
                    self.path=os.path.join(self.path,newpath)
                    os.chdir(self.path)
                    program="python SubKonsole.py"
                    input=cmd+","+oldpath
                    p=sp.Popen(program, stdin=sp.PIPE, stdout=sp.PIPE,
                               stderr=sp.PIPE)
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

    def motorget(self):
        self.motordict={}
        self.motorwidget=[]
        self.motornames=[]
        for i in range(len(self.specrun.getmotors())):
            NameString=self.specrun.getmotors()[i]
            self.motorwidget.append(QtGui.QTreeWidgetItem(self.MotorsTree))
            self.motorwidget[i].setText(0,NameString)
            Status=self.specrun.status(self.specrun.getmotors()[i])
            self.motorwidget[i].setText(1,Status)
            self.motornames.append(NameString)
            self.motordict[self.motorwidget[i]]=self.motornames[i]
    def motorselect(self):
        if self.MotorsTree.selectedItems()[0] in self.motordict.keys():
            selection=self.motordict[self.MotorsTree.selectedItems()[0]]
            self.specrun.setmotor(selection)
            print " **%s selected**\n Select a variable"%self.specrun.getmotor()
            try:
                if DEBUG==1:            
                    min = 30
                    max = 100
                else:
                    (min,max)=self.specrun.getmotorlimits(selection)
                    place=self.specrun.getmotorposition(selection)
                self.MoveBar.setRange(min,max)
                self.Positioner.setRange(min,max)
            except:
                print "unable to get limits of motor"
            try:
                if DEBUG==1:
                    place=0
                else:
                    place=self.specrun.getmotorposition(selection)
                self.MoveBar.setValue(place)
                self.Positioner.setRange(place)
                print "\n Select a Variable"
            except:
                print "Unable to Get Position"
            
        else:
            print self.MotorsTree.selectedItems()[0]
            print "\n select a motor first"

    def varget(self):
        self.vardict={}
        self.varwidget=[]
        self.varnames=[]
        for i in range(len(self.motornames)):
            self.specrun.readvariables(self.motornames[i])
            MotorsVar= self.specrun.getvars(self.motornames[i])
            MotorValues=self.specrun.getvarsvalue(self.motornames[i])
            for j in range(len(MotorVar)):
                self.varwidget.append(QtGui.QTreeWidgetItem(self.motorwidget[i]))
                self.varwidget.setText(0,MotorVar[j])
                self.vardict[MotorVar[j]]=MotorValues[j]
        
    def varselect(self):
        #todo make this work
        print ("\n **%s to be monitored** \n"+\
                       "Select  a command to run asynchronously: "%self.var)
                
    def cmdMove(self):
        cmd="move(%s)"%self.Positioner.value()
        self.specrun.setcmd(cmd)
        self.specrun.runcmd()
            
    def reStart(self):
        self.specrun=SpecRunner()
        self.MotorsTree.clear()
        self.write("\n Enter spec server hostname: ")
        self.clearlog()
    def endsesh(self):
        if self.sesh:
            self.sesh.sendline('exit')
            self.sesh.prompt
            print self.sesh.before
            self.sesh.logout()
            self.sesh.close()
        else:
            time=strftime("%a, %d %b %Y %H:%M:%S", localtime())
            print "BYE!!!!!!!@%s"%time
        
    def tester(self):
        #used to see if a signal is received
        print "signaled"


                   
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyUI()
    myapp.show()
    sys.exit(app.exec_())
