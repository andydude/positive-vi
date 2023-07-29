from . import EditMode as modes
from . import EditOption as options

    
class ViCommands:
    """
    We prefix everything with "c_" for edit commands.
    """
    

    def c_abbreviate(self):
        pass

    def c_append(self):
        """
        EnterMode(text_input_mode)
        """
        pass

    def c_arguments(self):
        pass

    def c_change(self):
        """
        EnterMode(text_input_mode)
        """
        pass

    def c_chdir(self):
        pass

    def c_copy(self):
        pass

    def c_delete(self):
        pass

    def c_edit(self):
        pass

    def c_ex(self):
        pass

    def c_file(self):
        pass

    def c_global(self):
        pass

    def c_insert(self):
        pass

    def c_join(self):
        pass

    def c_list(self):
        pass

    def c_map(self):
        pass

    def c_mark(self):
        pass

    def c_move(self):
        pass

    def c_next(self):
        pass

    def c_number(self):
        pass

    def c_open(self):
        pass

    def c_preserve(self):
        pass

    def c_print(self):
        pass

    def c_put(self):
        pass

    def c_quit(self, force=False):
        """
        ex.html: q[uit][!]
        """
        print(":quit")

    def c_read(self):
        pass

    def c_recover(self):
        pass

    def c_rewind(self):
        pass

    def c_set(self):
        pass

    def c_shell(self):
        pass

    def c_source(self):
        pass

    def c_substitute(self):
        pass

    def c_suspend(self):
        pass

    def c_tag(self):
        pass

    def c_unabbreviate(self):
        pass

    def c_undo(self):
        pass

    def c_unmap(self):
        pass

    def c_version(self):
        pass

    def c_visual(self):
        pass

    def c_write(self, region=None, file=None, append=False):
        """
        ex.html: Write
        ex.html: [2addr] w[rite][!][>>][file]
        ex.html: [2addr] w[rite][!][file]
        """
        filemode = "w+b" if append else "wb"
        with open(self.filename, filemode) as writer:
            content = b'\n'.join(map(bytes, self.lines))
            writer.write(content)

    def c_write_and_quit(self, region=None, file=None):
        """
        ex.html: Write and Exit
        ex.html: [2addr] x[it][!][file]
        ex.html: [2addr] wq[!][>>][file]
        vi.html: Exit
        vi.html: ZZ
        """
        self.c_write(region=region, file=file)
        self.c_quit()

    def c_yank(self):
        pass

    def c_window(self):
        pass

    def c_escape(self):
        pass

    def c_shift_left(self):
        pass

    def c_shift_right(self):
        pass

    def c_write_line_number(self):
        """
        ex.html: File
        ex.html: f[ile][FILE]
        ex.html: Write Line Number
        ex.html: [1addr] = [flags]
        If line is not specified, it shall default to the last line in the edit buffer. Write the line number of the specified line.
        Write an informational message. If the file has a current pathname, it shall be included in this message; otherwise, the message shall indicate that there is no current pathname. If the edit buffer contains lines, the current line number and the number of lines in the edit buffer shall be included in this message; otherwise, the message shall indicate that the edit buffer is empty. If the edit buffer has been modified since the last complete write, this fact shall be included in this message. If the readonly edit option is set, this fact shall be included in this message. The message may contain other unspecified information.
        """
        pass

    def c_execute(self):
        pass
