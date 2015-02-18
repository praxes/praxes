"""
"""
from __future__ import absolute_import

import sys

from PyQt4 import QtCore, QtGui, uic

from .ui import resources


class Viewer(QtGui.QWidget):

    """Establishes widget"""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi(resources['viewer.ui'], self)
        self.timer = QtCore.QTimer(self)

        self.urlBox.currentIndexChanged['QString'].connect(self.changeURL)
        self.reloadRateSpinvalueChanged[int].connect(self.changeFPS)
        self.timer.timeout.connect(self.reload)
        self.changeFPS()

    def changeFPS(self):
        time = self.reloadRateSpin.value()
        self.timer.stop()
        if time !=0:
            self.reload()
            self.timer.setInterval(1000/time)
            self.timer.start()
    def changeURL(self, address):
##        self.timer.stop()
        self.reloadRateSpin.setValue(0)
        url =QtCore.QUrl(self.urlBox.currentText())
        self.camWebView.setUrl(url)
##        self.timer.start()

    def reload(self):
        self.camWebView.reload()





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('test')
    myapp = Viewer()
    myapp.show()
    sys.exit(app.exec_())
