import os
from distutils.core import setup


packages = []
for dirpath, dirnames, filenames in os.walk('praxis'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])        


setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    description = 'Praxis framework for scientific analysis',
    name = 'praxis',
    packages = packages,
)
