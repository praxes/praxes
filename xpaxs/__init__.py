"""
XPaXS -- Extensible Packages for X-ray Science

XPaXS is a collection of python packages and libraries for X-ray Science. XPaXS
was developed with the hope that it many will find it useful, and many will
contribute to --- and take credit for --- its development.

This project began with the goal of providing useful real-time feedback and
analysis of scanning X-ray fluorescence microscopy experiments, using several
existing and very successful libraries such as PyMca, SpecClient, Matplotlib,
PyQt4, NumPy, PyTables, and ParallelPython. It quickly became clear, however,
that due to the object-oriented nature of the Python language, with a little
abstraction XPaXS was poised to provide a framework for X-ray science in
general.

XPaXS is therefore divided into several subpackages:

:mod:`xpaxs.config`
    Configuration utilities for the xpaxs package

:mod:`xpaxs.core`
    Intended to provide the core scientific support, such as physical constants,
    interactions of X-rays with matter, X-ray sources and optics, etc.

:mod:`xpaxs.dispatch`
    Provides support for concurrent processing, using multi-core computers and
    computer clusters

:mod:`xpaxs.frontend`
    Where the main user interfaces are assembled from xpaxs and external
    libraries

:mod:`xpaxs.instrumentation`
    Provides the interface to beamline instrumentation hardware and software

:mod:`xpaxs.io`
    Support for data input/output

XPaXS is developed primarily in Python, but it relies heavily on libraries and
extension code written in C and C++. It is often the case that we have to
analyze massive datasets, which can place high demands physical memory, disk
space, and read/write speed. We therefore decided to use hdf5 and pytables for
data management and storage, and we inted to format our datafiles according to
the NeXus standard, which is rapidly gaining acceptance in the synchrotron and
neutron communities. Finally, we decided to use PyQt4 for event-based
programming and developing graphical user interfaces. PyQt4 is a python binding
to the modern and very actively developed Qt4 GUI toolkit, which is written in
C++.

XPaXS is open source software. XPaXS and all of its dependencies are compatible
with the GNU Public License.

"""

import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import logging.config
import logging.handlers
import os

from xpaxs import config

from xpaxs.release import __version__

# One of DEBUG, INFO, WARNING, ERROR, CRITICAL:
logLevel = DEBUG

logger = logging.getLogger("XPaXS")
logger.setLevel(logLevel)
logFile = os.path.join(config.getUserConfigDir(), 'xpaxs.log')
handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=10000,
                                               backupCount=5)
handler.setLevel(logLevel)

if logLevel == DEBUG:
    fmtString = """\
=== %(asctime)s - %(name)s ===
%(funcName)s, line %(lineno)d
%(levelname)s: %(message)s"""
else:
    fmtString = """\
=== %(asctime)s - %(name)s ===
%(levelname)s: %(message)s"""

formatter = logging.Formatter(fmtString)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Initial XPaXS import")
