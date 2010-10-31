"""Windows-specific part of the installation"""

import os, sys, shutil

def mkshortcut(target, description, link_file, *args, **kw):
    """make a shortcut if it doesn't exist, and register its creation"""

    create_shortcut(target, description, link_file, *args, **kw)
    file_created(link_file)

def install():
    """Routine to be run by the win32 installer with the -install switch."""

    # Get some system constants
    prefix = sys.prefix
    python = os.path.join(prefix, 'python.exe')
    # Lookup path to common startmenu ...
    start_dir = os.path.join(
        get_special_folder_path('CSIDL_COMMON_PROGRAMS'),
        'XPaXS'
    )
    scripts_dir = os.path.join(prefix, 'Scripts')

    # Create entry ...
    if not os.path.isdir(start_dir):
        os.mkdir(start_dir)
        directory_created(start_dir)

    # Create program shortcuts ...
    script = os.path.join(scripts_dir, 'xpaxs-script.pyw')
    f = os.path.join(start_dir, 'xpaxs.lnk')
    mkshortcut(python, 'xpaxs', f, '"%s"'%script)

    # Create documentation shortcuts ...
#    t = prefix + r'\share\doc\ipython-%s\manual.pdf' % version
#    f = ip_dir + r'\Manual in PDF.lnk'
#    mkshortcut(t,r'IPython Manual - PDF-Format',f)
#
#    t = prefix + r'\share\doc\ipython-%s\manual\manual.html' % version
#    f = ip_dir + r'\Manual in HTML.lnk'
#    mkshortcut(t,'IPython Manual - HTML-Format',f)

def remove():
    """Routine to be run by the win32 installer with the -remove switch."""
    pass

# main()
if len(sys.argv) > 1:
    if sys.argv[1] == '-install':
        install()
    elif sys.argv[1] == '-remove':
        remove()
    else:
        print "Script was called with option %s" % sys.argv[1]
