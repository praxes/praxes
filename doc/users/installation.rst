============
Installation
============

Praxes depends on a few python packages, most of which can be installed on
Linux using the distribution's package manager, or on Mac OS X with MacPorts.
Note to windows users:  you may need to run .exe installers as administrator by
right-clicking on them and choose "run as Administrator"). Check that you have
the following installed:

#. Python_ (version 2.6.x or 2.7.x. May already be installed on Linux)
#. Cython_ (version 0.15 or later, only required for Mac OS X and Linux)
#. NumPy_ (version 1.5.1 or later) [#f1]_
#. PyQt4_ (version 4.5.2 or later) [#f2]_
#. PyMca_ (version 4.4.0 or later) [#f3]_
#. matplotlib_ (1.1.0 or later) [#f1]_
#. h5py_ (2.1.0 or later) [#f1]_, [#f4]_
#. quantities_ (optional, only required by physref package)
#. Praxes_

To install Praxes on OS X or Linux, download the source tar.gz file, unpack it,
and run the following in the source directory::

  python setup.py build && sudo python setup.py install


.. rubric:: Footnotes


.. [#f1] Windows installers for 64-bit Python environments can be found
   `here <http://www.lfd.uci.edu/~gohlke/pythonlibs>`_
.. [#f2] May require installing Qt_ on Mac, and development tools
   like pyqt4-dev and pyqt4-dev-tools through the package manager on
   Linux.
.. [#f3] Mac and linux users please install from source: e.g.
   pymca4.4.1-src.tgz. Windows users should follow the `PythonPackages` link,
   and download the file that includes the platform and python version in the
   name: e.g. PyMca-4.4.1.win-amd64-py2.7.exe.
.. [#f4] May require installing hdf5 on Linux and OS X, and development
   libraries like libhdf5-dev if installing with a packager manager on
   some linux distributions.


.. _Python: http://www.python.org/download/releases/2.7.2/
.. _Cython: http://pypi.python.org/pypi/Cython
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _PyQt4: http://pypi.python.org/pypi/PyQt
.. _Qt: http://qt.nokia.com/
.. _matplotlib: http://pypi.python.org/pypi/matplotlib
.. _PyMca: http://sourceforge.net/projects/pymca/files/pymca/PyMca4.4.1
.. _h5py: http://pypi.python.org/pypi/h5py
.. _quantities: http://pypi.python.org/pypi/quantities
.. _Praxes: http://github.com/praxes/praxes/downloads
