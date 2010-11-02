********
Releases
********

Before creating a release, the version number needs to be updated in
:file:`phynx/version.py`. Then Phynx needs to be installed either with::

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

  python setup.py sdist --formats=zip,gztar

This will create the tgz and zip files that can be uploaded at the
`phynx project page`_ by selecting the "Downloads" button. 


Creating Windows Installers
===========================

Open a DOS window, cd into the phynx source directory and run::

  python setup.py bdist_msi


Building Phynx documentation
============================

When publishing a new release, the Phynx doumentation needs to be
generated and published as well::

  cd doc
  make html
  sphinxtogithub _build/html

which will produce the html output and save it in :file:`_build/html`.

To upload the documentation to the phynx project page::

  cd ..
  cp -rf doc/_build/html ../
  git clean -fxd
  git checkout gh-pages
  cp -rf doc/_build/html/* .
  git commit -a -m "update documentation for version x"
  git push

It may take a few minutes for the documentation_ to update.

.. _`phynx project page`: github.com/darrendale/phynx
.. _documentation: darrendale.github.com/phynx
