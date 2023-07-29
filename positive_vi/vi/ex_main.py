from argparse import ArgumentParser
from .vi_main import View

PROGRAM = 'ex'

class Edit(View):
    """
    `ex` originally meant "extended" but we are not trying to
    re-write history, just name a class, so we call it `Edit`.
    """
    
    def __init__(self,
                 file,
                 recover=False,
                 readonly=False,
                 command=[],
                 # tags are unimplemented
                 tag=None,
                 # vi scroll edit option*2
                 # vi window edit option
                 window=0,
                 suppress=False,
                 visual=False):
        """
        """
        View.__init__(self, file,
                      recover=recover,
                      readonly=readonly,
                      command=command,
                      tag=tag,
                      window=window,
                      suppress=suppress,
                      visual=visual)

def add_arguments(parser):
    parser.add_argument('-r',
                        action='store_true',
                        default=False,
                        dest='recover',
                        help="Recover the named files. Recovery information for a file shall be saved after the use of a preserve command.")
    parser.add_argument('-R',
                        action='store_true',
                        default=False,
                        dest='readonly',
                        help="Set readonly edit option.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('-s',
                       action='store_true',
                       default=False,
                       dest='suppress',
                       help="Suppress prompts, autoindentation, ignoring the value of the autoindent edit option, and the EXINIT environment variable.")
    modes.add_argument('-v',
                       action='store_true',
                       default=False,
                       dest='visual',
                       help="Enter visual mode")
    parser.add_argument('-c',
                        action='append',
                        default=[],
                        dest='command',
                        help="Initial command to be executed in the first edit buffer loaded from an existing file.")
    parser.add_argument('-t',
                        action='store',
                        default=None,
                        dest='tag',
                        help="Edit the file containing the specified tagstring; see ctags. The tags feature represented by -t tagstring and the tag command is optional.")
    parser.add_argument('-w',
                        action='store',
                        default=None,
                        dest='size',
                        help="Set the window edit option to size.")
    parser.add_argument('file',
                        action='store',
                        nargs='*')
    return parser


def ex_main():
    parser = add_arguments(ArgumentParser(PROGRAM))
    arguments = parser.parse_args()
    options = vars(arguments)
    # print(repr(options))
    Edit(**options)

    
if __name__ == '__main__':
    ex_main()
