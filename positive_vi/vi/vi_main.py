"""
more is POSIX-UP (User Portability Utilities)
ex is POSIX-UP
vi is POSIX-UP
"""
try:
    from .Buffer import (
        Addr, Buffer as _Buffer,
        commands, modes, motions, options)
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
from argparse import ArgumentParser
import binascii
import curses.ascii
import sys
import os

PROGRAM = 'vi'
VERSION = '0.7.2018'
DEFAULT_DIGIT_ENCODING = 'latin1'
DEBUG = True

CMD_VI_PROMPT 		= "--CMD--"
CMD_EX_PROMPT 		= "--CMD/EX--"
CMD_PENDING_PROMPT 	= "--CMD/PENDING--"
CMD_LINE_PROMPT 	= "--CMD/LINE--"
INP_INSERT_PROMPT 	= "--INPUT--"
INP_REPLACE_PROMPT 	= "--INPUT/REPLACE--"


class Buffer(_Buffer,
             commands.ViCommands,
             motions.ViMotions):
    pass


class View:
    """
    `vi` originally meant "visual" but we are not trying to
    re-write history, just name a class, so we call it `View`.
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
                 # ex-only CLI option
                 suppress=False,
                 # ex-only CLI option
                 visual=True):
        """
        """
        # BEGIN of options
        self.file = file
        self.recover = recover
        self.readonly = readonly
        self.command = command
        self.tag = tag
        self.window = window
        self.suppress = suppress
        self.visual = visual
        # END of options
        # BEGIN of states
        self.last_key = ''
        self.count_digits = bytearray()
        self.command_buf = bytearray()
        self.operand_buf = bytearray()
        self.screen = None
        self.mode = modes.Mode.CMD
        self.inpmode = modes.InputMode.INP_INSERT
        if self.visual:
            self.cmdmode = modes.CommandMode.CMD_VISUAL
        else:
            self.cmdmode = modes.CommandMode.CMD_EXTEND
        # END of states

        if self.recover:
            raise NotImplementedError
        elif self.readonly:
            raise NotImplementedError

        # curses.wrapper calls initscr()
        # and passes the result to loop()
        try:
            curses.wrapper(self.on_screen)
        except StopIteration:
            self.visual = not self.visual
            curses.wrapper(self.on_screen)
        except KeyboardInterrupt:
            self.buffer.c_quit()
        else:
            self.buffer.c_quit()

    def mode_transition_from_command_to_command_visual(self):
        assert self.mode == modes.Mode.CMD
        self.mode = modes.Mode.CMD
        self.cmdmode = modes.CommandMode.CMD_VISUAL

    def mode_transition_from_input_to_command(self):
        assert self.mode == modes.Mode.INP
        self.mode = modes.Mode.CMD

    def mode_transition_from_command_to_input(self):
        assert self.mode == modes.Mode.CMD
        self.mode = modes.Mode.INP

    def mode_to_string(self) -> str:
        if self.mode == modes.Mode.CMD:
            if self.cmdmode == modes.CommandMode.CMD_EXTEND:
                return CMD_EX_PROMPT
            elif self.cmdmode == modes.CommandMode.CMD_VISUAL:
                return CMD_VI_PROMPT
            elif self.cmdmode == modes.CommandMode.CMD_PENDING:
                return CMD_PENDING_PROMPT
            elif self.cmdmode == modes.CommandMode.CMD_LINE:
                return CMD_LINE_PROMPT
            else:
                raise ValueError
        elif self.mode == modes.Mode.INP:
            if self.inpmode == modes.InputMode.INP_INSERT:
                return INP_INSERT_PROMPT
            elif self.inpmode == modes.InputMode.INP_REPLACE:
                return INP_REPLACE_PROMPT
            else:
                raise ValueError
        else:
            raise ValueError

    def config_window(self) -> Addr:
        """
        We have to combine 4 sources:
        - curses
        - environ
        - exinit
        - args
        the source $EXINIT should already have been
        combined at this point, so we don't need
        to consider it here.
        """
        # curses source
        lines = curses.LINES
        cols = curses.COLS

        return Addr(lines, cols)

    def on_screen(self, stdscr):
        os.putenv("ESCDELAY", "0")
        self.screen = stdscr
        self.window = self.config_window()
        self.buffer = Buffer.from_filename(
            self.file[0], self.window)
        # self.screen.nodelay(True)
        self.screen.keypad(False)
        self.screen.notimeout(True)
        self.redraw()
        while self.loop():
            pass

    def execute_command(self, command_buf):
        command = command_buf.decode(self.buffer.encoding)
        if command in [':q', ':quit']:
            self.buffer.c_quit()
            # equivalent to break
            return False
        elif command in [':w', ':write']:
            self.buffer.c_write()
        elif command in [':x', ':xit', ':wq']:
            self.buffer.c_write_and_quit()
            # equivalent to break
            return False
        else:
            pass

        self.mode_transition_from_command_to_command_visual()
        self.discard_input()
        return True

    def loop(self) -> bool:
        key = self.screen.getkey()
        self.last_key = key

        # Implement ex command mode and ex command-line mode
        if self.mode == modes.Mode.CMD and \
           self.cmdmode == modes.CommandMode.CMD_LINE:
            if key == chr(curses.ascii.DEL):
                self.command_buf.pop()
            elif key == chr(curses.ascii.LF):
                if not self.execute_command(self.command_buf):
                    # If we want to continue, then the result
                    # of the function above is True, in which
                    # case we want to redraw(), but if it is
                    # False, then we don't care and we can
                    # return early.
                    return False
            else:
                self.command_buf.append(ord(key))

        # Implement vi text input mode, the Vim
        # documentation calls this "insert" mode, but
        # the POSIX specification makes no mention of
        # the "insert" mode, so we call it input mode.
        elif self.mode == modes.Mode.INP:
            if key == chr(curses.ascii.ESC):
                self.mode_transition_from_input_to_command()
            elif key == chr(curses.ascii.DEL):
                self.buffer.m_delete_character_before_cursor()
            elif key == chr(curses.ascii.NL):
                self.buffer.split_line()
            else:
                self.buffer.insert_char(key)

        # Implement count prefix for motions
        elif key.isdigit():
            self.count_digits.append(ord(key))

        # Implement 1 character motions
        elif len(self.command_buf) == 0:
            if key in ['i', 'I', 'o', 'O', 'a', 'A']:
                self.mode_transition_from_command_to_input()

            if key == 'h':
                self.buffer.m_move_cursor_backward()
            elif key == 'l':
                self.buffer.m_move_cursor_forward()
            elif key == ' ':
                self.buffer.m_scroll_page_forward()
            elif key == curses.ascii.ctrl('F'):
                self.buffer.m_scroll_page_forward()
            elif key == 'b':
                self.buffer.m_scroll_page_backward()
            elif key == curses.ascii.ctrl('B'):
                self.buffer.m_scroll_page_backward()
            elif key == 'i':
                self.buffer.m_insert_before_cursor()
            elif key == 'I':
                self.buffer.m_insert_at_begin_of_line()
            elif key == 'o':
                self.buffer.m_insert_empty_line_below()
            elif key == 'O':
                self.buffer.m_insert_empty_line_above()
            elif key == 'a':
                self.buffer.m_append()
            elif key == 'A':
                self.buffer.m_append_at_end_of_line()
            elif key == curses.ascii.ctrl('E'):
                self.buffer.m_scroll_line_forward(app=self)
            elif key == curses.ascii.ctrl('Y'):
                self.buffer.m_scroll_line_backward(app=self)
            elif key == 'j':
                self.buffer.m_move_cursor_down(app=self)
            elif key == 'k':
                self.buffer.m_move_cursor_up(app=self)
            elif key == curses.ascii.ctrl('D'):
                self.buffer.m_scroll_half_forward()
            elif key == curses.ascii.ctrl('U'):
                self.buffer.m_scroll_half_backward()
            elif key == 'x':
                self.buffer.m_delete_character_at_cursor()
            elif key == 'X':
                self.buffer.m_delete_character_before_cursor()
            elif key == 'Y':
                self.buffer.m_yank_line()
            elif key == 'z':
                self.buffer.m_redraw()
            elif key == 'R':
                raise NotImplementedError
            elif key == 'r':
                self.command_buf.append(ord(key))
            elif key == 'd':
                self.command_buf.append(ord(key))
            elif key == 'm':
                self.command_buf.append(ord(key))
            elif key == 'y':
                self.command_buf.append(ord(key))
            elif key == 'Z':
                self.command_buf.append(ord(key))
            elif key == '[':
                self.command_buf.append(ord(key))
            elif key == ']':
                self.command_buf.append(ord(key))
            elif key == '<':
                self.command_buf.append(ord(key))
            elif key == '>':
                self.command_buf.append(ord(key))
            elif key == 'f':
                self.command_buf.append(ord(key))
            elif key == 't':
                self.command_buf.append(ord(key))
            elif key == 'T':
                self.command_buf.append(ord(key))
            elif key == 'q':
                # equivalent to break
                return False
            elif key in [':', '/', '?']:
                self.cmdmode = modes.CommandMode.CMD_LINE
                self.command_buf.append(ord(key))

        # Implement 2 character motions
        elif len(self.command_buf) == 1:
            first_key = self.command_buf.decode(self.buffer.encoding)
            if first_key == 'Z':
                if key == 'Z':
                    self.buffer.m_write_and_quit()
                    # equivalent to break
                    return False
            elif first_key == '[':
                if key == '[':
                    self.buffer.m_move_to_previous_section()
            elif first_key == ']':
                if key == ']':
                    self.buffer.m_move_to_next_section()
            elif first_key == '<':
                self.buffer.m_shift_left(key)
            elif first_key == '>':
                self.buffer.m_shift_right(key)
            elif first_key == 'd':
                self.buffer.m_delete(key)
            elif first_key == 'm':
                self.buffer.m_mark(key)
            elif first_key == 'r':
                self.buffer.m_replace(key)
            elif first_key == 'f':
                self.buffer.m_find_character_forward(key)
                self.discard_input()
            elif first_key == 'F':
                self.buffer.m_find_character_backward(key)
                self.discard_input()
            elif first_key == 't':
                self.buffer.m_find_character_before_forward(key)
                self.discard_input()
            elif first_key == 'T':
                self.buffer.m_find_character_after_backward(key)
                self.discard_input()
            elif first_key == 'y':
                self.buffer.m_yank(key)
        else:
            # command_buf is non-empty
            print(repr(self.command_buf))
        self.redraw()
        return True

    def discard_input(self):
        self.command_buf.clear()

    def redraw(self):
        """
        more.html: Refresh the Screen
        vi.html: Clear and Redisplay
        vi.html: Redraw Screen
        """
        if self.cmdmode == modes.CommandMode.CMD_EXTEND:
            # simplify output
            return
        self.screen.clear()
        for i, line in enumerate(
            self.buffer.visible_lines()):
            self.screen.addstr(i, 0, bytes(line))

        prompt = self.calculate_the_prompt()
        self.screen.addstr(self.buffer.scr.line - 1, 0, prompt)
        self.screen.move(self.buffer.pos.line - self.buffer.top.line,
                         self.buffer.pos.col - 1)

    def calculate_the_prompt(self) -> bytes:
        if DEBUG:
            command = ' '.join(
                ([self.count_digits.decode(DEFAULT_DIGIT_ENCODING)]
                 if len(self.count_digits) else []) +
                ([self.command_buf.decode(self.buffer.encoding)]
                 if len(self.command_buf) else []) +
                ([self.operand_buf.decode(self.buffer.encoding)]
                 if len(self.operand_buf) else []))
            mode = self.mode_to_string()
            percent = self.buffer.visible_percent()
            prompt = "{:s}({:d}%){:s} {:s}".format(
                mode, percent, repr(self.last_key), command).encode(
                    self.buffer.encoding)
            return prompt
        else:
            mode = self.mode_to_string()
            if len(self.command_buf):
                command = ' '.join(
                    ([self.count_digits.decode(DEFAULT_DIGIT_ENCODING)]
                    if len(self.count_digits) else []) +
                    ([self.command_buf.decode(self.buffer.encoding)]
                    if len(self.command_buf) else []) +
                    ([self.operand_buf.decode(self.buffer.encoding)]
                    if len(self.operand_buf) else []))
                prompt = "{:s} {:s}".format(
                    mode, command).encode(self.buffer.encoding)
            else:
                prompt = "{:s}".format(
                    mode).encode(self.buffer.encoding)
            return prompt

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
                        dest='window',
                        help="Set the window edit option to size.")
    parser.add_argument('file',
                        action='store',
                        nargs='*')
    return parser


def vi_main():
    parser = add_arguments(ArgumentParser(PROGRAM))
    arguments = parser.parse_args()
    options = vars(arguments)
    if DEBUG:
        print(repr(options))
    View(**options)


if __name__ == '__main__':
    vi_main()
