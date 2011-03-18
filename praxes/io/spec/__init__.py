"""
"""

def open(file_name):
    """Open a spec data file for read-only access.

    Returns an OrderedDict-like interface to the scans contained in the file.
    """
    from .file import create_file
    return create_file(file_name)
