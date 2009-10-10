Phynx
+++++

============
Introduction
============

Phynx is a high-level interface to HDF5 files, using the h5py bindings
to the the HDF5 library. HDF5 is an open-source binary format designed
for scientific data, it allows you to organize your data in an
hierarchy similar to a filesystem. It is fair to think of HDF5 as a
file system for large, complex data. Phynx provides access to such
datasets without storing the entire file in memory, thus it is easy to
work with multi-gigabyte files on a computer with limited RAM.

Phynx offers additional object oriented routines designed to make it
easier to work with the kind of data generated at synchrotron labs.
Its organization is inspired in part by the NeXus_ format. The NeXus
project has the laudable goal of bridging the gap between experimental
and theoretical research initiatives, and phynx does not intend to
subvert the NeXus project. Rather, phynx is designed to provide a
simple interface for organizating and working with synchrotron data,
including the standard NeXus hierarchy and full instrument definition,
if so desired. The phynx routines are designed to provide an
extensible interface to your data that is hopefully intuitive and
simple to use.

==============
Exporting data
==============

Naturally, you will feel more comfortable storing your data in the
HDF5 format if you understand how to get it back out. So before we get
into how to get your data into the HDF5 format and how to work with it
using phynx, here is a quick example of how to export data back out of
phynx. Imagine you have a file with the following standard format::

  mydata.h5
    /entry_1/measurement/scalar_data/motor_1
                                     motor_2
                                     ion_chamber_1
                        /MCA/counts
                             deadtime

and you want to export channels 500-550 of the first three MCA spectra
to an ASCII text file. You can do so with the following simple python
code, which can be run as a script or in an interactive session::

  from phynx import File
  import numpy

  f = File('mydata.h5')
  mca_spectra = f['/entry_1/measurement/MCA/counts'][:3, 500:551]
  numpy.savetxt('mca_spectra.txt', mca_spectra, fmt='%g')

If you don't know how to run a python script, try reading the
tutorial_ at the `python website`_. For working with data
interactively, have a look at the IPython_ package. If you don't know
what `fmt='%g'` meant, you can find an explanation in the python
documentation for `string formatting`_.

Now, lets move on to the full documantation.

.. _NeXus: http://www.nexusformat.org
.. _tutorial: http://docs.python.org/tutorial/
.. _`python website`: http://www.python.org
.. _IPython: http://ipython.scipy.org
.. _`string formatting`: http://docs.python.org/library/stdtypes.html#string-formatting

.. toctree::
   :maxdepth: 2

   users/index
   devel/index
   glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

