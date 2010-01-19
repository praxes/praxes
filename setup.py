import ConfigParser
import os

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


cfg = ConfigParser.ConfigParser()
cfg.read('setup.cfg')

with open('phynx/version.py') as f:
    for line in f:
        if line[:11] == '__version__':
            exec(line)
            break
if __version__ != cfg.get('metadata', 'version'):
    # need to update the project version metadata:
    with open('setup.cfg') as f:
        lines = f.readlines()
    with open('setup.cfg', 'w') as f:
        for line in lines:
            if line.startswith('version'):
                line = 'version = %s\n' % __version__
            f.write(line)

setup(
    author = cfg.get('metadata', 'author'),
    author_email = cfg.get('metadata', 'author_email'),
    classifiers = cfg.get('metadata', 'classifiers').split('\n'),
    description = cfg.get('metadata', 'description'),
    entry_points = {
        'console_scripts' : [
            #'foo = my_package.some_module:main_func'
        ],
        'gui_scripts' : [
            #'bar = my_package_gui.start_func',
        ],
    },
    extras_require = dict(
        [(k,v.split('\n')) for (k,v) in cfg.items('metadata.extras_require')]
    ),
    install_requires = cfg.get('metadata', 'install_requires').split('\n'),
    license = cfg.get('metadata', 'license'),
    long_description = cfg.get('metadata', 'long_description'),
    name = cfg.get('metadata', 'name'),
    package_data = {
        'phynx' : [
            'tests/citrus_leaves.dat.h5',
        ]
    },
    packages = find_packages(),
    platforms = cfg.get('metadata', 'platforms'),
    requires = cfg.get('metadata', 'requires').split('\n'),
    url = cfg.get('metadata', 'url'),
    version = cfg.get('metadata', 'version'),
    zip_safe = cfg.getboolean('metadata', 'zip_safe'),
)
