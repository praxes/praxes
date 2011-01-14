All code is currently tailored for the analysis of XRD/XRF data from the Cornell High Energy Source.

The *.ui files were generated with Qt Designer.

The file XRDdefaults.py must be customized for each user. It contains several local hard disc paths. All paths must exist for the relevant functionality of the program - the most important file is maps_attrs.h5 which contains analysis tools specific to experiment geometry.

The files have been wrapped into an Eric4 project, but after downloading the files, the program is run be executing "mainprogram.py" in a Python interpreter.

JM Gregoire
20 June 2010