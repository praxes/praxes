=====
Phynx
=====

Phynx is a high-level interface to HDF5_ files, using the h5py bindings
to the the HDF5 library. HDF5 is an open-source binary format designed
for scientific data. The structure of an HDF5 file is analogous to a
file system, where you can designate an hierarchy of groups
(directories) and datasets (files) to describe data of arbitrary
complexity.

Phynx offers an extensible, object-oriented interface designed to
provide an easy, intuitive way to access and work with data stored in
HDF5 files, whether you are an application developer or working with
your own data in a script or the IPython_ interactive interpreter. The
preliminary focus of Phynx classes is to describe the multifaceted
data produced at synchrotron an neutron facilities, but phynx can be
used to provide rich interfaces to all kinds of data. Its organization
is inspired in part by the NeXus_ format. The NeXus project has the
ambitious goal of providing a standard file hierarchy and component
specification, to bridge the gap between experimental and theoretical
research initiatives and improve our ability to share data. Phynx is
designed to provide an interface that takes advantage of the power and
expressiveness of the Python_ language, the full capability of the HDF5
standard, and support for the standard NeXus hierarchy and instrument
definition, if so desired.

.. _HDF5: http://www.hdfgroup.org/HDF5/
.. _IPython: http://ipython.scipy.org
.. _NeXus: http://www.nexusformat.org
.. _Python: http://www.python.org

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
