# -*- coding: utf-8 -*-
"""Release data for the XPaXS project."""

#*****************************************************************************
#       Copyright (C) 2007-2009 Darren Dale <darren.dale@cornell.edu>
#
#  Distributed under the terms of the GPL License.
#*****************************************************************************

# This file is derived from work done on the IPython project,

# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = 'xpaxs'

# For versions with substrings (like 0.6.16.svn), use an extra . to separate
# the new substring.  We have to avoid using either dashes or underscores,
# because bdist_rpm does not accept dashes (an RPM) convention, and
# bdist_deb does not accept underscores (a Debian convention).

development = False    # change this to False to do a release
version_base = '0.8a4'
branch = 'xpaxs'
revision = '550'

if development:
    if branch == 'xpaxs':
        version = '%s.bzr.r%s' % (version_base, revision)
    else:
        version = '%s.bzr.r%s.%s' % (version_base, revision, branch)
else:
    version = version_base


description = 'Extensible Packages for X-ray Science'

long_description = \
"""
XPaXS provides a python interface for data acquisition and analysis in the
field of X-ray science.
"""

license = 'GPL'

authors = {
    'Darren': ('Darren Dale', 'darren.dale@cornell.edu'),
    'Jeffrey': ('Jeffrey Lipton', 'jil26@cornell.edu'),
}

author = 'The XPaXS Development Team'

author_email = 'darren.dale@cornell.edu'

url = 'http://www.chess.cornell.edu/software/xpaxs'

download_url = 'http://pypi.python.org/pypi/xpaxs'

platforms = ['Linux', 'Mac OSX', 'Windows Vista/XP/2000']

keywords = []

requires = [
    'numpy (>=1.2)',
    'matplotlib (>=0.98.3)',
    'PyMca (>=4.3.1)',
    'pp (>=1.5.6)',
#    'pexpect>=2.3',
    'h5py (>=1.1)',
#    'TraitsBackendQt>=3.0',
#    'EnvisagePlugins>=3.0',
]
