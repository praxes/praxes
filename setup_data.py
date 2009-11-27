import os

MATPLOTLIB = 'matplotlib >=0.98.3'
PARALLELPYTHON = 'pp >=1.5.6'
PHYNX = 'phynx >=0.10.0'
PYMCA = 'PyMca >=4.4.0'

execfile(os.path.join('xpaxs', 'version.py'))

INFO = {
    'extras_require':  {
        'parallel': [
            PARALLELPYTHON,
        ],
        'fluorescence': [
            PYMCA,
        ],
    },
    'install_requires': [
        MATPLOTLIB,
        PHYNX,
    ],
    'name': 'XPaXS',
    'requires': [
        'python (>=2.6, <3.0)',
        'distribute (>=0.6.8)',
        'PyQt4 (>=4.5.2)',
    ],
    'version': __version__,
}
