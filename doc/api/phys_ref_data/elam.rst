:mod:`praxes.phys_ref_data.elam`
================================

The :mod:`elam` module provides an interface to the Elam x-ray database.
Elements are accessed using :attr:`atomic_data`, which provides a read-only
dictionary-like interface to the element data::

   >>> from praxes.phys_ref_data.elam import atomic_data
   >>> copper = atomic_data['Cu']
   >>> print(copper.atomic_number)
   29
   >>> print(copper.keys())
   ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5']

Each element provides a read-only dictionary-like interface to the x-ray states
reported in the Elam database::

   >>> print(copper['K'].fluorescence_yield)
   0.441091
   >>> print(copper['K'].keys())
   ['L1', 'L2', 'L3', 'M2', 'M3', 'M4,5']

Each x-ray state provides a read-only dictionary-like interface to the
transitions originating from that state::

   >>> print(copper['K']['L3'].iupac_symbol)
   'K-L3'

Note, in multithreading environments, there are issues sharing sqlite data
between threads. As a result, objects arising from a given instance of
:class:`AtomicData`, such as :attr:`atomic_data`, should not be shared between
threads. Instead, you should create a new instance of :class:`AtomicData` in
each thread to access the data.


Module Interface
----------------

.. automodule:: praxes.phys_ref_data.elam
   :members:
