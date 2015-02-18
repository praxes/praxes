%PYTHON% setup.py build

%PYTHON% setup.py install --old-and-unmanageable
if errorlevel 1 exit 1
