#!/usr/bin/python
"""This hook prevents AutoPkg overrides from being added to the repo."""

import argparse
import plistlib
from xml.parsers.expat import ExpatError


def build_argument_parser():
    """Build and return the argument parser."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    return parser


def main(argv=None):
    """Main process."""

    # Overrides should not contain top-level Process arrays.
    required_keys = ("Process",)

    # Parse command line arguments.
    argparser = build_argument_parser()
    args = argparser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            recipe = plistlib.readPlist(filename)
            for req_key in required_keys:
                if req_key not in recipe:
                    print("{}: possible AutoPkg recipe override".format(filename))
                    retval = 1
                    break  # No need to continue checking this file.

        except (ExpatError, ValueError) as err:
            print("{}: plist parsing error: {}".format(filename, err))
            retval = 1

    return retval


if __name__ == "__main__":
    exit(main())
