#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from __future__ import absolute_import

import smtplib
import os
import sys
import socket
from getpass import getpass

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore,  QtGui

#---------------------------------------------------------------------------
# GUI imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .emailDlg import EmailDialog

#---------------------------------------------------------------------------
# Normal code begins
#--------------------------------------------------------------------------


class mailer(QtGui.QWidget):

    def __init__(self,subject, message=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.settings = QtCore.QSettings()
        server,port,user,pwd,mailFrom,mailTo,sendTo,tls,secure = self.getSavedInfo()

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



##########################################################
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
#############################################
    def getSetInfo(self):
        server = 'authusersmtp.mail.cornell.edu'
        port = '25'
        user = 'jil26'
        pwd =getpass()
        mailFrom = 'XPaXS at f3 <XPaXS@cornell.edu>'
        mailTo =  'jil26@cornell.edu'

        tls = True
        secure = True
        return [server,port,user,pwd,mailFrom,mailTo,sendTo,tls,secure]
###########################################
    def getSavedInfo(self):
        server = str(self.settings.value('Email/server').toString())
        port = str(self.settings.value('Email/port').toInt()[0])
        user = str(self.settings.value('Email/user').toString())
        pwd = str(self.settings.value('Email/pwd').toString())
        mailFrom = str(self.settings.value('Email/mailFrom').toString())
        tls = self.settings.value('Email/tls').toBool()
        secure = self.settings.value('Email/secure').toBool()

        mailTo=self.getTo()
        sendTo= mailTo.split(';')
        return [server,port,user,pwd,mailFrom,mailTo,sendTo,tls,secure]


    def getTo(self):
#        importantAddresses = self.settings.value('Email/importantAddresses').toString()
#        regualrAddresses = self.settings.value('Email/regularAddresses').toString()
        return str(self.settings.value('Email/mailFrom').toString())




class notice(mailer):
    def __init__(self,subject,message=None):
        subject='Notice: '+subject
        mailer.__init__(self,subject,message)

    def getTo(self):
        return';'.join(str(self.settings.value('Email/regularAddresses').toString()).splitlines())




class alarm(mailer):
    def __init__(self,subject,message=None):
        subject='ALARM: '+subject
        mailer.__init__(self,subject,message)
    def getTo(self):
        regualrAddresses = ';'.join(str(self.settings.value('Email/regularAddresses').toString()).splitlines())
        importantAddresses = ';'.join( str(self.settings.value('Email/importantAddresses').toString()).splitlines())
        return ';'.join( [regualrAddresses, importantAddresses])


if __name__  ==  "__main__":
    print __file__
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = notice('Testing XPaXS','working')
#    sys.exit(app)
