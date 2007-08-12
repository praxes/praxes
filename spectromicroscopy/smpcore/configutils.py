"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import shutil

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.external import configobj

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

def getUserConfigDir():
    '''return the path to the user's spectromicroscopy config directory'''
    configDir = os.path.join(os.path.expanduser('~'), '.spectromicroscopy')
    if not os.path.exists(configDir): os.mkdir(configDir)
    return configDir

def getDefaultConfigDir():
    '''return the path to the default spectromicroscopy config directory'''
    import spectromicroscopy as smp
    return os.path.join(os.path.split(smp.__file__)[0], 'smp-data')

def getSmpConfigFile():
    return os.path.join(getUserConfigDir(), 'smp.conf')

def getSmpConfig():
    '''return a ConfigObj containing the smp config data'''
    return configobj.ConfigObj(getSmpConfigFile())

def getDefaultPymcaConfigFile():
    configFile = os.path.join(getUserConfigDir(), 'pymca.cfg')
    if not os.path.isfile(configFile):
        defaultConfigFile = os.path.join(getDefaultConfigDir(), 'pymca.cfg')
        shutil.copyfile(defaultConfigFile, configFile)
    return configFile

def getPymcaConfig(configFile=None):
    '''return a ConfigObj containing the pymca config data'''
    if not configFile: configFile = getPymcaConfigFile()
    return configobj.ConfigObj(configFile)

def getClientUtilsFile():
    return os.path.join(getDefaultConfigDir(), 'clientutils.mac')

def getClientUtilsMacro():
    return open(getClientUtilsFile()).read()


if __name__ == '__main__':
    getPymcaConfig()
