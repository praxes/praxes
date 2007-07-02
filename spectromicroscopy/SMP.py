import os
path=os.path.join(os.path.expanduser("~"),
                  "My Documents/labwork/spectromicroscopy/spectromicroscopy/")

os.system("pyuic4 %s/GearTester.ui>%s/GearTester.py"%(path,path))
from PyQt4 import QtCore, QtGui    
from SMP import Ui_Main

class MySMP(Ui_Main,QtGui.QMainWindow):
    """Establishes a Experimenbt controls"""
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        
if __name__ == "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    myapp = MySMP()
    myapp.show()
    sys.exit(app.exec_())
