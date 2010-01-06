********
Releases
********

Before creating a release, the version number needs to be updated in
`xpaxs/release.py`. The next step is to create a source distribution,
which will serve as the foundation for the eggs and other
installers::

  python setup.py sdist

This sdist needs to be unpacked and checked to make sure that no
files are missing from the source distribution (using `diff -uR`) and
that the tests pass.

Distributing Source Releases
============================

XPaXS is distributed as a source release for Linux and OS-X. To create a source
release, just do::

  python setup.py register
  python setup.py sdist --formats=zip,gztar upload --sign

This will create the tgz source file and upload it to the Python
Package Index. Uploading to PyPi requires a .pypirc file in your home
directory, something like::

  [server-login]
  username: <username>
  password: <password>


Creating Windows Installers
===========================

open a DOS window, cd into the xpaxs source directory and run::

  python setup.py bdist_msi --install-script=win_install.py

.. We distribute binary installers for the windows platform. Run the
following in the xpaxs source directory::

     python setup.py bdist_msi --skip-build \
         --install-script postinstall_win.py upload --sign

This creates the executable windows installer in the `dist/`
directory. 

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
