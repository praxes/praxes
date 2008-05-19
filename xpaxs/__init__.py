"""
"""
#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import logging.config
import logging.handlers
import os

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs import configutils

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

__version__ = '0.4a1'

# One of DEBUG, INFO, WARNING, ERROR, CRITICAL:
logLevel = DEBUG

logger = logging.getLogger("XPaXS")
logger.setLevel(logLevel)
logFile = os.path.join(configutils.getUserConfigDir(), 'xpaxs.log')
handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=10000,
                                               backupCount=5)
handler.setLevel(logLevel)

if logLevel == DEBUG:
    fmtString = """\
%(asctime)s - %(name)s
%(pathname)s: %(funcName)s, line %(lineno)d
%(levelname)s: %(message)s
"""
else:
    fmtString = """\
%(asctime)s - %(name)s
%(levelname)s: %(message)s
"""

formatter = logging.Formatter(fmtString)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Initial XPaXS import")
