# encoding: utf-8

"""
This module defines the things that are used in setup.py for building IPython

This includes:

    * The basic arguments to setup
    * Functions for finding things like packages, package data, etc.
    * A function for checking dependencies.
"""

__docformat__ = "restructuredtext en"

#-------------------------------------------------------------------------------
#  Copyright (C) 2009  The XPaXS Development Team
#
#  Distributed under the terms of the GPL License.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from distutils.core import Extension
import os
import sys

from glob import glob

from setupext import (
    print_line, print_raw, print_status, print_message,
    check_for_python, check_for_numpy, check_for_h5py,
    check_for_pyqt4, check_for_matplotlib,
    check_for_pymca, check_for_pyqwt,
    check_for_parallelpython, check_for_pytables
)

#---------------------------------------------------------------------------
# Basic project information
#---------------------------------------------------------------------------

# Release.py contains version, authors, license, url, keywords, etc.
execfile(os.path.join('xpaxs','release.py'))

# Create a dict with the basic information
# This dict is eventually passed to setup after additional keys are added.
setup_args = dict(
      name = name,
      version = version,
      description = description,
      long_description = long_description,
      author = author,
      author_email = author_email,
      url = url,
      download_url = download_url,
      license = license,
      platforms = platforms,
      keywords = keywords,
)

#---------------------------------------------------------------------------
# Find packages
#---------------------------------------------------------------------------

def ui_cvt(arg, dirname, fnames):
    if os.path.split(dirname)[-1] in ('ui', 'resources'):
        for fname in fnames:
            if fname.endswith('.ui'):
                ui = '/'.join([dirname, fname])
                py = os.path.splitext(ui)[0]+'.py'
                if os.path.isfile(py):
                    if os.path.getmtime(ui) < os.path.getmtime(py):
                        continue
                os.system('pyuic4 -o %s %s'%(py, ui))
                print_raw('converted %s'%fname)
            elif fname.endswith('.qrc'):
                rc = '/'.join([dirname, fname])
                py = os.path.splitext(rc)[0]+'.py'
                if os.path.isfile(py):
                    if os.path.getmtime(rc) < os.path.getmtime(py):
                        continue
                os.system('pyrcc4 -o %s %s'%(py, rc))
                print_raw('converted %s'%fname)

def convert_ui():
    os.path.walk('xpaxs', ui_cvt, None)

def add_package(packages, dirname, fnames):
    if '__init__.py' in fnames:
        packages.append(dirname.replace(os.path.sep, '.'))

def find_packages():
    """
    Find all of XPaXS' packages.
    """
    packages = []
    os.path.walk('xpaxs', add_package, packages)
    os.path.walk('SpecClient', add_package, packages)
    return packages

#---------------------------------------------------------------------------
# Find package data
#---------------------------------------------------------------------------

def add_package_data(package_data, dirname, fnames):
    dir = os.path.split(dirname)[-1]
    if dir in ('tests', 'icons', 'cursors', 'macros'):
        package_data.extend(
            os.path.join(dirname.lstrip('xpaxs/'), fname) for fname in fnames
        )


def find_package_data():
    """
    Find XPaXS' package_data.
    """
    # This is not enough for these things to appear in an sdist.
    # We need to muck with the MANIFEST to get this to work
    package_data = []
    os.path.walk('xpaxs', add_package_data, package_data)
    return {'xpaxs': package_data}


#---------------------------------------------------------------------------
# Find data files
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extension modules
#---------------------------------------------------------------------------

if sys.platform == "win32":
    define_macros = [('WIN32',None)]
else:
    define_macros = []

def build_specfile():
    import numpy
    sources = 'specfile/src/*.c'
    headers = 'specfile/include'
    return Extension(
        name = 'specfile',
        sources = glob(sources),
        define_macros = define_macros,
        include_dirs = [headers, numpy.get_include()]
    )

def find_extensions():
    ext_modules = []
#    ext_modules.append(build_specfile())
    return ext_modules

#---------------------------------------------------------------------------
# Find scripts
#---------------------------------------------------------------------------

def find_scripts():
    """
    Find XPaXS' scripts.
    """
    scripts = filter(os.path.isfile, glob('scripts/*'))

    # Script to be run by the windows binary installer after the default setup
    # routine, to add shortcuts and similar windows-only things.  Windows
    # post-install scripts MUST reside in the scripts/ dir, otherwise distutils
    # doesn't find them.
    if 'bdist_wininst' in sys.argv or 'sdist' in sys.argv:
        pass
    else:
        scripts.remove('scripts/xpaxs_win_post_install.py')

    return scripts

#---------------------------------------------------------------------------
# Verify all dependencies
#---------------------------------------------------------------------------

def check_for_dependencies():
    """Check for XPaXS' dependencies.

    This function should NOT be called if running under setuptools!
    """
    print_line()
    print_raw("BUILDING XPAXS")
    print_status('platform', sys.platform)
    if sys.platform == 'win32':
        print_status('Windows version', sys.getwindowsversion())

    print_raw("")
    print_raw("REQUIRED DEPENDENCIES")

    check_for_python()
    check_for_numpy()
    check_for_h5py()
    check_for_parallelpython()
    check_for_pyqt4()
    check_for_matplotlib()
    check_for_pymca()
    check_for_pyqwt()

    print_raw("")
    print_raw("OPTIONAL DEPENDENCIES")

    check_for_pytables()
    print_line()
