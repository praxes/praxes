********
Releases
********

Before creating a release, the version number needs to be updated in
:file:`xpaxs/release.py`. The next step is to create a source distribution,
which will serve as the foundation for the eggs and other
installers::

  python setup.py develop --user


Distributing Source Releases
============================

XPaXS is distributed as a source release for Linux and OS-X. To create a source
release, just do::

  python setup.py sdist --formats=zip,gztar

This will create the tgz and zip source files that can be uploaded to the
`xpaxs project page`_ by selecting the "Downloads" button.


Creating Windows Installers
===========================

Once the source distributions have been created, which converts the pyqt UI and
resource files, run the following in the xpaxs source directory::

  python setup.py bdist_wininst --install-script=xpaxs_win_post_install.py

This creates the executable windows installer in the :file:`dist/` directory. 

Building XPaXS documentation
============================

When publishing a new release, the XPaXS doumentation needs to be generated and
published as well. Sphinx_ is required to build the documentation::

  cd doc
  make html
  sphinxtogithub _build/html

which will produce the html output and save it in :file:`_build/html`.

To upload the documentation to the xpaxs project page::

  cd .. 
  cp -rf doc/_build/html ../
  git clean -fxd
  git checkout gh-pages
  cp -rf doc/_build/html/* .
  git commit -a -m "update documentation for version x"
  git push
  
It may take a few minutes for the documentation_ to update.
    
.. _`xpaxs project page`: github.com/darrendale/xpaxs-legacy
.. _documentation: darrendale.github.com/xpaxs-legacy
.. _Sphinx: http://sphinx.pocoo.org/
