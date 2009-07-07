************
Installation
************

If you are using the Windows operating system, see the instructions below for 
:ref:`windows-installations`.

Prerequisites
=============

XPaXS requires several packages in order to run (this list applies to Linux
and Mac, Windows users see :ref:`windows-installations`):

* Python_ (version 2.5 or 2.6)
* NumPy_ (version 1.3 or later)
* PyQt4_ (version 4.4.3 or later)
* PyQwt_ (version 5.1.0 or later. If you have PyQt4-4.5.1 or later, you must 
  use PyQwt-5.2.0 or later, which will not be released until July 2009. In
  the interim, you may install using a cvs checkout of the development branch. 
  Contact D.Dale for assistance.)
* PyMca_ (version 4.3.1 or later, which may be released during Summer 2009. In
  the interim, you may install using an svn checkout of the development branch. 
  Contact D.Dale for assistance.)
* matplotlib_ (0.98.5 or later)
* ParallelPython_ (version 1.5.6 or later)
* h5py_ (1.1 or later)
* XPaXS_

On several distributions, like Ubuntu, you may need to install the developer
tools and -dev packages in order to use XPaXS, for example pyqt4-dev-tools. If
you have trouble installing python-qwt5-qt4 on debian/ubuntu, see this comment_
at the bug report or contact D.Dale for assistance.

XPaXS developers may also want to install:

* setuptools_ (version 0.6c8 or later)
* sphinx_ (version 0.6.1 or later)

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
.. _comment: https://bugs.edge.launchpad.net/ubuntu/+source/pyqwt5/+bug/342782/comments/12

Linux and OSX
=============

To install XPaXS on linux and OSX, download the XPaXS sourcecode from PyPi_,
unpack it and run "python setup.py install" in the xpaxs source directory.

.. _windows-installations:

Windows Installations
=====================

Software development is a bit more difficult in a Windows environment than it
is if you use Mac or Linux. A few of XPaXS' dependencies are not yet 
compatible with 64-bit versions of Python, and a few are not quite ready for 
use with python-2.6. You can still use XPaXS with Python-2.5 without any loss 
of functionality, just be sure to use the following prerequisites. Windows 
Vista users may need to right click on the installers and select "run as 
administrator".

* `Python-2.5.4`_ (version 2.5.4 for 32-bits, even if you have a 64-bit
  processor. Several of XPaXS dependencies are not yet compatible with
  python-2.6 or python-3 on Windows, you must have 32-bit python-2.5 for now.)
* `NumPy-1.3.0`_
* `PyQt4-4.4.3-1`_
* `PyQwt-5.1.0`_ (do not worry that the name of the installer indicates
  numpy-1.2.)
* `PyMca-4.3.1_snapshot`_
* `matplotlib-0.98.5.3`_
* `ParallelPython-1.5.7`_
* `h5py-1.2`_
* `XPaXS-0.9`_

Once you have installed these packages, you can launch xpaxs from your start
menu as you would any other program.

.. _`Python-2.5.4`: http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi
.. _`NumPy-1.3.0`: http://sourceforge.net/project/downloading.php?group_id=1369&filename=numpy-1.3.0-win32-superpack-python2.5.exe&a=88448002
.. _`PyQt4-4.4.3-1`: http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-Py2.5-gpl-4.4.3-1.exe
.. _`matplotlib-0.98.5.3`: http://sourceforge.net/project/downloading.php?group_id=80706&filename=matplotlib-0.98.5.3.win32-py2.5.exe&a=20132040
.. _`PyMca-4.3.1_snapshot`: http://ftp.esrf.eu/pub/bliss/PyMca-4.3.1-20090619-snapshotdev_r758.win32-py2.5.exe
.. _`PyQwt-5.1.0`: http://prdownloads.sourceforge.net/pyqwt/PyQwt5.1.0-Python2.5-PyQt4.4.3-NumPy1.2.0-1.exe
.. _`ParallelPython-1.5.7`: http://www.parallelpython.com/downloads/pp/pp-1.5.7.exe
.. _`h5py-1.2`: http://h5py.googlecode.com/files/h5py-1.2.0.win32-py2.5.msi
.. _`XPaXS-0.9`: http://pypi.python.org/packages/2.5/x/xpaxs/xpaxs-0.9.win32.exe#md5=3aeeec067d3da8d7b5039caefbab5a25

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
