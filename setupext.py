# encoding: utf-8

__docformat__ = "restructuredtext en"

#-------------------------------------------------------------------------------
#  Copyright (C) 2008  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

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

class Redirect(object):

    'This wouldnt be necessary if ipython and pp were more friendly to py-2.6'

    def __init__(self, stdout):
        self._stdout = stdout

    def write(self, s):
        pass

    @property
    def original_stdout(self):
        return self._stdout

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
            "WARNING: numpy-%s or greater required" % npReq
        )
        print_message("XPaXS uses numpy to handle numeric arrays")
        return False
    else:
        print_status("numpy", numpy.__version__)
        if LooseVersion(numpy.__version__) < LooseVersion(npReq):
            print_message(
                "WARNING: numpy-%s or greater required, found %s"
                % (npReq, numpy.__version__)
            )
            print_message("XPaXS uses numpy to handle numeric arrays")
            return False
        else:
            return True

def check_for_h5py():
    h5Req = '1.1'
    try:
        sys.stdout = Redirect(sys.stdout)
        from h5py.version import hdf5_version, version
        sys.stdout = sys.stdout.original_stdout
    except ImportError:
        sys.stdout = sys.stdout.original_stdout
        print_status("h5py", "Not found")
        print_message("WARNING: h5py-%s or greater required" % h5Req)
        print_message("XPaXS uses h5py for reading and writing data")
        return False
    else:
        print_status("h5py", "HDF5: %s, h5py: %s" % (hdf5_version, version))
        if LooseVersion(version) < LooseVersion(h5Req):
            print_message(
                "WARNING: h5py-%s or greater required, found %s"
                % (h5Req, version)
            )
            print_message("XPaXS uses h5py for reading and writing data")
            return False
        elif LooseVersion(hdf5_version) < LooseVersion('1.8.1'):
            print_message(
                "WARNING: hdf5-1.8 or greater required for data acquisition"
            )
            print_message(
                "Offline data analysis requires hdf5-1.6.7 or greater"
            )
            return True
        else:
            return True

def check_for_pyqt4():
    try:
        from PyQt4 import pyqtconfig
    except ImportError:
        print_status(
            "PyQt4", "Not found (required for graphical user interfaces)"
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
        print_message("WARNING: matplotlib-%s or greater required" % mplReq)
        print_message('XPaXS uses matplotlib to plot data')
        return False
    else:
        print_status("matplotlib", mpl.__version__)
        if LooseVersion(mpl.__version__) < LooseVersion(mplReq):
            print_message(
                "WARNING: matplotlib-%s or greater required, found %s"
                % (mplReq, mpl.__version__)
            )
            print_message('XPaXS uses matplotlib to plot data')
            return False
        else:
            return True

def check_for_pymca():
    pymcaReq = '4.3.1'
    try:
        from PyMca import PyMca
    except ImportError:
        print_status(
            "PyMca", "Not found (required for X-ray fluorescence capabilities)"
        )
        return False
    else:
        print_status("PyMca", PyMca.__version__)
        if LooseVersion(PyMca.__version__) < LooseVersion(pymcaReq):
            print_message(
                "pymca-%s or greater required for X-ray fluorescence analysis"
                % pymcaReq
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
        sys.stdout = Redirect(sys.stdout)
        import pp
        sys.stdout = sys.stdout.original_stdout
    except ImportError:
        sys.stdout = sys.stdout.original_stdout
        print_status("parallelpython", "Not found")
        print_message(
            "WARNING: parallelpython-%s or greater required" % ppReq
        )
        print_message("XPaXS uses parallelpython to process data")
        return False
    else:
        print_status("parallelpython", pp.version)
        if LooseVersion(pp.version) < LooseVersion(ppReq):
            print_message(
                "WARNING: parallelpython-%s or greater required" % ppReq
            )
            print_message("XPaXS uses parallelpython to process data")
            return False
        else:
            return True

def check_for_pexpect():
    pxReq = '2.3'
    try:
        import pexpect
    except ImportError:
        print_status("pexpect", "Not found")
        return False
    else:
        print_status("pexpect", pexpect.__version__)
        if LooseVersion(pexpect.__version__) < LooseVersion(pxReq):
            print_message(
                "pexpect-%s or greater, found %s"
                % (pxReq, pexpect.__version__)
            )
            return False
        else:
            return True

def check_for_pytables():
    ptReq = '2.1'
    try:
        import tables
    except ImportError:
        print_status("pytables", "Not found")
        return False
    else:
        print_status("pytables", tables.__version__)
        if LooseVersion(tables.__version__) < LooseVersion(ptReq):
            print_message(
                "pytables-%s or greater, found %s"
                % (ptReq, tables.__version__)
            )
            return False
        else:
            return True
