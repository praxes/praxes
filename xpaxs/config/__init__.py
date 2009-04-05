"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import glob
import logging
import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logger = logging.getLogger('XPaXS.config')

def getUserConfigDir():
    '''return the path to the user's spectromicroscopy config directory'''
    configDir = os.path.join(os.path.expanduser('~'), '.xpaxs')
    if not os.path.exists(configDir): os.mkdir(configDir)
    return configDir

def qrc2py(dir):
    """If .ui files are present, xpaxs is being run in development mode. In that
    case, convert .ui files to .py files.
    """
    for rc in glob.glob(dir+'/*.qrc'):
        py = os.path.splitext(rc)[0]+'_rc.py'
        if os.path.isfile(py):
            convert = os.path.getmtime(rc) > os.path.getmtime(py)
        else:
            convert = True
        if convert:
            os.system('pyrcc4 -o %s %s'%(py, rc))
            logger.debug('converted %s'%rc)

def ui2py(dir):
    """If .ui files are present, xpaxs is being run in development mode. In that
    case, convert .ui files to .py files.
    """
    for ui in glob.glob(dir+'/*.ui'):
        py = os.path.splitext(ui)[0]+'.py'
        if os.path.isfile(py):
            convert = os.path.getmtime(ui) > os.path.getmtime(py)
        else:
            convert = True
        if convert:
            converted = os.system('pyuic4 -o %s %s'%(py, ui))
            if converted == 0:
                logger.debug('converted %s'%ui)
            else:
                logger.error('could not find pyuic4')
