"""Traits-based declaration for SMP configuration.
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import enthought.traits.api as T

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

import smptraits as smpT
import cutils
from tconfig import TConfig, TConfigManager, tconf2File

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


DEBUG = False


class SmpConfig(TConfig):
    """
    This is a sample smp configuration file.  It should be placed
    in HOME/.spectromicroscopy/smp.conf.

    By default, the installer will overwrite the existing file in the install
    path, so if you want to preserve yours, please move it to your HOME dir and
    set the environment variable if necessary.

    This file is best viewed in a editor which supports ini or conf mode syntax
    highlighting.

    Blank lines, or lines starting with a comment symbol, are ignored,
    as are trailing comments.  Other lines must have the format

      key = val   optional comment

    val should be valid python syntax. This should become more obvious by 
    inspecting the default values listed herein.

    ### CONFIGURATION BEGINS HERE ###
    """

    class session(TConfig):
        """Valid ports are something like 'spec', 'fourc', etc."""
        port = T.Str('')
        server = T.Str('')


configManager = TConfigManager(SmpConfig,
                               cutils.getSmpConfigFile(), 
                               filePriority=True)
smpConfig = configManager.tconf

def saveConfig():
    """Save mplConfig customizations to current matplotlib.conf
    """
    configManager.write()

