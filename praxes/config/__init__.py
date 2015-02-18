"""
"""

import glob
#import logging
import os
import sys


#logger = logging.getLogger('praxes.config')

def get_user_config_dir():
    '''return the path to the user's spectromicroscopy config directory'''
    config_dir = os.path.join(os.path.expanduser('~'), '.praxes')
    if not os.path.exists(config_dir): os.mkdir(config_dir)
    return config_dir
