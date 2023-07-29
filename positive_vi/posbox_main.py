"""
"""
import sys
from argparse import ArgumentParser
from positive_vi.more.more_main import more_main
from positive_vi.vi.ex_main import ex_main
from positive_vi.vi.vi_main import vi_main

DEBUG = False


def add_arguments(parser):
    subparsers = parser.add_subparsers(
        title='subcommands')
    subparsers.add_parser(
        'more', help="More pager")
    subparsers.add_parser(
        'ex', help="Ex editor")
    subparsers.add_parser(
        'vi', help="Vi editor")
    return parser


def posbox_main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args())
    if DEBUG:
        print(repr(options))
    match sys.argv[1]:
        case "more":
            more_main()
        case "ex":
            ex_main()
        case "vi":
            vi_main()

            
if __name__ == '__main__':
    posbox_main()
