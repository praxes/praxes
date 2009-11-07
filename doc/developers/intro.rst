************
Introduction
************

Getting Started
===============

In order to work on xpaxs development, after installing the xpaxs dependencies,
you will need to do the following:

python setup.py develop

This uses setuptools to install a link in your site-packages directory which
points to your source directory. This allows you to make changes in the source
directory without having to reinstall xpaxs. Note, however, that after changing
extension code, which needs to be compiled, you will need to run
"python setup.py develop" again. Also note that executable scripts are copied
to their install directory, rather than being linked, so you need to run
"python setup.py develop" after editing scripts.

Organization
============


