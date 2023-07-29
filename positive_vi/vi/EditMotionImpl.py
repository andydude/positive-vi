from . import EditMode as modes
from . import EditOption as options


class ViMotions:
    """
    We prefix everything with "m_" for edit motions.
    """
        

    # def move_to_column(self):  # |
    def m_move_to_column(self, count=None, app=None):
        """
        vi.html: Move Specific Column Position
        vi:html: [count] |
        """
        if count:
            self.pos.col = count
        else:
            self.pos.col = 1
        self.update_from_pos_to_top()
        self.validate_current_pos()
        self.validate_current_top()

    # def move_to_line(self):  # G
    def m_move_to_line(self, count=None, app=None):
        """
        more.html: Go to Beginning-of-File
        more.html: [count] g
        more.html: Go to End-of-File
        more.html: [count] G
        vi.html: Move to Line
        vi.html: [count] G

        If count is not specified, it shall default to the last
        line of the edit buffer. If count is greater than the
        last line of the edit buffer, it shall be an error.
        """
        if count is not None:
            self.pos.line = count
        else:
            end = (len(self.lines) - self.scr.line)
            self.pos.line = end
        self.update_from_pos_to_top()
        self.validate_current_pos()
        self.validate_current_top()
        
    # def m_move_cursor_backward(self):  # control-H
    def m_move_cursor_backward(self, count=None, app=None):
        """
        vi.html: [count] <control>-H
        vi.html: [count] h
        """
        count = count if count is not None else 1
        self.m_move_to_column(self.pos.col - count)
        
    # def move_cursor_forward(self):
    def m_move_cursor_forward(self, count=None, app=None):
        """
        vi.html: [count] <space>
        vi.html: [count] l
        """
        count = count if count is not None else 1
        self.m_move_to_column(self.pos.col + count)

    def m_move_cursor_up(self, app=None):  # k
        """
        vi.html: Move Up
        vi.html: [count] <control>-P
        vi.html: [count] k
        vi.html: [count] -
        """
        self.pos.line -= 1
        self.update_from_pos_to_top()
        self.validate_current_top()
        self.validate_current_pos()
        
    def m_move_cursor_down(self, app=None):  # j
        """
        vi.html: Move Down
        vi.html: [count] <newline>
        vi.html: [count] <control>-J
        vi.html: [count] <control>-M
        vi.html: [count] <control>-N
        vi.html: [count] j
        vi.html: [count] <CR>
        vi.html: [count] +
        """
        self.pos.line += 1
        self.update_from_pos_to_top()
        self.validate_current_top()
        self.validate_current_pos()

    # def scroll_half_backward(self):  # control-U
    def m_scroll_half_backward(self, app=None):
        """
        more.html: Scroll Backward One Half Screenful
        more.html: [count] u
        more.html: [count] <control>-U
        vi.html: Scroll Backward
        vi.html: [count] <control>-U
        gnu/less/command.c: A_B_SCROLL
        """
        self.pos.line -= self.scroll_half.line
        self.pos.col = self.find_non_blank()
        self.update_from_pos_to_top()
        self.validate_current_top()
        self.validate_current_pos()

    # def scroll_half_forward(self):  # control-D
    def m_scroll_half_forward(self, app=None):
        """
        more.html: Scroll Forward One Half Screenful
        more.html: [count] d
        more.html: [count] <control>-D
        vi.html: Scroll Forward
        vi.html: [count] <control>-D
        util-linux/more.c: set_scroll_len
        gnu/less/command.c: A_F_SCROLL
        """
        self.pos.line += self.scroll_half.line
        self.pos.col = self.find_non_blank()
        self.update_from_pos_to_top()
        self.validate_current_pos()
        self.validate_current_top()

    def m_scroll_line_backward(self, app=None):
        """
        more.html: Scroll Backward One Line
        more.html: [count] k
        vi.html: Scroll Backward by Line
        vi.html: [count] <control>-Y
        gnu/less/command.c: A_B_LINE
        """
        # if app is not None and app.cmdmode == modes.CommandMode.CMD_MORE:
        #     self.pos.line -= 1
        #     self.top.line -= 1
        # else:
        #     self.pos.line -= 1
        #     self.update_from_pos_to_top()
        self.top.line -= 1
        self.update_from_top_to_pos()
        self.validate_current_top()
        self.validate_current_pos()

    def m_scroll_line_forward(self, app=None):
        """
        more.html: Scroll Forward One Line
        more.html: [count] j
        more.html: [count] <control>-J
        vi.html: Scroll Forward by Line
        vi.html: [count] <control>-E
        gnu/less/command.c: A_F_LINE
        """
        self.top.line += 1
        self.update_from_top_to_pos()
        self.validate_current_pos()
        self.validate_current_top()
            
    def m_scroll_page_backward(self, app=None):
        """
        more.html: Scroll Backward One Screenful
        more.html: [count] b
        more.html: [count] <control>-B
        vi.html: Page Backward
        vi.html: [count] <control>-B
        util-linux/more.c: backwards
        gnu/less/command.c: A_B_SCREEN
        """
        self.pos.line -= self.scroll_page.line
        self.pos.col = self.find_non_blank()
        self.update_from_pos_to_top()
        self.validate_current_pos()
        self.validate_current_top()

    def m_scroll_page_forward(self, app=None):
        """
        more.html: Scroll Forward One Screenful
        more.html: [count] f
        more.html: [count] <control>-F
        more.html: [count] <space>
        vi.html: Page Forward
        vi.html: [count] <control>-F
        util-linux/more.c: skip_forward_screen
        gnu/less/command.c: A_F_SCREEN
        """
        self.pos.line += self.scroll_page.line
        self.pos.col = self.find_non_blank()
        self.update_from_pos_to_top()
        self.validate_current_pos()
        self.validate_current_top()

    def m_scroll_skip_forward(self, app=None):
        """
        more.html: Skip Forward One Line
        more.html: [count] s
        util-linux/more.c: skip_forward_line

        I believe this is equivalent to [screen+count] j
        """
        pass
    
    def m_display_info(self):  # control-G
        """
        vi.html: Display Information
        vi.html: <control>-G

        Write an informational message. If the file has a current pathname, it shall be included in this message; otherwise, the message shall indicate that there is no current pathname. If the edit buffer contains lines, the current line number and the number of lines in the edit buffer shall be included in this message; otherwise, the message shall indicate that the edit buffer is empty. If the edit buffer has been modified since the last complete write, this fact shall be included in this message. If the readonly edit option is set, this fact shall be included in this message. The message may contain other unspecified information.
        """
        pass

    def m_clear_and_redisplay(self):  # control-L
        pass

    def m_redraw_screen(self):  # control-R
        pass

    def m_edit_alternate_file(self):  # control-^
        pass

    def m_terminate_mode(self):  # esc
        pass

    def m_search_tagstring(self):  # esc
        pass

    def m_replace_text_with_results_from_shell_command(self):  # !
        pass

    def m_move_cursor_to_end_of_line(self):  # $
        pass

    def m_move_cursor_to_maching_character(self):  # %
        pass

    def m_repeat_substitution(self):  # &
        pass

    def m_move_to_previous_line(self):  # '
        pass

    def m_move_to_previous_context(self):  # `
        pass

    def m_move_to_previous_section(self):  # [[
        pass

    def m_move_to_next_section(self):  # ]]
        pass

    def m_move_to_first_non_blank(self):  # ^
        pass

    def m_current_and_line_above(self):  # _
        pass

    def m_move_to_sentance_backward(self):  # (
        pass

    def m_move_to_sentance_forward(self):  # )
        pass

    def m_move_to_paragraph_backward(self):  # {
        pass

    def m_move_to_paragraph_forward(self):  # }
        pass

    def m_reverse_find_character(self):  # ,
        pass

    def m_repeat(self):  # .
        pass

    def m_find_regular_expression(self):  # /
        pass

    def m_move_to_first_character_in_line(self):  # 0
        pass

    def m_execute_an_ex_command(self):  # :
        pass

    def m_repeat_find(self):  # ;
        pass

    def m_shift_left(self):  # <
        pass

    def m_shift_right(self):  # >
        pass

    def m_scan_backward_for_regular_expression(self):  # ?
        pass

    def m_execute(self):  # @
        pass

    def m_reverse_case(self):  # ~
        pass

    def m_append(self):  # a
        """
        EnterMode(text_input_mode)
        """
        pass

    def m_append_at_end_of_line(self):  # A
        self.m_move_to_column(self)

    def m_change(self):  # c
        """
        EnterMode(text_input_mode)
        """
        pass

    def m_change_to_end_of_line(self):  # C
        """
        EnterMode(text_input_mode)
        """
        pass

    def m_delete(self):  # d
        pass

    def m_delete_to_end_of_line(self):  # D
        pass

    def m_move_to_begin_of_word(self):  # w
        """
        vi.html: Move to Beginning of Word
        vi.html: [count] w
        """
        pass

    def m_move_to_begin_of_bigword(self):  # W
        """
        vi.html: Move to Beginning of Word
        vi.html: [count] W
        """
        pass

    def m_move_to_end_of_word(self):  # e
        """
        vi.html Move to End of Word
        """
        pass

    def m_move_to_end_of_bigword(self):  # E
        """
        vi.html Move to End of Bigword
        """
        pass

    def m_find_word_backward(self):  # b
        """
        vi.html: Move Backward to Preceding word
        vi.html: [count] b
        """
        pass

    def m_find_bigword_backward(self):  # B
        """
        vi.html: Move Backward to Preceding Bigword
        """
        pass

    def m_find_character_forward(self, character, count=None):
        """
        vi.html: [count] f (character)
        """
        line = self.lines[self.pos.line - 1]
        matches = [
            (i, c)
            for i, c in zip(range(self.pos.col, len(line)),
                                line[self.pos.col - 1:])
            if chr(c) == character
        ]
        if len(matches) == 0:
            raise ValueError("find_character_forward" + repr(matches))
        i = matches[0][0]
        self.m_move_to_column(i)

    def m_find_character_backward(self, character, count=None):
        """
        vi.html: Find Character in Current Line (Reverse)
        vi.html: [count] F (character)
        """
        line = self.lines[self.pos.line - 1]
        matches = [
            (i, c)
            for i, c in zip(range(1, self.pos.col),
                            line[0:self.pos.col - 1])
            if chr(c) == character
        ]
        if len(matches) == 0:
            raise ValueError("find_character_backward")
        i = matches[-1][0]
        self.m_move_to_column(i)

    def m_insert_before_cursor(self):  # i
        """
        EnterMode(text_input_mode)
        """
        pass
    
    def m_insert_at_begin_of_line(self):  # I
        self.m_move_to_column(1)

    def m_join(self):  # J
        pass

    def m_move_to_screen_top(self):  # H
        pass
    
    def m_move_to_screen_bottom(self):  # L
        pass

    def m_move_to_screen_middle(self):  # M
        pass

    def m_mark_position(self):  # m
        pass
    
    def m_repeat_find_forward(self):  # n
        pass

    def m_repeat_find_backward(self):  # N
        pass

    def m_insert_empty_line_below(self):  # o
        self.m_move_cursor_down()
        self.m_move_to_column(1)
        self.insert_line()
    
    def m_insert_empty_line_above(self):  # O
        self.m_move_to_column(1)
        self.insert_line()

    def m_put_from_buffer_following(self):  # p
        pass

    def m_put_from_buffer_before(self):  # P
        pass
    
    def m_enter_ex_mode(self):  # Q
        raise NotImplementedError

    def m_replace_character(self):  # r
        pass

    def m_replace_characters(self):  # R
        raise NotImplementedError
    
    def m_substitute_character(self):  # s
        pass

    def m_substitute_lines(self):  # S
        pass

    def m_find_character_before_forward(self, character, count=None):
        """
        vi.html: Move Cursor to Before Character (Forward)
        vi.html: [count] t (character)
        """
        self.m_find_character_forward(character)
        self.m_move_cursor_backward()
    
    def m_find_character_after_backward(self, character, count=None):
        """
        vi.html: Move Cursor to After Character (Reverse)
        vi.html: [count] T (character)
        """
        self.m_find_character_backward(character)
        self.m_move_cursor_forward()

    def m_undo(self):  # u
        pass

    def m_undo_current_line(self):  # U
        pass
    
    def m_delete_character_at_cursor(self):  # x
        """
        vi.html: Delete Character at Cursor
        vi.html: [buffer][count] x
        """
        self.delete_char()
    
    def m_delete_character_before_cursor(self):  # X
        """
        vi.html: Delete Character at Cursor
        vi.html: [buffer][count] x
        """
        self.pos.col -= 1
        self.delete_char()
        

    def m_yank(self):  # y
        pass

    def m_yank_line(self):  # Y
        pass
    
    def m_redraw_window(self):  # z
        pass

    def m_write_and_quit(self):
        self.c_write_and_quit()
