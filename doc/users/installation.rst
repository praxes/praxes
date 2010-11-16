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
#. NumPy_ (version 1.4.1 or later)
#. Praxes_

To install Praxes on OS X or Linux, download the source tar.gz file, unpack it,
and run the following in the source directory::

  python setup.py build && sudo python setup.py install


.. _Python: http://www.python.org/
.. _Cython: http://pypi.python.org/pypi/Cython
.. _NumPy: http://pypi.python.org/pypi/numpy
.. _Praxes: http://github.com/praxes/praxes/downloads
