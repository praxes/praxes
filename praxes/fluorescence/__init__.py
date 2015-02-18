"""
"""

import logging
import sys


class Args(object):

    def __getattr__(self, key):
        return False


def _launch_gui(args=None):
    from PyQt4 import QtGui

    from praxes.frontend import mainwindow
    from praxes.frontend.application import PraxesApplication

    # configure logging
    if args is None:
        print '"sxfm" is deprecated, use "praxes sxfm"'
        args = Args()
    if args.debug:
        log_level = logging.DEBUG
        add_handler(log_level)
    else:
        log_level = logging.CRITICAL if args.quiet else logging.INFO

    app = PraxesApplication(sys.argv)
    app.setOrganizationName('Praxes')
    app.setApplicationName('sxfm')
    sxfm_gui = mainwindow.MainWindow(log_level)
    sxfm_gui.show()

    app.exec_()
