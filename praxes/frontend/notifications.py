"""
"""
from __future__ import absolute_import

import smtplib
import os
import sys
import socket
from getpass import getpass

from PyQt4 import QtCore,  QtGui


from .ui.ui_notificationsdialog import Ui_NotificationsDialog


class Mailer(QtGui.QWidget):

    def __init__(self,subject, message=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.settings = QtCore.QSettings()

        server = str(self.settings.value('Email/server').toString())
        port = str(self.settings.value('Email/port').toInt()[0])
        user = str(self.settings.value('Email/user').toString())
        pwd = str(self.settings.value('Email/pwd').toString())
        mailFrom = str(self.settings.value('Email/mailFrom').toString())
        tls = self.settings.value('Email/tls').toBool()
        secure = self.settings.value('Email/secure').toBool()
        mailTo = self.getTo()
        sendTo = mailTo.split(';')

        try:
            mailer = smtplib.SMTP(server,port)
        except socket.gaierror:
            self.warn('socket error','The server address is not correct')
            return
        except socket.error:
            self.warn('Socket Error','check server and port')
            return

        if secure: mailer.ehlo()
        if tls: mailer.starttls()

        try:
            mailer.login(user,pwd)
        except smtplib.SMTPAuthenticationError:
            self.warn('SMTP Error', 'login failed')
            return
        except smtplib.SMTPException:
            self.warn('SMTP Error','Authorization failed, set security')
            return

        if message:
            msg = """\
From: %s
To: %s
Subject: %s

%s"""%(mailFrom,mailTo,subject,message)
        else:
            msg = """\
From: %s
To: %s
Subject: %s"""%(mailFrom,mailTo,subject)
        print '\n',msg

        try:
            mailer.sendmail(mailFrom,sendTo,msg)
        except smtplib.SMTPSenderRefused:
            self.warn('Sender Refused','Domain of a sender address does not exist')
        mailer.quit()

    def warn(self, title, message):
        QtGui.QMessageBox.warning(self, title, message)
        EmailDialog().exec_()

    def getRawInfo(self):
        try:
            server, port = raw_input('server:port ').split(':',1)
        except ValueError:
            print 'Wrong format'
            return
        user = raw_input('login: ')
        pwd = getpass()
        mailFrom = raw_input('From: ')
        mailTo =  raw_input('To: ')
        sendTo= mailTo.split(';')
        tls = True
        secure = True
        return [server,port,user,pwd,mailFrom,mailTo,sendTo,tls,secure]

    def getSetInfo(self):
        server = 'authusersmtp.mail.cornell.edu'
        port = '25'
        user = 'jil26'
        pwd =getpass()
        mailFrom = 'Praxes at f3 <praxes@cornell.edu>'
        mailTo =  'jil26@cornell.edu'

        tls = True
        secure = True
        return [server,port,user,pwd,mailFrom,mailTo,sendTo,tls,secure]

    def getTo(self):
#        importantAddresses = self.settings.value('Email/importantAddresses').toString()
#        regualrAddresses = self.settings.value('Email/regularAddresses').toString()
        return str(self.settings.value('Email/mailFrom').toString())


class Notice(Mailer):

    def __init__(self,subject,message=None):
        subject='Notice: '+subject
        mailer.__init__(self,subject,message)

    def getTo(self):
        return ';'.join(
            str(
                self.settings.value('Email/regularAddresses').toString()
            ).splitlines()
        )


class Alarm(Mailer):

    def __init__(self,subject,message=None):
        subject='ALARM: '+subject
        mailer.__init__(self,subject,message)

    def getTo(self):
        regualrAddresses = ';'.join(
            str(
                self.settings.value('Email/regularAddresses').toString()
            ).splitlines()
        )
        importantAddresses = ';'.join(
            str(
                self.settings.value('Email/importantAddresses').toString()
            ).splitlines()
        )
        return ';'.join([regualrAddresses, importantAddresses])


class NotificationsDialog(Ui_NotificationsDialog, QtGui.QDialog):

    """Specify email settings"""

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.allEdit.setFocus()
        self.settings = QtCore.QSettings()
        self.getValues()
        self.importantBox.toggled.connect(self.importantWarn)

    def importantWarn(self, bool):
        if bool:
            response = QtGui.QMessageBox.warning(
                self,
                'Editing Important Emails',
                'Only edit these addresses if you are the system administrator',
                QtGui.QMessageBox.Ok| QtGui.QMessageBox.Cancel
            )
            if response == QtGui.QMessageBox.Ok:
                self.importantEdit.setEnabled(True)
            else:
                self.importantEdit.setEnabled(False)
                self.importantBox.setChecked(False)


    def exec_(self):
        if QtGui.QDialog.exec_(self):
            self.setValues()

    def accept(self):
        self.setValues()
        QtGui.QDialog.accept(self)

    def setValues(self):
            self.settings.setValue(
                'Email/emailDlgGeometry',
                QtCore.QVariant(self.saveGeometry())
            )
            self.settings.setValue(
                'Email/server',
                QtCore.QVariant(self.serverEdit.text())
            )
            self.settings.setValue(
                'Email/port',
                QtCore.QVariant(self.portSpin.value())
            )
            self.settings.setValue(
                'Email/user',
                QtCore.QVariant(self.loginEdit.text())
            )
            self.settings.setValue(
                'Email/pwd',
                QtCore.QVariant(self.passEdit.text())
            )
            self.settings.setValue(
                'Email/mailFrom',
                QtCore.QVariant(self.fromEdit.text())
            )
            self.settings.setValue(
                'Email/importantAddresses',
                QtCore.QVariant(self.importantEdit.document().toPlainText())
            )
            self.settings.setValue(
                'Email/regularAddresses',
                QtCore.QVariant(self.allEdit.document().toPlainText())
            )
            self.settings.setValue(
                'Email/tls',
                QtCore.QVariant(self.tlsCheck.isChecked())
            )
            self.settings.setValue(
                'Email/secure',
                QtCore.QVariant(self.secureCheck.isChecked())
            )

    def getValues(self):
        self.restoreGeometry(
            self.settings.value('Email/emailDlgGeometry').toByteArray()
        )
        self.serverEdit.setText(self.settings.value('Email/server').toString())
        self.portSpin.setValue(self.settings.value('Email/port').toInt()[0])
        self.loginEdit.setText(self.settings.value('Email/user').toString())
        self.passEdit.setText(self.settings.value('Email/pwd').toString())
        self.fromEdit.setText(self.settings.value('Email/mailFrom').toString())
        self.importantEdit.setText(
            self.settings.value('Email/importantAddresses').toString()
        )
        self.allEdit.setText(
            self.settings.value('Email/regularAddresses').toString()
        )
        self.tlsCheck.setChecked(self.settings.value('Email/tls').toBool())
        self.secureCheck.setChecked(
            self.settings.value('Email/secure').toBool()
        )


if __name__  ==  "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Praxes')
    Notice('Testing Praxes','working')
    myapp = EmailDialog()
    myapp.show()
    sys.exit(app.exec_())
