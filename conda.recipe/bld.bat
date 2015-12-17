git describe --tags --dirty > %SRC_DIR%/__conda_version__.txt
%PYTHON% %RECIPE_DIR%/format_version.py %SRC_DIR%/__conda_version__.txt

%PYTHON% setup.py build

%PYTHON% setup.py install --old-and-unmanageable
if errorlevel 1 exit 1
