************
Installation
************

Prerequisites
=============

XPaXS requires several packages in order to run:

* Python_ (2.5 ≤ version < 3.0) Windows users: Please install the 32 bit
  version of python-2.6.x, even if your computer is 64-bit.
* NumPy_ (version 1.3 or later)
* PyQt4_ (preferrably version 4.4.4 or later)
* PyQwt_ (version 5.2.0 or later)
* PyMca_ (version 4.3.1 or later) Please be sure to use the windows installer
  includes your python version in the name (like PyMca-4.3.0.win32-py2.5.exe).
  Windows users: You may need to right-click on the installer and select "run
  as administrator"
* matplotlib_ (0.98.5.2 or later) Windows users: you may need to right-click on
  the installer and select "run as administrator"
* ParallelPython_ (version 1.5.7 or later) Note: please install from one of the
  .zip or .tgz source files, **not** the .exe file and not using easy_install.
  There is a bug with the later two installers. Just unzip the sources, cd into
  the new directory and run "python setup.py install".
* h5py_ (1.1 or later)
* XPaXS_ Windows users: you may need to right-click on the installer and select
  "run as administrator".

On several distributions, like Ubuntu, you may need to install the developer
tools and -dev libraries in order to use XPaXS.

XPaXS developers may also want to install:

* setuptools_ (version 0.6c8 or later)
* sphinx_ (version 0.6.1 or later)

Linux and OSX
=============

To install XPaXS on linux and OSX, download the XPaXS sourcecode from PyPi_
and run "python setup.py install" in the xpaxs source directory.

Windows
=======

A 32-bit windows installer is available at PyPi_. It requires the 32-bit python
installation, even on a 64-bit machine, since most 3rd-party modules (like numpy
and PyQt4) are compiled for the 32-bit platform.

Development Branch
==================

You can follow and contribute to XPaXS' development by obtaining a bzr version
control branch. Just install bzr and type::

  bzr branch lp:xpaxs

and then periodically bring your branch up to date::

  bzr pull

Bugs, feature requests, and questions can be directed to the launchpad_
website.


.. _Python: http://www.python.org/
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _sphinx: http://sphinx.pocoo.org/
.. _NumPy: http://www.scipy.org
.. _PyQt4: http://www.riverbankcomputing.com/software/pyqt/intro
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _PyMca: http://pymca.sourceforge.net/
.. _PyQwt: http://pyqwt.sourceforge.net/
.. _ParallelPython: http://www.parallelpython.com
.. _h5py: http://code.google.com/p/h5py/
.. _PyPi: http://pypi.python.org/pypi/xpaxs
.. _XPaXS: http://pypi.python.org/pypi/xpaxs
.. _launchpad: https://launchpad.net/xpaxs
