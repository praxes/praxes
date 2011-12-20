# -*- coding: utf-8 -*-
'''
The elam module is an interface to a database of fundamental X-ray fluorescence
parameters compiled by W.T. Elam, B.D. Ravel and J.R. Sieber, and published in
Radiation Physics and Chemistry, 63 (2), 121 (2002). The database is published
by NIST at http://www.nist.gov/mml/analytical/inorganic/xrf.cfm.
'''

from .atomicdata import AtomicData
atomic_data = AtomicData()
