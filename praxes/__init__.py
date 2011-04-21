#import logging
#from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
#import logging.config
#import logging.handlers
#import os
#
#from .config import get_user_config_dir

from .version import __version__

# One of DEBUG, INFO, WARNING, ERROR, CRITICAL:
#logLevel = DEBUG
#
#logger = logging.getLogger("praxes")
#logger.setLevel(logLevel)
#logFile = os.path.join(get_user_config_dir(), 'praxes.log')
#handler = logging.handlers.RotatingFileHandler(
#    logFile, maxBytes=10000, backupCount=5)
#handler.setLevel(logLevel)
#
#if logLevel == DEBUG:
#    fmtString = """\
#    === %(asctime)s - %(name)s ===
#    %(funcName)s, line %(lineno)d
#    %(levelname)s: %(message)s"""
#else:
#    fmtString = """\
#    === %(asctime)s - %(name)s ===
#    %(levelname)s: %(message)s"""
#
#formatter = logging.Formatter(fmtString)
#handler.setFormatter(formatter)
#logger.addHandler(handler)
#
#logger.info("Initial praxes import")
