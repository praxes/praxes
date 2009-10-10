********
Releases
********

Before creating a release, the version number needs to be updated in
`phynx/version.py`. Then Phynx needs to be installed either with::

  python setup.py install

or::

  python setup.py develop

in order proceed with building the release, so the package version
numbers will be advertised correctly for the installers and the
documentation.


Creating Source Releases
========================

Phynx is distributed as a source release for Linux and OS-X. To create
a source release, just do::

  python setup.py register
  python setup.py sdist --formats=zip,gztar upload --sign

This will create the tgz source file and upload it to the Python
Package Index. Uploading to PyPI requires a .pypirc file in your home
directory, something like::

  [server-login]
  username: <username>
  password: <password>

You can create a source distribution without uploading by doing::

  python setup.py sdist

This creates a source distribution in the `dist/` directory.


Creating Windows Installers
===========================

Open a DOS window, cd into the phynx source directory and run::

  python setup.py bdist_wininst


Building Phynx documentation
============================

When publishing a new release, the Phynx doumentation needs to be
generated and published as well::

  python setup.py build_sphinx

which will produce the html output and save it in build/sphinx/html.
Then run::

  python setup.py build_sphinx -b latex
  cd build/sphinx/latex
  make all-pdf

which will generate a pdf file in the latex directory. Finally, copy
the `html/` directory and the `latex/XPaXS.pdf` file to the webserver.
To upload the documentation to the Phynx website::

  cd build/sphinx/html
  zip -r phynx *

Then visit the `Phynx page at the Python Package Index`_ to upload the
documentation.

.. _`Phynx page at the Python Package Index`: http://pypi.python.org/pypi?%3Aaction=pkg_edit&name=phynx
