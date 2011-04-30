=============================================================
:mod:`phynx` --- Object-oriented interface to hdf5 data files
=============================================================

.. module:: praxes.io.phynx
   :synopsis: Object-oriented interface to domain-specific hdf5 data files.
.. moduleauthor:: Darren Dale <dsdale24@gmail.com>

Introduction
============

Phynx is a high-level interface to HDF5 files, built around the h5py bindings
to the the HDF5 library. HDF5 is an cross-platform, open-source, binary file
format designed for scientific data, allowing data to be organized in an
hierarchy similar to the directories and files on a filesystem. It is fair to
think of HDF5 as a file system for large, complex data. HDF5 provides access to
data without loading the entire file in memory, thus it is easy to work with
multi-gigabyte files on a computer with limited RAM.

Phynx offers a useful and intuitive object oriented interface designed to make
it easier to work with the kind of data generated at synchrotron labs. The
files are organized into a simple hierarchy that attempts to provide sufficient
context for interpretation and processing.

The phynx file organization attempts to provide compatibility with the NeXus_
format. NeXus strives to provide a common exchange format for data generated at
synchrotron and neutron facilities, using the NeXus API to interact with data
stored in either XML or HDF5 files. NeXus application definitions play a major
role in the "universality" of a NeXus file.

Many experiments, however, do not involve a well-defined application. They may
involve combinations of application definitions, or instrumentation may need to
be adapted to experimental necessity in ways that diverge from a well-defined
application definition. Phynx is not necessarily suitable as a common exchange
format. Rather, its design is based on a flexible, time-tested way to organize
data which simplifies real-time analysis routines and allows data to be
interpret in some other context not envisioned by a well-defined application
definition. Data in phynx files can easily be exported into a more
domain-specific common exchange format.


Exporting data
==============

Naturally, you will feel more comfortable storing your data in the HDF5 format
if you know how to export it to another familiar format. Imagine you have a
file with the following standard format::

  mydata.h5
    /entry_1/measurement/scalar_data/motor_1
                                     motor_2
                                     ion_chamber_1
                        /MCA/counts
                             deadtime

and you want to export channels 500-550 of the first three MCA spectra to an
ASCII text file. You can do so with the following simple python code, which can
be run as a script or in an interactive session::

  from praxes.io.phynx import File
  import numpy

  f = File('mydata.h5')
  mca_spectra = f['/entry_1/measurement/MCA/counts'][:3, 500:551]
  numpy.savetxt('mca_spectra.txt', mca_spectra, fmt='%g')

Since we didnt need any of phynx special features, I could have done
`from h5py import File` instead.

If you don't know how to run a python script, try reading the tutorial_ at the
`python website`_. For working with data interactively, have a look at the
IPython_ package. If you don't know what `fmt='%g'` meant, you can find an
explanation in the python documentation for `string formatting`_.


.. _NeXus: http://www.nexusformat.org
.. _tutorial: http://docs.python.org/tutorial/
.. _`python website`: http://www.python.org
.. _IPython: http://ipython.scipy.org
.. _`string formatting`: http://docs.python.org/library/stdtypes.html#string-formatting
