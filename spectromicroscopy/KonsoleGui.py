#!/usr/bin/env python
################################################################################
import sys, os, codecs
from os.path import isfile
OS="linux"
if sys.platform=="win32":
    OS="Windows"
    import subprocess as sp
else:
    from pexpect import run

    

#GUI
from PyQt4 import QtCore, QtGui
from Konsole import Ui_Kontrol

class MyKon(Ui_Kontrol,QtGui.QMainWindow):
    """Establishes a custom Console for interacting with the Computer"""
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.Runner, QtCore.SIGNAL("clicked()"),
                               self.konsole)
        QtCore.QObject.connect(self.MacroSave, QtCore.SIGNAL("clicked()"),
                               self.macrosave)
        QtCore.QObject.connect(self.changer, QtCore.SIGNAL("clicked()"),
                               self.change)
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

if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MyKon()
    myapp.show()
    sys.exit(app.exec_())
        