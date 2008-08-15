"""spec is a graphical client interface to the spec data acquisition program,
based on the SpecClient library developed by Matias Guijarro at the ESRF and Qt
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

import SpecClient

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import config

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

logfile = os.path.join(config.getUserConfigDir(), 'specclient.log')
SpecClient.setLogFile(logfile)

TEST_SPEC=False

def setSPEC(bool):
    TEST_SPEC=bool
