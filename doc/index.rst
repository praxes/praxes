=====
Phynx
=====

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
project has the ambitious goal of bridging the gap between
experimental and theoretical research initiatives, and phynx does not
intend to subvert the NeXus project. Rather, phynx is designed to
provide a simple interface for organizating and working with
synchrotron data, including the standard NeXus hierarchy and full
instrument definition, if so desired. The phynx routines are designed
to provide an extensible interface to your data that is intuitive and
simple to use.

.. _NeXus: http://www.nexusformat.org

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

