:mod:`praxes.physref.elam`
==========================

The :mod:`elam` module provides an interface to the Elam x-ray database.
Elements are accessed using :attr:`atomic_data`, which provides a mapping to
the element data::

   >>> from praxes.physref import elam
   >>> copper = elam.atomic_data['Cu']
   >>> print(copper.atomic_number)
   29

Each element provides a mapping to the x-ray states reported in the Elam
database::

   >>> print(copper.keys())
   ['K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5']
   >>> print(copper['K'].fluorescence_yield)
   0.441091

Each x-ray state provides a mapping to the transitions originating from that
state::

   >>> print(copper['K'].keys())
   ['L1', 'L2', 'L3', 'M2', 'M3', 'M4,5']
   >>> print(copper['K']['L3'].iupac_symbol)
   'K-L3'

There is also a set of top-level functions in the :mod:`elam` module for
calculating some simple properties of compositions, including conversions
between stoichiometry and mass fractions, photoabsorption cross section,
transmission and attenuation.

Note, in multithreading environments, there are issues sharing sqlite data
between threads. As a result, objects arising from a given instance of
:class:`AtomicData`, such as :attr:`atomic_data`, should not be shared between
threads. Instead, you should create a new instance of :class:`AtomicData` in
each thread to access the data.


Module Interface
----------------

.. automodule:: praxes.physref.elam

.. autoclass:: praxes.physref.elam.atomicdata.AtomicData
   :members:
   :inherited-members:

.. autoclass:: praxes.physref.elam.element.Element
   :members:
   :inherited-members:

.. autoclass:: praxes.physref.elam.xraylevel.XrayLevel
   :members:
   :inherited-members:

.. autoclass:: praxes.physref.elam.transition.Transition
   :members:
   :inherited-members:


Composition Functions
+++++++++++++++++++++

.. autofunction:: praxes.physref.elam.mass_fraction_to_stoichiometry

.. autofunction:: praxes.physref.elam.stoichiometry_to_mass_fraction

.. autofunction:: praxes.physref.elam.photoabsorption_cross_section

.. autofunction:: praxes.physref.elam.transmission_coefficient

.. autofunction:: praxes.physref.elam.absorption_coefficient
