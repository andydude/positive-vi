"""
more is POSIX-UP (User Portability Utilities)
ex is POSIX-UP
vi is POSIX-UP

"""
try:
    from .Buffer import (
        Addr, Buffer as _Buffer,
        commands, modes, motions, options)
    from .CommandLexer import CommandLexer
    from .CommandParser import CommandParser
    from .CommandVisitor import CommandVisitor
except ImportError:
    import sys
    import os
    parent = os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)))
    sys.path.append(parent)
    from positive_vi.vi.Buffer import (
        Addr, Buffer as _Buffer,
        commands, modes, motions, options)
    from positive_vi.vi.EditOption import EditOpt
    from positive_vi.vi.EditOptionMap import EditOptionMap
    from positive_vi.vi.CommandLexer import CommandLexer
    from positive_vi.vi.CommandParser import CommandParser
    from positive_vi.vi.CommandVisitor import CommandVisitor

from antlr4 import (CommonTokenStream, InputStream)
from argparse import ArgumentParser
import binascii
import curses.ascii
# import transitions
import yaml
import sys
import os

PROGRAM = 'keys'
VERSION = '0.7.2018'

DEBUG = True
PROMPT = "-- KEYS --"
DEFAULT_ENCODING = 'utf-8'
DEFAULT_WINDOW = 22

class Buffer(_Buffer,
             commands.ViCommands,
             motions.ViMotions):
    pass

class Keys:

    def __init__(self,
                 command=[]):
        """
        """
        self.options = EditOptionMap(window=DEFAULT_WINDOW)
        self.command = command
        self.command_buffer = bytearray()

        # curses.wrapper calls initscr()
        # and passes the result to loop()
        try:
            curses.wrapper(self.on_screen)
        except KeyboardInterrupt:
            print(":quit")

    def config_window(self, window_lines=None) -> Addr:
        """
        We have to combine 4 sources:
        - curses
        - environ
        - more
        - args
        the source $MORE should already have been
        combined at this point, so we don't need
        to consider it here.

        POSIX specifies "COLUMNS -- Override the system-selected horizontal display line size" which implies [curses < environ]

        POSIX specifies "LINES -- Override the system-selected vertical screen size, used as the number of lines in a screenful" which implies [curses < environ]

        POSIX specifies "Any command line options shall be processed after those in the MORE variable" which implies that actual args take precedence over $MORE args, but this should already have been taken care of. [more < args]

        POSIX specifies "The MORE variable shall take precedence over the TERM and LINES variables for determining the number of lines in a screenful." This implies that [environ < more]
        """
        # curses source
        lines = curses.LINES
        cols = curses.COLS

        # environ source
        environ_lines = os.getenv('LINES', None)
        environ_cols = os.getenv('COLUMNS', None)

        if environ_lines is not None:
            lines = environ_lines
        if environ_cols is not None:
            cols = environ_cols

        # combined (more and args) sources
        if window_lines is not None and \
           window_lines != 0:
            lines = window_lines
            assert isinstance(lines, int)

        return Addr(lines, cols)

    def on_screen(self, stdscr):
        self.screen = stdscr
        self.window_addr = self.config_window()
#        self.temp_file = NamedTemporaryFile(encoding=DEFAULT_ENCODING)
        self.buffer = Buffer.from_content(b'', '-', self.window_addr)
        self.redraw()
        while self.loop():
            pass
            

    def loop(self):
        key = self.screen.getkey()
        self.command_buffer.append(ord(key))
        cmd = self.command_buffer
        if self.parse_command(cmd):
            if not self.exec_command(cmd):
                self.quit()
                return False
        self.redraw()
        return True

    def parse_command(self, cmd: bytearray, start='start'):
        lexer = CommandLexer(InputStream(cmd.decode(DEFAULT_ENCODING)))
        parser = CommandParser(CommonTokenStream(lexer))
        visitor = CommandVisitor()
        try:
            tree = getattr(parser, start)()
            return tree.accept(visitor)
        except Exception as exc:
            return None
    
    def exec_command(self, cmd: bytearray):
        pass
    
    def exec_ex_command(self, cmd: bytearray):
        pass
    
    def exec_vi_command(self, cmd: bytearray):
        pass
    
    def exec_vi_motion(self, cmd: bytearray):
        pass
    
    def print_command(self, cmd: bytearray):
        pass
        
    def clear_screen(self):
        pass

    def discard_input(self):
        pass

    def redraw(self):
        """
        more.html: Refresh the Screen
        vi.html: Clear and Redisplay
        vi.html: Redraw Screen
        """
        self.screen.clear()
        for i, line in enumerate(
            self.buffer.visible_lines()):
            bs = bytes(line)
            with open("def", "ab") as writer:
                writer.write(bs)
            self.screen.addstr(i, 0, bs)
        command = bytes(self.command_buffer).decode('utf-8')
        percent = self.buffer.visible_percent()
        prompt = "{:s}({:d}%) {:s}".format(
            PROMPT, percent, command).encode('utf-8')
        self.screen.addstr(self.buffer.scroll_page.line - 1, 0, prompt)

    def quit(self):
        print(":quit")

        
def add_arguments(parser):
    parser.add_argument(
        '-p',
        action='store',
        default=[],
        dest='command')
    return parser


def keys_main():
    parser = add_arguments(ArgumentParser(PROGRAM))
    arguments = parser.parse_args(sys.argv[1:])
    options = vars(arguments)
    Keys(**options)


if __name__ == '__main__':
    keys_main()
