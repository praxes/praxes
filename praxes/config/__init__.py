"""
"""

import glob
import logging
import os
import sys


logger = logging.getLogger('praxes.config')

def get_user_config_dir():
    '''return the path to the user's spectromicroscopy config directory'''
    config_dir = os.path.join(os.path.expanduser('~'), '.praxes')
    if not os.path.exists(config_dir): os.mkdir(config_dir)
    return config_dir

def qrc2py(dir):
    """If .ui files are present, praxes is being run in development mode. In
    that case, convert .ui files to .py files.
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
    """If .ui files are present, praxes is being run in development mode. In
    that case, convert .ui files to .py files.
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
