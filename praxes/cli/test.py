from __future__ import print_function, division, absolute_import


descr = 'runs the praxes test suite'
example = """
examples:
    praxes test --verbose
"""


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('test', description = descr, help = descr)
    p.add_argument(
        '-v', '--verbose', action='store_true',
        help="report detailed results in terminal"
        )
    p.set_defaults(func=execute)


def execute(args, parser):
    import os
    import unittest

    suite = unittest.TestLoader().discover(
        '.' if os.path.isfile('praxes/__init__.py') else 'praxes'
        )
    unittest.TextTestRunner(verbosity = args.verbose + 1).run(suite)
