:mod:`spec` --- Core tools for reading spec data files
======================================================

.. module:: praxes.io.spec
   :synopsis: Core tools for reading spec data files.
.. moduleauthor:: Darren Dale <dsdale24@gmail.com>

Module Interface
----------------

.. function:: open(file_name)

   Open *file_name* and return a read-only dictionary-like interface.  If the
   file cannot be opened, an :exc:`IOError` is raised.
