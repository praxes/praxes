import fileinput
import glob
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
os.system('sphinx-build -b html -d build/doctrees source build/html')
#htmls = glob.glob('build/html/*.html')
#for html in htmls:
#    base = os.path.splitext(os.path.abspath(html))[0]
#    shutil.move(html, base+'.xhtml')

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
