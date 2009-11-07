************
Installation
************

Prerequisites
=============

XPaXS requires several packages in order to run. Note to windows 
users: you need to install the 32-bit python and 32-bit package 
installers, and you may need to run .exe files as administrator
(just right-click on them and choose "run as Administrator").

* Python_ (version 2.5 or 2.6)
* NumPy_ (version 1.3 or later)
* PyQt4_ (version 4.6.2 or later)
* PyQwt_ (version 5.2.1 or later, Required by PyMca.)
* PyMca_ (version 4.3.1 or later)
* matplotlib_ (0.99.1 or later)
* ParallelPython_ (version 1.5.6 or later)
* h5py_ (1.2.0 or later, required by phynx)
* phynx_ (0.10.0 or later)
* XPaXS_

To install XPaXS on linux, the easiest approach is to use your
distribution's package manager to install the dependencies. On
several linux distributions, like Ubuntu, you may need to install the
developer tools and -dev packages in order to use XPaXS, for example
pyqt4-dev-tools. If you have trouble installing python-qwt5-qt4 on
debian/ubuntu, see this comment_ at the bug report or contact D.Dale
for assistance. To install XPaXS itself, download the source, unpack
it, and run the following in the source directory::

  python setup.py build && sudo python setup.py install

XPaXS developers may also want to install:

* distribute_ (version 0.6.8 or later)
* sphinx_ (version 0.6.3 or later)
* nose_ (version 0.11 or later)

.. _Python: http://www.python.org/
.. _distribute: http://pypi.python.org/pypi/distribute
.. _sphinx: http://sphinx.pocoo.org/
.. _NumPy: http://www.scipy.org
.. _PyQt4: http://www.riverbankcomputing.com/software/pyqt/download
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _PyMca: http://pymca.sourceforge.net/
.. _PyQwt: http://pyqwt.sourceforge.net/
.. _ParallelPython: http://www.parallelpython.com
.. _h5py: http://code.google.com/p/h5py/
.. _phynx: http://packages.python.org/phynx/
.. _XPaXS: http://pypi.python.org/pypi/xpaxs
.. _comment: https://bugs.edge.launchpad.net/ubuntu/+source/pyqwt5/+bug/342782/comments/12

Development Branch
==================

You can follow and contribute to XPaXS' development by obtaining a
bzr version control branch. Just install bzr and type::

  bzr branch lp:xpaxs

and then periodically bring your branch up to date::

  bzr pull

Bugs, feature requests, and questions can be directed to the
launchpad_ website.

.. _launchpad: https://launchpad.net/xpaxs
