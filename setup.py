import ConfigParser
import os
import sys

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist as _sdist

cfg = ConfigParser.ConfigParser()
cfg.read('setup.cfg')

with open('xpaxs/version.py') as f:
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

class install(_install):

    def run(self):
        _install.run(self)
        if sys.platform.startswith('win'):
            self.post_install_windows()

    def post_install_windows(self):
        # Lookup path to common startmenu ...
        start_dir = os.path.join(
            get_special_folder_path('CSIDL_COMMON_PROGRAMS'),
            'XPaXS'
        )
        if not os.path.isdir(start_dir):
            os.mkdir(start_dir)
            directory_created(start_dir)

        python = os.path.join(sys.prefix, 'python.exe')
        scripts_dir = os.path.join(sys.prefix, 'Scripts')
        for item in ['xpaxs.pyw']:
            base = item.rstrip('.pyw').strip('.py')
            link = os.path.join(start_dir, base + '.lnk')
            script = '"%s"' % os.path.join(scripts_dir, item)
            
            create_shortcut(python, base, link, script)
            file_created(link)


class sdist(_sdist):

    def ui_cvt(self, arg, dirname, fnames):
        if os.path.split(dirname)[-1] in ('ui'):
            for fname in fnames:
                if fname.endswith('.ui'):
                    ui = '/'.join([dirname, fname])
                    py = os.path.splitext(ui)[0]+'.py'
                    if os.path.isfile(py):
                        if os.path.getmtime(ui) < os.path.getmtime(py):
                            continue
                    os.system('pyuic4 -o %s %s'%(py, ui))
                    print('converted %s'%fname)
                elif fname.endswith('.qrc'):
                    rc = '/'.join([dirname, fname])
                    py = os.path.splitext(rc)[0]+'_rc.py'
                    if os.path.isfile(py):
                        if os.path.getmtime(rc) < os.path.getmtime(py):
                            continue
                    os.system('pyrcc4 -o %s %s'%(py, rc))
                    print('converted %s'%fname)

    def run(self):
        os.path.walk('xpaxs', self.ui_cvt, None)
        _sdist.run(self)

setup(
    author = cfg.get('metadata', 'author'),
    author_email = cfg.get('metadata', 'author_email'),
    classifiers = cfg.get('metadata', 'classifiers').split('\n'),
    cmdclass = {
        'install' : install,
        'sdist' : sdist,
    },
    description = cfg.get('metadata', 'description'),
    entry_points = {
        'console_scripts' : [
            #'foo = my_package.some_module:main_func'
        ],
        'gui_scripts' : [
            'xpaxs = xpaxs.frontend.mainwindow:main',
        ],
    },
#    extras_require = dict(
#        [(k,v.split('\n')) for (k,v) in cfg.items('metadata.extras_require')]
#    ),
    include_package_data = True,
#    install_requires = cfg.get('metadata', 'install_requires').split('\n'),
    license = cfg.get('metadata', 'license'),
    long_description = cfg.get('metadata', 'long_description'),
    name = cfg.get('metadata', 'name'),
    #package_data = {
    #    '' : [
    #        '*.svg',
    #    ]
    #},
    packages = find_packages(),
    platforms = cfg.get('metadata', 'platforms'),
#    requires = cfg.get('metadata', 'requires').split('\n'),
#    scripts = ['scripts/postinstall_win.py'] if 'bdist_msi' in sys.argv else [],
    test_suite = 'nose.collector',
    url = cfg.get('metadata', 'url'),
    version = cfg.get('metadata', 'version'),
    zip_safe = cfg.getboolean('metadata', 'zip_safe'),
)
