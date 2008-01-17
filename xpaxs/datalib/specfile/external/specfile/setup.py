#!/usr/bin/env python

"""Setup script for the SPECFILE module distribution."""

import os, sys, glob
try:
    import numpy
except ImportError:
    text  = "You must have numpy installed.\n"
    text += "See http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=175103\n"
    raise ImportError, text

from distutils.core import setup
from distutils.extension import Extension

srcfiles = [ 'sfheader','sfinit','sflists','sfdata','sfindex',
             'sflabel' ,'sfmca', 'sftools','specfile_py']

sources = [] 
for file in srcfiles:
  sources.append('src/'+file+'.c')

if sys.platform == "win32":
                                                                                                   
    setup (
            name         = "specfile",
            version      = "3.1",
            description  = "module to read SPEC datafiles",
            author       = "BLISS Group",
            author_email = "rey@esrf.fr",
            url          = "http://www.esrf.fr/computing/bliss/",

            # Description of the modules and packages in the distribution

            #extra_path   = 'Pybliss',
            ext_modules  = [
                           Extension(
                                name          = 'specfile',
                                sources       = sources,
                                define_macros = [('WIN32',None)],
                                include_dirs  = ['include', numpy.get_include()],
                           ),
           ],
    )
else:                                                                                              
    setup (
            name         = "specfile",
            version      = "3.1",
            description  = "module to read SPEC datafiles",
            author       = "BLISS Group",
            author_email = "rey@esrf.fr",
            url          = "http://www.esrf.fr/computing/bliss/",

            # Description of the modules and packages in the distribution

            #extra_path   = 'Pybliss',
            ext_modules  = [
                           Extension(
                                name          = 'specfile',
                                sources       = sources,
                                include_dirs  = ['include', numpy.get_include()],
                           ),
           ],
    )
    
print """Python module ready.
 If you want to generate C libraries:
 Find a Makefile ready on the directory \"src\"
 Minor changes may be needed ( customized for Linux,HP-UX and Solaris)
"""
