"""
spec is a graphical client interface to the spec data acquisition program,
based on the SpecClient library developed by Matias Guijarro at the ESRF and Qt
"""

import os

import SpecClient

from praxes import config


logfile = os.path.join(config.get_user_config_dir(), 'specclient.log')
SpecClient.setLogFile(logfile)

TEST_SPEC = False
USESSH = False

def setSPEC(bool):
    TEST_SPEC = bool

def setSSH(bool):
    USESSH = bool
