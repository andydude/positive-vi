from dataclasses import dataclass
from typing import List, Optional
from . import CommandImpl as commands
from . import EditMode as modes
from . import EditMotionImpl as motions
from . import EditOption as options

DEFAULT_ENCODING = 'utf-8'


@dataclass
class Addr:
    line: int
    col: int = 1

    @classmethod
    def copy(cls, other):
        assert isinstance(other.line, int)
        assert isinstance(other.col, int)
        return cls(other.line, other.col)

    @classmethod
    def default(cls):
        return cls(1, 1)

    def update(self, other):
        assert isinstance(self.line, int)
        assert isinstance(self.col, int)
        assert isinstance(other.line, int)
        assert isinstance(other.col, int)
        self.line = other.line
        self.col = other.col


@dataclass
class Region:
    start: Addr
    end: Addr


@dataclass
class Buffer:
    """
    The distinction between buffer:
    - lines
    - encoding
    - filename
    and the concept of a cursor in a window:
    - top: Addr
    - pos: Addr
    - scroll_half: Addr
    - scroll_page: Addr
    are not really enforced here.
    """
    lines: List[bytearray]

    pos: Addr 	# represents the pos of cursor
    top: Addr 	# represents the top of screen as a cursor
    scr: Addr 	# represents the size of the screen
    scroll_half: Addr  # represents the scroll_half_* motions
    scroll_page: Addr  # represents the scroll_page_* motions

    encoding: str = 'utf-8'
    filename: str = '-'

    def __getitem__(self, base1):
        return self.lines[base1 - 1]

    def __setitem__(self, base1, value):
        self.lines[base1 - 1] = value

    def last_line_addr(self) -> Addr:
        """
        The character '$' shall address the last line of the edit buffer.
        """
        return Addr(line=len(self.lines))

    def nth_line_addr(self, n: int) -> Addr:
        return Addr.nth_line(n)

    @classmethod
    def marked_line(cls, c: str):
        """
        The address "'x" refers to the line marked with the
        mark name character 'x', which shall be a lowercase
        letter from the portable character set, the backquote
        character, or the single-quote character. It shall be
        an error if the line that was marked is not currently
        present in the edit buffer or the mark has not been set.
        Lines can be marked with the ex mark or k commands,
        or the vi m command.
        """
        return cls(line=c)

    @classmethod
    def from_filename(cls, filename: str,
                  scr: Addr,
                  scroll_page: Optional[Addr] = None,
                  scroll_half: Optional[Addr] = None):
        with open(filename, "rb") as reader:
            return cls.from_reader(reader, filename, scr,
                                   scroll_page,
                                   scroll_half)

    @classmethod
    def from_reader(cls, reader,
                    filename: str,
                  scr: Addr,
                  scroll_page: Optional[Addr] = None,
                  scroll_half: Optional[Addr] = None):
        content = reader.read()
        return cls.from_content(content, filename, scr,
                                scroll_page,
                                scroll_half)

    @classmethod
    def from_content(cls, content: bytes,
                     filename: str,
                  scr: Addr,
                  scroll_page: Optional[Addr] = None,
                  scroll_half: Optional[Addr] = None):
        lines = bytearray(content).split(b'\n')
        if scroll_page is None:
            scroll_page = Addr.copy(scr)
        if scroll_half is None:
            scroll_half = Addr(int(scroll_page.line//2))
        return cls(
            lines=lines,
            filename=filename,
            top=Addr.default(),
            pos=Addr.default(),
            scr=scr,
            scroll_half=scroll_half,
            scroll_page=scroll_page)

    def visible_lines(self, count=None):
        if count is None:
            count = self.scr.line - 1
        return self.lines[
            self.top.line - 1:
            self.top.line - 1 + count]

    def visible_percent(self):
        end = len(self.lines) - self.scr.line
        percent = 100*float(self.top.line)/float(end)
        return int(min(max(percent, 0), 100))

    def validate_current_top(self):
        end = max(1, len(self.lines) - self.scr.line + 2)
        if self.top.line < 1:
            raise ValueError("top is less than the edit buffer!")
            self.top.line = 1
        if self.top.line > end:
            raise ValueError("top is greater than the edit buffer!")
            self.top.line = end

    def validate_current_pos(self):
        end = len(self.lines)
        if self.pos.line < 1:
            # raise ValueError("pos is less than the edit buffer!")
            self.pos.line = 1
        if self.pos.line > end:
            # raise ValueError("pos is greater than the edit buffer!")
            self.pos.line = end

    def update_from_top_to_pos(self):
        # self.pos.line = self.top.line + self.scroll_half.line
        pass

    def update_from_pos_to_top(self):
        """
        This is not specified in POSIX, but
        ThePrimeagen said that centering the cursor
        half-way on the screen is good practice.
        """
        if self.pos.line < self.scroll_half.line + 1:
            self.top.line = 1
        elif (len(self.lines) > self.scroll_half.line) \
            and self.pos.line > (
                len(self.lines) - self.scroll_half.line + 1):
            end = len(self.lines) - self.scr.line + 2
            self.top.line = end
        else:
            mid = self.pos.line - self.scroll_half.line
            self.top.line = mid

    def find_non_blank(self):
        # line_buf = self[self.pos]
        return 1

    def delete_char(self):
        del self.lines[
            self.pos.line - 1][
            self.pos.col - 1]

    def insert_char(self, key):
        self.lines[
            self.pos.line - 1].insert(
            self.pos.col - 1,
            key.encode(self.encoding)[0])
        self.pos.col += 1

    def insert_line(self, line=None):
        if line is None:
            line = bytearray()
        self.lines.insert(
            self.pos.line - 1, line)

    def split_line(self):
        line1 = self.lines[
            self.pos.line - 1][0:self.pos.col - 1]
        line2 = self.lines[
            self.pos.line - 1][self.pos.col - 1:]
        self.lines[self.pos.line - 1] = line2
        self.insert_line(line1)
        self.pos.line += 1
        self.pos.col = 1
