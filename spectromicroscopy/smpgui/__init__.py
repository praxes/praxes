"""
"""

UI_DEVEL = True

def gen_ui():
    import glob
    import os

    import spectromicroscopy as smp
    dir = os.path.split(smp.__file__)[0]

    for ui in glob.glob(dir+'/smpgui/*.ui'):
        py = os.path.splitext(ui)[0]+'.py'
        if os.path.isfile(py):
            convert = os.path.getatime(ui) > os.path.getatime(py)
        else:
            convert = True
        if convert:
            os.system('pyuic4 %s > %s'%(ui, py))

if UI_DEVEL: gen_ui()
del(UI_DEVEL, gen_ui)

from smpmainwindow import SmpMainWindow
