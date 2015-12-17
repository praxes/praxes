git describe --tags --dirty > $SRC_DIR/__conda_version__.txt
$PYTHON $RECIPE_DIR/format_version.py $SRC_DIR/__conda_version__.txt

$PYTHON praxes/physref/elam/create_db praxes/physref/elam/elam.dat praxes/physref/elam/elam.db
$PYTHON praxes/physref/waasmaier/create_db praxes/physref/waasmaier/waasmaier_kirfel.dat praxes/physref/waasmaier/waasmaier_kirfel.db

$PYTHON setup.py install
