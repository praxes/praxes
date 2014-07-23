%PYTHON% praxes/physref/elam/create_db praxes/physref/elam/elam.dat praxes/physref/elam/elam.db
%PYTHON% praxes/physref/waasmaier/create_db praxes/physref/waasmaier/waasmaier_kirfel.dat praxes/physref/waasmaier/waasmaier_kirfel.db

%PYTHON% setup.py install
if errorlevel 1 exit 1

copy scripts\* %SCRIPTS%\
if errorlevel 1 exit 1
