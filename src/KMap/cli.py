"""Create Karnaugh Map objects which can be solved and manipulated. from the command line
Supported characters:
    Any case is supported
    or equivalents: |, ||, +, v
    and equivalents: &, &&, *, ^
    not equivalents: !, ~, ¬

Functions:

    cli() -> (None)

Misc variables:

    __all__
    __author__
    __version__
    supported_from
"""

__all__ = ["cli"]
__author__ = "Alexander Bisland"
__version__ = "1.2.2"
supported_from = "3.8.1"

from KMap import Mapper
import argparse


def cli() -> None:
    """Solve the map from the arguments

        Parameters:
            (None)

        Returns:
            Nothing (None): Null
    """
    parser = argparse.ArgumentParser(description='(Optionally) Dependency-free library for steganography')
    parser.add_argument('expression', type=str, help='Unsimplified expression to simplify')
    parser.add_argument('--print-map', '-p', dest='print_map', action='store_const',
                        const=True, default=False, help='Whether to print the map or not')
    parser.add_argument('--debug', '-d', dest='debug', action='store_const',
                        const=True, default=False, help='Debug mode (verbose)')
    parser.add_argument('--tot-input', '-i', type=int, default=None, help='Total number of inputs (Optional)')

    args = parser.parse_args()

    kmap = Mapper.KarnaughMap(expression=args.expression, tot_input=args.tot_input, debug=args.debug)
    kmap.create_map()
    if args.print_map:
        kmap.print()
    print(kmap.solve_map())


if __name__ == "__main__":
    cli()
