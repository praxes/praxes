"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external.SpecClient import SpecVariable

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class QtSpecVariableA(SpecVariable.SpecVariableA):
    
#    def __init__(self, var, host_port):
#        SpecVariable.SpecVariableA.__init__(self, var, host_port)
#        if DEBUG:
#            print '%s connected at %s'%(self.getVarName(),
#                                               host_port)
    
    def connected(self):
        self.__connected__ = True
        if DEBUG: print 'Variable %s connected'%self.getVarName()
    
    def disconnected(self):
        self.__connected__ = False
        if DEBUG: print "Variable %s disconnected"%self.getVarName()
    
    def update(self, value):
        print "Variable %s updated to %s"%(self.getVarName(), value)
    
    def isConnected(self):
        return (self.__connected__ != None) and (self.__connected__)
    
    def getVarName(self):
        return self.channelName[4:len(self.channelName)]


class QtSpecVariable(SpecVariable.SpecVariable):

    def __init__(self, var, host_port, timeout=None):
        SpecVariable.SpecVariable.__init__(self, var, host_port)
        if DEBUG: print '%s connected at %s'%(self.getVarName(), host_port)

    def getVarName(self):
        return self.channelName[4:len(self.channelName)]
