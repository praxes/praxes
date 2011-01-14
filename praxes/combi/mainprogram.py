import time
import os
import sys
import numpy
from XRDdefaults import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from xrdUI import *


try:
    mainapp=None
    ltime=time.localtime()
    runfoldername="%4i" % ltime[0] + "%02i" % ltime[1] + "%02i" % ltime[2]+"_"+"%02i" % ltime[3]+"."+"%02i" % ltime[4]

    runrootpath = mygetdir(markstr = 'house XRDrundata folder', xpath = defaultdir('runlog'))
    datpath=defaultdir('dataimport')
    h5path=defaultdir('h5')
    runpath=os.path.join(runrootpath, runfoldername).replace('\\','/')
    while os.path.exists(runpath):
        runpath=''.join(runpath, 'a')
    os.makedirs(runpath)

    mainapp = QApplication(sys.argv)
    form = MainMenu(datpath=datpath, h5path=h5path, runpath=runpath)
    form.show()
    form.setFocus()
    mainapp.exec_()

finally:
    if mainapp is not None:
        mainapp.quit()
    print 'done'
