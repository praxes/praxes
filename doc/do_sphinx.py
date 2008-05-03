import fileinput
import os
import shutil
import sys

build_dirs = ['build', 'build/doctrees', 'build/html', 'build/latex', 'source/_static', 
              'source/_templates']
for d in build_dirs:
    try:
        os.mkdir(d)
    except OSError:
        pass

# html manual.
os.system('sphinx-build -d build/doctrees source build/html')

if sys.platform != 'win32':
    # LaTeX format.
    os.system('sphinx-build -b latex -d build/doctrees source build/latex')

    # Produce pdf.
    os.chdir('build/latex')

    # Copying the makefile produced by sphinx...
    os.system('pdflatex XPaXS.tex')
    os.system('pdflatex XPaXS.tex')
    os.system('makeindex -s python.ist XPaXS.idx')
    os.system('makeindex -s python.ist modXPaXS.idx')
    os.system('pdflatex XPaXS.tex')

    os.chdir('../..')
