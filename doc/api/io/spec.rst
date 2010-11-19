:mod:`spec` --- Core tools for reading spec data files
======================================================

.. module:: praxes.io.spec
   :synopsis: Core tools for reading spec data files.
.. moduleauthor:: Darren Dale <dsdale24@gmail.com>

The :mod:`spec` module provides an interface to data stored in files created
by Certified Scientific's "spec" program.

Files are opened using the the :func:`open` function, which returns a read-only
dictionary-like interface to the scans contained in the file::

   >>> from praxes.io import spec

   >>> f = spec.open('spec_file.dat')


Each scan is also
a read-only dictionary-like interface to the scalar and vector data.

At the top of the :mod:`spec` hierarchy is the :class:`ReadOnlyDict` class,
which provides a dictionary interface similar to the dictionaries in python-3.
Extending :class:`ReadOnlyDict` is :class:`SpecFile`, which scans the file and
creates an index of available scans::

   >>> f.keys()
   dict_keys(['1'])

   >>> scan = f['1']

:meth:`SpecFile.update` is provided to update the file's index in the event
that data has been appended to the file.

Also extending :class:`ReadOnlyDict` is :class:`SpecScan`, which scans a
portion of the file and creates an index of available datasets and metadata::

   >>> scan.keys()
   dict_keys(['motor1', 'Epoch', 'Seconds', 'counter'])

Ordinary dictionary access of :class:`SpecScan` yields proxies to the
underlying data, which can be indexed to yield in-memory copies of the data::

   >>> counter = scan['counter'] # counter is a proxy, no data has been loaded
   >>> counter[...]
   array([100, 101, 102])
   >>> counter[0]
   100

:attr:`SpecScan.data` provides another means of accessing the scalar data::

   >>> scan.data[:, 0] # return the first column of data
   >>> scan.data[3, :] # return the fourth row of data

Note that vector data (keys starting with "@") is not accessible using this
mechanism.

If data has been appended to the file, the existing proxies will reflect this
change::

   >>> f.update() # or scan.update()
   >>> counter[...]
   array([100, 101, 102, 103])

Note, however, that the indices for the file and the scans are not completely
reconstructed. They are only updated based on the assumption that data has only
been appended to the file, and that any existing data in the file has not been
modified.

:class:`SpecScan` stores scan metadata in a read-only dictionary, which can be
accessed using the :attr:`SpecScan.attrs` attribute::

   >>> scan.attrs.keys()
   dict_keys(['command', 'date'])
   >>> scan.attrs['command']
   'dscan motor1 -1 1 10 1'


Module Interface
----------------

.. function:: open(file_name)

   Open *file_name* and return a read-only dictionary-like interface.  If the
   file cannot be opened, an :exc:`IOError` is raised.

   *lock* can be *True* to protect access with a recursive lock from python's
   threading library. An instance of an alternative recursive lock implementation can
   be provided, but it must have acquire() and release() methods, and must support
   python's context management protocol (must have __enter__() and __exit__()
   methods).


.. class:: ReadOnlyDict

   The base class for all :mod:`spec` dictionary-like access to read-only data.

   .. describe:: len(d)

      Return the number of items in the dictionary *d*

   .. describe:: d[key]

      Return the item of *d* with key *key*. Raises a :exc:`KeyError` if *key*
      is not in *d*.

   .. describe:: key in d

      return ``True`` if *d* has a key *key*, else ``False``.

   .. method:: get(key[, default=None])

      Return the value for *key*, or return *default*

   .. method:: keys()

      Return a new view of the keys.

   .. method:: items()

      Return a new view of the ``(key, value)`` pairs.

   .. method:: values()

      Return a new view of the values.


.. class:: SpecFile

   A class providing high-level access to scans stored in a "spec" data file.
   It inherits :class:`ReadOnlyDict`.

   .. method:: update()

      Updates the file's index of scans in the file, if necessary. Also updates
      the indices for the scans in the file.


.. class:: SpecScan

   A class providing high-level access to datasets associated with a scan in a
   "spec" data file. It inherits :class:`ReadOnlyDict`.

   .. attribute:: attrs

      A :class:`ReadOnlyDict` instance containing the metadata for the scan.

   .. attribute:: data

      A proxy providing access to the scan's scalar data.

   .. method:: update()

      Updates the scan's index of the data in the file, if necessary.