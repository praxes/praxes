:mod:`praxes.physref.waasmaier`
===============================

The :mod:`waasmaier` module provides an interface to the energy-independent
atomic form factors, as calculated by D. Waasmaier and A. Kirfel in Acta.
Cryst. vA51, p416 (1995). The calculations take the form

.. math::

   f_0(s) = \sum_{i=0}^{5} a_i e^{-b_i s^2} + c

This approximation is valid for :math:`s ≤ 6 \AA^{-1}`, or
:math:`|Q| ≤ 75 \AA^{-1}`.

Atomic form factors accessed using :attr:`atomic_data`::

   >>> from praxes.physref.waasmaier import atomic_data
   >>> import quantities as pq
   >>> f0 = atomic_data['O']
   >>> print f0(0 * 1/pq.angstrom)
   7.99706
   >>> print f0([0,1,2] * 1/pq.angstrom)
   array([ 7.999706  ,  7.50602869,  6.31826029])
   >>> f0 = atomic_data['O2-']
   >>> print f0(0* 1/pq.angstrom)
   9.998401

Module Interface
----------------

.. automodule:: praxes.physref.waasmaier

.. autoclass:: praxes.physref.waasmaier.atomicdata.AtomicData
   :members:
   :inherited-members:

.. autoclass:: praxes.physref.waasmaier.atomicdata.FormFactor
   :members:
   :inherited-members:
