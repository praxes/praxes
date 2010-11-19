"""
"""

def open(file_name, lock=None):
    """Open a spec data file for read-only access.

    Returns an OrderedDict-like interface to the scans contained in the file.

    lock can be True to protect access with a recursive lock from python's threading
    library. An instance of an alternative recursive lock implementation can be
    provided, but it must have acquire() and release() methods, and must support
    python's context management protocol.
    """
    from .file import SpecFile
    return SpecFile(file_name, lock=lock)
