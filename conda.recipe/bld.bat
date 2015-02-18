REM %PYTHON% praxes/physref/elam/create_db praxes/physref/elam/elam.dat praxes/physref/elam/elam.db
REM %PYTHON% praxes/physref/waasmaier/create_db praxes/physref/waasmaier/waasmaier_kirfel.dat praxes/physref/waasmaier/waasmaier_kirfel.db

%PYTHON% setup.py build

%PYTHON% setup.py install --old-and-unmanageable
if errorlevel 1 exit 1

REM copy scripts\* %SCRIPTS%\
REM if errorlevel 1 exit 1
