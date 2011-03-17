========
Releases
========

Before creating a release, the version number needs to be updated in
:file:`praxes/__init__.py`. Ensure that the Praxes source directory appears
on the $PYTHONPATH, so the package version numbers will be advertised correctly
for the installers and the documentation.


Creating Source Releases
========================

Praxes is distributed as a source release for Linux and OS-X. To create a
source release, just do::

  git tag v{X}
  git push --tags

This automatically creates links to download the source release at the
`Praxes downloads page`_.


Creating Windows Installers
===========================

Open a DOS window, cd into the praxes source directory and run::

  python setup.py bdist_wininst --install-script=praxes_win_post_install.py

This creates the windows installer in the `dist/` directory, which can then be
uploaded to the `Praxes downloads page`_.


Publishing Praxes' documentation
================================

When publishing a new release, the Praxes doumentation needs to be generated
and published as well. Sphinx_ is required to build the documentation. First,
run::

   git clean -fdx

Then, in the :file:`doc/` directory, run::

   make html

Next, move to the master branch of the praxes.github.com repository, and run::

   cp -r ../praxes/doc/_build/html/* .
   git status

Use ``git add`` to add any new files to the repository, and then commit and
push the changes to the upstream praxes repository::

   git commit -a -m "meaningful commit message"
   git push

and visit the `Praxes documentation page`_ to view the documentation.

.. _`Praxes downloads page`: https://github.com/praxes/praxes/downloads
.. _Sphinx: http://sphinx.pocoo.org/
.. _`Praxes documentation page`: http://praxes.github.com
