from __future__ import print_function, absolute_import

import sys


help = "Launches the sxfm graphical user interface"


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('sxfm', description = help, help = help)
    p.add_argument(
        '-q', '--quiet', action='store_true',
        help="don't report progress in terminal"
        )
    p.set_defaults(func=execute)


def execute(args, parser):
    import logging

    logger = logging.getLogger('praxes')
    logger.setLevel(logging.DEBUG)

    from praxes.fluorescence import _launch_gui

    _launch_gui(args)
