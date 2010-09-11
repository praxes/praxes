========
Releases
========

Before creating a release, the version number needs to be updated in
:file:`praxis/__init__.py`. Then Praxis then needs to be installed in order
proceed with building the release, so the package version numbers will be
advertised correctly for the installers and the documentation.


Creating Source Releases
========================

Praxis is distributed as a source release for Linux and OS-X. To create a
source release, just do::

  python setup.py register
  python setup.py sdist --formats=zip,gztar upload --sign

This will create the tgz source file and upload it to the Python Package Index.
Uploading to PyPi requires a .pypirc file in your home directory, something
like::

  [server-login]
  username: <username>
  password: <password>

You can create a source distribution without uploading by doing::

  python setup.py sdist

This creates a source distribution in the :file:`dist/` directory.


Creating Windows Installers
===========================

open a DOS window, cd into the praxis source directory and run::

  python setup.py bdist_wininst --install-script=praxis_win_post_install.py

   This creates the executable windows installer in the `dist/` directory.


Publishing Praxis' documentation
================================

When publishing a new release, the Praxis doumentation needs to be generated
and published as well. Sphinx_ is required to build the documentation. In the
`doc/` directory, run::

  make html

which will save the documentation in `doc/_build/html`. Changing into that new
directory, run::

  zip -r praxis *

and visit the `Praxis project page`_ to upload the documentation 

.. _Sphinx: http://sphinx.pocoo.org/
.. _`Praxis project page`: http://pypi.python.org/pypi?:action=pkg_edit&name=praxis
