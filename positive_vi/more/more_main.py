"""
more is POSIX-UP (User Portability Utilities)
ex is POSIX-UP
vi is POSIX-UP
"""
try:
    from ..vi.Buffer import (Addr, Buffer as _Buffer,
        commands, modes, motions, options)
except ImportError:
    from editbuffer import (Addr, Buffer as _Buffer,
        commands, modes, motions, options)

from argparse import ArgumentParser
import binascii
import curses.ascii
import sys
import os

PROGRAM = 'more'
VERSION = '0.7.2018'

PROMPT = "-- MORE --"


class Buffer(_Buffer,
             commands.ViCommands,
             motions.ViMotions):
    pass

class More:

    def __init__(self,
                 file,
                 clear_screen=False,
                 quit_at_eof=False,
                 ignore_case=False,
                 single_empty_line=False,
                 underline_special=False,
                 command=[],
                 tag=None,
                 # vi scroll edit option*2
                 # vi window edit option
                 window=0):
        """
        """
        # BEGIN of options
        self.file = file
        self.clear_screen = clear_screen
        self.quit_at_eof = quit_at_eof
        self.ignore_case = ignore_case
        self.single_empty_line = single_empty_line
        self.underline_special = underline_special
        self.window = window
        self.command = command
        self.tag = tag
        # END of options
        # BEGIN of states
        self.last_key = ''
        self.count_digits = bytearray()
        self.command_buf = bytearray()
        self.operand_buf = bytearray()
        self.operand_mode = False
        self.screen = None
        # END of states

        if self.clear_screen:
            raise NotImplementedError
        elif self.quit_at_eof:
            raise NotImplementedError
        elif self.ignore_case:
            raise NotImplementedError
        elif self.single_empty_line:
            raise NotImplementedError
        elif self.underline_special:
            raise NotImplementedError

        # curses.wrapper calls initscr()
        # and passes the result to loop()
        try:
            curses.wrapper(self.on_screen)
        except KeyboardInterrupt:
            print("quit gracefully")

    def count(self):
        count = bytes(self.count_digits).decode('utf-8')
        self.count_digits.clear()
        return count

    def config_window(self) -> Addr:
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
        if self.window is not None and \
           self.window != 0:
            lines = self.window
            assert isinstance(lines, int)

        return Addr(lines, cols)

    def on_screen(self, stdscr):
        self.screen = stdscr
        window = self.config_window()
        self.buffer = Buffer.from_file(
            self.file[0], window)
        self.redraw()
        while True:
            self.loop()
            
    def loop(self):
            key = self.screen.getkey()
            self.last_key = key
            if self.operand_mode:
                if key == '\n':
                    if chr(self.command_buf[0]) == '/':
                        if chr(self.command_buf[1]) == '!':
                            raise NotImplementedError("forward re!")
                        else:
                            raise NotImplementedError("forward re")
                    elif chr(self.command_buf[0]) == '?':
                        if chr(self.command_buf[1]) == '!':
                            raise NotImplementedError("backward re!")
                        else:
                            raise NotImplementedError("backward re")
                    elif chr(self.command_buf[0]) == ':':
                        if chr(self.command_buf[1]) == 'e':
                            self.open_new_file()
                            return True
                self.operand_buf.append(chr(key))
            elif key.isdigit():
                self.count_digits.append(ord(key))
            elif key == ':':
                self.command_buf.append(ord(key))
                self.operand_mode = True
            elif key == '/':
                self.command_buf.append(ord(key))
                self.operand_mode = True
            elif key == '?':
                self.command_buf.append(ord(key))
                self.operand_mode = True
            elif len(self.command_buf) == 0:
                # command_buf is empty
                if key == 'h':
                    self.usage_summary()
                elif key == ' ':
                    self.buffer.m_scroll_page_forward()
                elif key == 'f':
                    self.buffer.m_scroll_page_forward()
                elif key == curses.ascii.ctrl('F'):
                    self.buffer.m_scroll_page_forward()
                elif key == 'b':
                    self.buffer.m_scroll_page_backward()
                elif key == curses.ascii.ctrl('B'):
                    self.buffer.m_scroll_page_backward()
                elif key == 'j':
                    self.buffer.m_scroll_line_forward()
                elif key == curses.ascii.ctrl('J'):
                    self.buffer.m_scroll_line_forward()
                elif key == 'k':
                    self.buffer.m_scroll_line_backward()
                elif key == 'd':
                    self.buffer.m_scroll_half_forward()
                elif key == curses.ascii.ctrl('D'):
                    self.buffer.m_scroll_half_forward()
                elif key == 'u':
                    self.buffer.m_scroll_half_backward()
                elif key == curses.ascii.ctrl('U'):
                    self.buffer.m_scroll_half_backward()
                elif key == 'g':
                    self.buffer.m_goto_begin_of_file()
                elif key == 'G':
                    self.buffer.m_goto_end_of_file()
                elif key == 'r':
                    self.redraw()
                elif key == curses.ascii.ctrl('L'):
                    self.redraw()
                elif key == 'R':
                    self.discard_input()
                    self.redraw()
                elif key == 'q':
                    self.quit()
                    return False
            else:
                # command_buf is non-empty
                if key == 'e':
                    self.filename_mode = True
                    return True
                elif key == 'n':
                    self.c_next()
                    return False
                elif key == 'p':
                    self.c_()
                    return False
                elif key == 'q':
                    self.quit()
                    return False
                elif key == 't':
                    raise NotImplementedError
            self.redraw()
            return True

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
        command = ' '.join(
            ([self.count_digits.decode('utf-8')]
             if len(self.count_digits) else []) +
            ([self.command_buf.decode('utf-8')]
             if len(self.command_buf) else []) +
            ([self.operand_buf.decode('utf-8')]
             if len(self.operand_buf) else []))
        percent = self.buffer.visible_percent()
        prompt = "{:s}({:d}%){:s}".format(
            PROMPT, percent, command).encode('utf-8')
        #prompt = "{:s}({:d}%) L{:s}".format(PROMPT, percent,
        #     repr(self.last_key)).encode('utf-8')
        #inascii.hexlify(bytes(self.last_key.encode('utf-8')))
        self.screen.addstr(self.buffer.scroll_page.line - 1, 0, prompt)

    def quit(self):
        print("quit intentionally")

