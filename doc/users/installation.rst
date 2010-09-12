============
Installation
============

Praxes requires several packages in order to run. Many of these
packages can be easily installed on Linux using the distribution's
package manager, which will also take care of dependencies. Note
to windows users: you need to install the 32-bit python and 32-bit
package installers, and you may need to run .exe files as
administrator (just right-click on them and choose "run as
Administrator"). Check that you have the following installed:

#. Python_ (version 2.6)
#. PyQt4_ (version 4.7.6 or later) [#f1]_
#. dip_ (version 0.2 or later)
#. NumPy_ (version 1.4.1 or later)
#. PyMca_ (version 4.5.0 or later) [#f2]_
#. matplotlib_ (0.98.3 or later)
#. h5py_ (1.3.1 or later) [#f3]_
#. Praxes_

To install Praxes on OS X or Linux, download the source, unpack it, and
run the following in the source directory::

  python setup.py build && sudo python setup.py install


.. rubric:: Footnotes

.. [#f1] May require installing Qt_ on Mac, and development tools
   like pyqt4-dev and pyqt4-dev-tools through the package manager on
   Linux.
.. [#f2] Windows users, please install the file that includes the python
   version in the name: e.g. PyMca-4.4.0.win32-py2.6.exe. Mac and Linux
   users, please install from source: e.g. pymca4.5.0-src.tgz.
.. [#f3] May require installing hdf5-1.8.5 or later on Linux and OS X,
   and development libraries like libhdf5-dev through the package
   manager on linux.


.. _Python: http://www.python.org/
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt
.. _Qt: http://qt.nokia.com/
.. _dip: http://www.riverbankcomputing.co.uk/software/dip
.. _matplotlib: http://pypi.python.org/pypi/matplotlib
.. _PyMca: http://pypi.python.org/pypi/PyMca
.. _h5py: http://pypi.python.org/pypi/h5py
.. _Praxes: http://pypi.python.org/pypi/praxes
