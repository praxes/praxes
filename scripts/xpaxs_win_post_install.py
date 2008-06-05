"""Windows-specific part of the installation"""

import os, sys, shutil

def mkshortcut(target,description,link_file,*args,**kw):
    """make a shortcut if it doesn't exist, and register its creation"""

    create_shortcut(target, description, link_file,*args,**kw)
    file_created(link_file)

def install():
    """Routine to be run by the win32 installer with the -install switch."""

    # Get some system constants
    prefix = sys.prefix
    python = prefix + r'/pythonw.exe'
    # Lookup path to common startmenu ...
    ip_dir = get_special_folder_path('CSIDL_COMMON_PROGRAMS') + r'\XPaXS'
    lib_dir = prefix + r'\Lib\site-packages\xpaxs'
    ip_filename="sxfm"

    # Create entry ...
    if not os.path.isdir(ip_dir):
        os.mkdir(ip_dir)
        directory_created(ip_dir)

    # Create program shortcuts ...
    name = 'sxfm'

    script = '"'+lib_dir+r'\%s.pyw"'%name
    f = ip_dir + r'\%s.lnk'%name
    shutil.copy(sys.prefix+r'\Scripts\%s'%name,lib_dir+'\%s.pyw'%ip_filename)
    mkshortcut(python,name,f,script)

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
