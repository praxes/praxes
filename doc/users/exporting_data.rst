
==============
Exporting data
==============

Naturally, you will feel more comfortable storing your data in the
HDF5 format if you understand how to get it back out. Imagine you have
a file with the following hierarchy::

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
