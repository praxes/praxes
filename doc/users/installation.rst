************
Installation
************

XPaXS requires several packages in order to run. Many of these
packages can be easily installed on Linux using the distribution's
package manager, which will also take care of dependencies. Note
to windows users: you need to install the 32-bit python and 32-bit
package installers, and you may need to run .exe files as
administrator (just right-click on them and choose "run as
Administrator"). Check that you have the following installed:

#. Python_ (version 2.6 on windows, 2.6 or 2.7 for linux/mac)
#. Distribute_ (version 0.6.10 or later)
   or Setuptools (0.6c9 or later) [#f1]_
#. PyQt4_ (version 4.5.2 or later) [#f2]_
#. NumPy_ (version 1.2.0 or later)
#. PyMca_ (version 4.4.0 or later) [#f3]_
#. matplotlib_ (0.98.3 or later)
#. ParallelPython_ (version 1.6.0 or later)
#. h5py_ (1.3.0 or later) [#f4]_
#. phynx_ (0.11.0 or later)
#. XPaXS_

To install XPaXS on OS X or Linux, download the source, unpack it, and
run the following in the source directory::

  python setup.py build && sudo python setup.py install

Developer's installation
========================

XPaXS developers may also want to install:

* git_ (version 2.0.0 or later)
* Sphinx_ (version 1.0.4 or later)
* nose_ (version 0.11 or later)

You can follow and contribute to XPaXS' development by obtaining a
bzr version control branch with the following command::

  git clone git://github.com/darrendale/xpaxs-legacy.git

That will create an xpaxs project directory for you. Python will
run code right from that directory if you run the following command::

  python setup.py develop --user

then periodically bring your branch up to date::

  git pull

and the changes are immediately available to you without having to
reinstall anything.

Bugs, feature requests, and questions can be directed to the
`xpaxs development page`_.

.. rubric:: Footnotes

.. [#f1] Distribute is a fork of the setuptools project. Some Linux
   package managers have not transitioned from setuptools to
   distribute. XPaXS will also work with setuptools.
.. [#f2] May require installing Qt_ on Mac, and development tools
   like pyqt4-dev and pyqt4-dev-tools through the package manager on
   Linux.
.. [#f3] Windows users, please install
   the file that includes the python version in the name: e.g.
   PyMca-4.4.0.win32-py2.6.exe. Mac and linux users please install
   from source: e.g. pymca4.4.0-src.tgz.
.. [#f4] May require installing hdf5-1.8.3 or later on lLnux and OS X,
   and development libraries like libhdf5-dev through the package
   manager on linux.


.. _Python: http://www.python.org/
.. _git: http://git-scm.com
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _Sphinx: http://pypi.python.org/pypi/Sphinx
.. _nose: http://pypi.python.org/pypi/nose
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _PyQt4: http://pypi.python.org/pypi/PyQt
.. _Qt: http://qt.nokia.com/
.. _matplotlib: http://pypi.python.org/pypi/matplotlib
.. _PyMca: http://pypi.python.org/pypi/PyMca
.. _ParallelPython: http://pypi.python.org/pypi/pp
.. _h5py: http://pypi.python.org/pypi/h5py
.. _phynx: http://pypi.python.org/pypi/phynx
.. _XPaXS: http://pypi.python.org/pypi/xpaxs
.. _`xpaxs development page`: http://github.com/darrendale/xpaxs-legacy
