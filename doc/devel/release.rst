********
Releases
********

Before creating a release, the version number needs to be updated in
`xpaxs/__init__.py`. Then XPaXS needs to be installed either with::

  python setup.py install

or::

  python setup.py develop

in order proceed with building the release, so the package version numbers will
be advertised correctly for the installers and the documentation.


Creating Source Releases
========================

XPaXS is distributed as a source release for Linux and OS-X. To create a source
release, just do::

  python setup.py register sdist --formats=zip,gztar upload --sign

This will create the tgz source file and upload it to the Python Package Index.
Uploading to PyPi requires a .pypirc file in your home directory, something
like::

  [server-login]
  username: <username>
  password: <password>

You can create a source distribution without uploading by doing::

  python setup.py sdist

This creates a source distribution in the `dist/` directory.


Creating Windows Installers
===========================

open a DOS window, cd into the xpaxs source directory and run::

  python setup.py bdist_wininst --install-script=xpaxs_win_post_install.py

.. We distribute binary installers for the windows platform. In order to build the
   windows installer, you need to install MinGW_ (tested with MinGW-5.1.4). Then
   open a DOS window, cd into the xpaxs source directory and run::

     python setup.py build -c mingw32
     python setup.py bdist_wininst --skip-build --install-script xpaxs_win_post_install.py

   This creates the executable windows installer in the `dist/` directory.

   .. _MinGW: http://www.mingw.org/


Building XPaXS documentation
============================

When publishing a new release, the XPaXS doumentation needs to be generated and
published as well. Sphinx_, LaTeX_ (preferably TeX-Live_), and dvipng_ are
required to build the documentation. Once these are installed, do::

  python setup.py build_sphinx

which will produce the html output and save it in build/sphinx/html. Then run::

  python setup.py build_sphinx -b latex
  cd build/sphinx/latex
  make all-pdf

which will generate a pdf file in the latex directory. Finally, copy the `html/`
directory and the `latex/XPaXS.pdf` file to the webserver.

.. _Sphinx: http://sphinx.pocoo.org/
.. _LaTeX: http://www.latex-project.org/
.. _TeX-Live: http://www.tug.org/texlive/
.. _dvipng: http://savannah.nongnu.org/projects/dvipng/
