from __future__ import print_function, absolute_import

import argparse
import logging
import sys
import multiprocessing

# These can't be relative imports on Windows because of the hack
# in main() for multiprocessing.freeze_support()
from praxes.cli import documentation
from praxes.cli import help
from praxes.cli import sxfm
from praxes.cli import test


def main():
    if sys.platform.startswith('win'):
        # Hack for multiprocessing.freeze_support() to work from a
        # setuptools-generated entry point.
        if __name__ != "__main__":
            sys.modules["__main__"] = sys.modules[__name__]
        multiprocessing.freeze_support()

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    import logging
    import praxes

    p = argparse.ArgumentParser(
        description='High energy diffraction data analysis'
    )
    p.add_argument(
        '-V', '--version',
        action = 'version',
        version = 'praxes %s' % praxes.__version__,
    )
    p.add_argument(
        "--debug",
        action = "store_true",
        help = 'verbose reporting',
    )
    sub_parsers = p.add_subparsers(
        metavar = 'command',
        dest = 'cmd',
    )

    help.configure_parser(sub_parsers)
    documentation.configure_parser(sub_parsers)
    sxfm.configure_parser(sub_parsers)
    test.configure_parser(sub_parsers)

    try:
        import argcomplete
        argcomplete.autocomplete(p)
    except ImportError:
        pass

    args = p.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = logging.getLogger('praxes')
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    args.func(args, p)
