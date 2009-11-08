************
Installation
************

Prerequisites
=============

XPaXS requires several packages in order to run. Many of these
packages can be easily installed on Linux using the distributions
package manager, which will also take care of dependencies. Note
to windows users: you need to install the 32-bit python and
32-bit package installers, and you may need to run .exe files as
administrator (just right-click on them and choose "run as
Administrator"). Install in the following order:

#. Python_ (version 2.5 or 2.6)
#. NumPy_ (version 1.3 or later)
#. PyQt4_ (version 4.6.2 or later) [#f1]_
#. PyQwt_ (version 5.2.1 or later, Required by PyMca.)
#. PyMca_ (version 4.3.1 or later)
#. matplotlib_ (0.99.1 or later)
#. ParallelPython_ (version 1.5.7 or later)
#. h5py_ (1.2.0 or later) [#f2]_
#. phynx_ (0.10.0 or later)
#. XPaXS_

To install XPaXS on linux, the easiest approach is to use your
distribution's package manager to install the dependencies. On
several linux distributions, like Ubuntu, you may need to install the
developer tools and -dev packages in order to use XPaXS, for example
pyqt4-dev and pyqt4-dev-tools. You may also need to install
hdf5-1.8.3 and the hdf5-dev packages before installing h5py and phynx.
If you have trouble installing python-qwt5-qt4 on debian/ubuntu, see
this comment_ at the bug report or contact D.Dale for assistance. To
install XPaXS itself, download the source, unpack it, and run the
following in the source directory::

  python setup.py build && sudo python setup.py install

Developers installation
=======================

XPaXS developers may also want to install:

* bzr_ (version 2.0.0 or later)
* distribute_ (version 0.6.8 or later)
* sphinx_ (version 0.6.3 or later)
* nose_ (version 0.11 or later)

You can follow and contribute to XPaXS' development by obtaining a
bzr version control branch with the following command::

  bzr branch lp:xpaxs

That will create an xpaxs project directory for you. Python-2.6 will
run code right from that directory if you run the following command::

  python setup.py develop --user

then periodically bring your branch up to date::

  bzr pull

and the changes are immediately available to you without having to
reinstall anything.

Bugs, feature requests, and questions can be directed to the
`xpaxs development page`_.

.. rubric:: Footnotes

.. [#f1] May require installing Qt_ on Mac, and development tools
   like pyqt4-dev-tools through the package manager on Linux
.. [#f2] May require installing hdf5-1.8.3 or later on linux and Mac,
   and development libraries like libhdf5-dev through the package
   manager on linux


.. _Python: http://www.python.org/
.. _bzr: http://bazaar-vcs.org/en/
.. _distribute: http://pypi.python.org/pypi/distribute
.. _sphinx: http://pypi.python.org/pypi/Sphinx
.. _nose: http://pypi.python.org/pypi/nose
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _PyQt4: http://pypi.python.org/pypi/PyQt
.. _SIP: http://pypi.python.org/pypi/SIP
.. _Qt: http://qt.nokia.com/
.. _matplotlib: http://pypi.python.org/pypi/matplotlib
.. _PyMca: http://pypi.python.org/pypi/PyMca
.. _PyQwt: http://pyqwt.sourceforge.net/
.. _ParallelPython: http://pypi.python.org/pypi/pp
.. _h5py: http://pypi.python.org/pypi/h5py
.. _phynx: http://pypi.python.org/pypi/phynx
.. _XPaXS: http://pypi.python.org/pypi/xpaxs
.. _`xpaxs development page`: https://launchpad.net/xpaxs
.. _comment: https://bugs.edge.launchpad.net/ubuntu/+source/pyqwt5/+bug/342782/comments/12

