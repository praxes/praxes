============
Installation
============

Praxes depends on a few python packages, most of which can be installed on
Linux using the distribution's package manager, or on Mac OS X with MacPorts.
Note to windows users: you currently need to install the 32-bit python and
32-bit package installers, and you may need to run .exe installers as
administrator by right-clicking on them and choose "run as Administrator").
Check that you have the following installed:

#. Python_ (version 2.7)
#. Cython_ (version 0.13 or later, only required for Mac OS X and Linux)
#. NumPy_ (version 1.5.1 or later)
#. PyQt4_ (version 4.5.2 or later) [#f1]_
#. PyMca_ (version 4.4.0 or later, Windows users, please see footnote) [#f2]_
#. matplotlib_ (0.98.3 or later)
#. ParallelPython_ (version 1.6.0 or later)
#. h5py_ (1.3.0 or later) [#f3]_
#. Praxes_

To install Praxes on OS X or Linux, download the source tar.gz file, unpack it,
and run the following in the source directory::

  python setup.py build && sudo python setup.py install


.. rubric:: Footnotes

.. [#f1] May require installing Qt_ on Mac, and development tools
   like pyqt4-dev and pyqt4-dev-tools through the package manager on
   Linux.
.. [#f2] Windows users, please install
   the file that includes the python version in the name: e.g.
   PyMca-4.4.0.win32-py2.6.exe. Mac and linux users please install
   from source: e.g. pymca4.4.0-src.tgz.
.. [#f3] May require installing hdf5 on Linux and OS X, and development
   libraries like libhdf5-dev if installing with a packager manager on
   some linux distributions. hdf5-1.8.4-patch1 is the recommended version.


.. _Python: http://www.python.org/
.. _Cython: http://pypi.python.org/pypi/Cython
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _PyQt4: http://pypi.python.org/pypi/PyQt
.. _Qt: http://qt.nokia.com/
.. _matplotlib: http://pypi.python.org/pypi/matplotlib
.. _PyMca: http://pypi.python.org/pypi/PyMca
.. _ParallelPython: http://pypi.python.org/pypi/pp
.. _h5py: http://pypi.python.org/pypi/h5py
.. _Praxes: http://github.com/praxes/praxes/downloads