def add_arguments(parser):
    parser.add_argument('-c',
                        action='store_true',
                        default=False,
                        dest='clear_screen')
    parser.add_argument('-e',
                        action='store_true',
                        default=False,
                        dest='quit_at_eof')
    parser.add_argument('-i',
                        action='store_true',
                        default=False,
                        dest='ignore_case')
    parser.add_argument('-s',
                        action='store_true',
                        default=False,
                        dest='single_empty_line')
    parser.add_argument('-u',
                        action='store_true',
                        default=False,
                        dest='underline_special')
    parser.add_argument('-n',
                        action='store',
                        default=0,
                        dest='window',
                        type=int)
    parser.add_argument('-p',
                        action='store',
                        default=[],
                        dest='command')
    parser.add_argument('-t',
                        action='store',
                        default=None,
                        dest='tag')
    parser.add_argument('file',
                        action='store',
                        nargs='*')
    return parser


def more_main():
    parser = add_arguments(ArgumentParser(PROGRAM))

    # Process $MORE options first (as per POSIX)
    more_environ = os.getenv('MORE', '')
    more_arguments = parser.parse_args(more_environ)
    more_options = vars(more_arguments)

    # Process actual options second (as per POSIX)
    act_arguments = parser.parse_args(sys.argv[1:])
    act_options = vars(act_arguments)

    # Combine more and args (see config_window())
    more_options.update(act_options)
    More(**more_options)


if __name__ == '__main__':
    more_main()
