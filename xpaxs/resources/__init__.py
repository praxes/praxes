"""
"""

from xpaxs import UI_DEVEL

def gen_resources():
    import glob
    import os

    dir = os.path.split(__file__)[0]

    for rc in glob.glob(dir+'/*.qrc'):
        py = os.path.splitext(rc)[0]+'.py'
        if os.path.isfile(py):
            convert = os.path.getmtime(rc) > os.path.getmtime(py)
        else:
            convert = True
        if convert:
            os.system('/usr/bin/pyrcc4 -o %s %s'%(py, rc))

if UI_DEVEL: gen_resources()
del(UI_DEVEL, gen_resources)
