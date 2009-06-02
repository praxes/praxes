# encoding: utf-8

from distutils.version import LooseVersion
import sys
import os
from textwrap import fill

#-------------------------------------------------------------------------------
# Normal code begins
#-------------------------------------------------------------------------------

def print_line(char='='):
    print char * 76

def print_status(package, status):
    initial_indent = "%22s: " % package
    indent = ' ' * 24
    print fill(str(status), width=76,
               initial_indent=initial_indent,
               subsequent_indent=indent)

def print_message(message):
    indent = ' ' * 24 + "* "
    print fill(str(message), width=76,
               initial_indent=indent,
               subsequent_indent=indent)

def print_raw(section):
    print section

def convert_qt_version(version):
    version = '%x'%version
    temp = []
    while len(version) > 0:
        version, chunk = version[:-2], version[-2:]
        temp.insert(0, str(int(chunk, 16)))
    return '.'.join(temp)

#-------------------------------------------------------------------------------
# Tests for specific packages
#-------------------------------------------------------------------------------

def check_for_python():
    pyVer = sys.version.split()[0]
    pyReq = '2.5'
    print_status("Python", pyVer)
    if LooseVersion(pyVer) < LooseVersion(pyReq):
        raise RuntimeWarning(
            'WARNING: Python-%s or later required, found "%s"'%(pyReq, pyVer)
        )

def check_for_numpy():
    npReq = '1.2'
    try:
        import numpy
    except ImportError:
        print_status("numpy", "Not found")
        print_message(
            "WARNING: numpy-%s or later required for handling arrays of "
            "numerical data" % npReq
        )
        return False
    else:
        print_status("numpy", numpy.__version__)
        if LooseVersion(numpy.__version__) < LooseVersion(npReq):
            print_message(
                "WARNING: numpy-%s or later required for handling arrays of "
                "numerical data" % npReq
            )
            return False
        else:
            return True

def check_for_h5py():
    h5Req = '1.2'
    try:
        from h5py.version import hdf5_version, version
    except ImportError:
        print_status("h5py", "Not found")
        print_message(
            "WARNING: h5py-%s or greater required for reading and writing "
            "data" % h5Req
        )
        return False
    else:
        print_status("h5py", "HDF5: %s, h5py: %s" % (hdf5_version, version))
        if LooseVersion(version) < LooseVersion(h5Req):
            print_message(
                "WARNING: h5py-%s or greater required for reading and writing "
                "data" % h5Req
            )
            return False
        elif LooseVersion(hdf5_version) < LooseVersion('1.8.1'):
            print_message(
                "WARNING: hdf5-1.8 or later required for data acquisition. "
                "hdf5-1.6.7 or later is sufficient for offline data analysis"
            )
            return True
        else:
            return True

def check_for_pyqt4():
    try:
        from PyQt4 import pyqtconfig
    except ImportError:
        print_status(
            "PyQt4", "Not found"
        )
        print_message(
            "WARNING: PyQt4-%s or later required for graphical user interfaces"
            % mplReq
        )
        return False
    else:
        try:
            qt_version = pyqtconfig.Configuration().qt_version
            qt_version = convert_qt_version(qt_version)
        except AttributeError:
            qt_version = "<unknown>"
        print_status(
            "PyQt4", "Qt: %s, PyQt: %s"
            % (qt_version, pyqtconfig.Configuration().pyqt_version_str)
        )
        return True

def check_for_matplotlib():
    mplReq = '0.98.3'
    try:
        import matplotlib as mpl
    except ImportError:
        print_status("matplotlib", "Not found")
        print_message(
            "WARNING: matplotlib-%s or later required to generate plots"
            % mplReq
        )
        return False
    else:
        print_status("matplotlib", mpl.__version__)
        if LooseVersion(mpl.__version__) < LooseVersion(mplReq):
            print_message(
                "WARNING: matplotlib-%s or later required to generate plots"
                % mplReq
            )
            return False
        else:
            return True

def check_for_pymca():
    pymcaReq = '4.3.1 20090202-snapshot'
    try:
        from PyMca import PyMcaMain
    except ImportError:
        print_status(
            "PyMca", "Not found"
        )
        print_message(
            "WARNING: pymca-%s or later required for X-ray fluorescence "
            "analysis" % pymcaReq
        )
        return False
    else:
        print_status("PyMca", PyMcaMain.__version__)
        if LooseVersion(PyMcaMain.__version__) < LooseVersion(pymcaReq):
            print_message(
                "WARNING: pymca-%s or later required for X-ray fluorescence "
                "analysis" % pymcaReq
            )
            return False
        else:
            return True

def check_for_pyqwt():
    pyqwtReq = '5.1.0'
    try:
        from PyQt4 import Qwt5
    except ImportError:
        print_status(
            "PyQwt",
            "Not found (required for some X-ray fluorescence capabilities)"
        )
        return False
    else:
        print_status("PyQwt", Qwt5.QWT_VERSION_STR)
        if LooseVersion(Qwt5.QWT_VERSION_STR) < LooseVersion(pyqwtReq):
            print_message(
                "PyQwt-%s or greater required for some X-ray "
                "fluorescence capabilities" % pymcaReq
            )
            return False
        else:
            return True

def check_for_parallelpython():
    ppReq = '1.5.6'
    try:
        import pp
    except ImportError:
        print_status("parallelpython", "Not found")
        print_message(
            "WARNING: parallelpython-%s or later required to process data"
            % ppReq
        )
        return False
    else:
        print_status("parallelpython", pp.version)
        if LooseVersion(pp.version) < LooseVersion(ppReq):
            print_message(
                "WARNING: parallelpython-%s or later required to process data"
                % ppReq
            )
            return False
        else:
            return True

def check_for_pytables():
    ptReq = '2.0'
    try:
        import tables
    except ImportError:
        print_status("pytables", "Not found")
        return False
    else:
        print_status("pytables", tables.__version__)
        if LooseVersion(tables.__version__) < LooseVersion(ptReq):
            print_message(
                "pytables-%s or later required to convert data from legacy "
                "format, found pytables-%s" % (ptReq, tables.__version__)
            )
            return False
        else:
            return True
