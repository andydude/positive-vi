/* -*- mode: antlr; -*-
 * SPDX-FileCopyrightText: © 2024 Andrew Robbins
 * SPDX-License-Identifier: Apache-2.0
 */
parser grammar CommandParser;
options { tokenVocab = CommandLexer; }

/* Command Line Parsing in ex
 * 1. Leading colon characters shall be skipped
 * 2. Leading blank characters shall be skipped
 * 3. If the leading character is a double-quote character,
 *    the characters up to and including the next 
 *    non-backslash-escaped-newline shall be discarded,
 *    and any subsequent characters shall be parsed 
 *    as a separate command.
 * 4. Leading characters that can be interpreted as 
 *    addressses shall be evaluated;
 * 5. Leading blank characters shall be skipped
 * 6. If the next character is vertical-line or newline:
 *    a. If the next character is newline:
 *       (We're always in visual mode)
 *       i. the current line shall be set to the last address specified.
 *    b. Otherwise, the implied command shall be the print command. 
 *       The last #, p, and l flags specified to any ex command shall 
 *       be remembered and shall apply to this implied command. 
 *       Executing the ex number, print, or list command shall 
 *       set the remembered flags to #, nothing, and l, respectively, 
 *       plus any other flags specified for that execution of the 
 *       number, print, or list command.
 *       If ex is not currently performing a global or v command, 
 *       and no address or count is specified, the current line 
 *       shall be incremented by 1 before the command is executed. 
 *       If incrementing the current line would result in an address 
 *       past the last line in the edit buffer, the command shall fail, 
 *       and the increment shall not happen.
 *    c. The <newline> or <vertical-line> character shall be discarded and 
 *       any subsequent characters shall be parsed as a separate command.
 * 7. The command name shall be comprised of the next character 
 *    (if the character is not alphabetic), or the next character 
 *    and any subsequent alphabetic characters (if the character 
 *    is alphabetic), with the following exceptions:
 *    a. Commands that consist of any prefix of the characters in the 
 *       command name delete, followed immediately by any of the 
 *       characters 'l', 'p', '+', '-', or '#' shall be interpreted 
 *       as a delete command, followed by a <blank>, followed by the 
 *       characters that were not part of the prefix of the delete command. 
 *       The maximum number of characters shall be matched to the command 
 *       name delete; for example, "del" shall not be treated as "de" 
 *       followed by the flag l.
 *    b. Commands that consist of the character 'k', followed by a 
 *       character that can be used as the name of a mark, shall be 
 *       equivalent to the mark command followed by a <blank>, 
 *       followed by the character that followed the 'k'.
 *    c. Commands that consist of the character 's', followed by 
 *       characters that could be interpreted as valid options to the s 
 *       command, shall be the equivalent of the s command, without any 
 *       pattern or replacement values, followed by a <blank>, 
 *       followed by the characters after the 's'.
 */

start : viCommand EOF ;

adr1 : Adr1 ;
adr2 : Adr2 ;
count : Count ;
countCmd : CountCmd ;
value : CountOpt ;
buffer : UnnamedBuffer ;
filename
    : SimpleFileName
    | StringFilename
    ;
directory : filename ;
shellCommand : ShellCommand ;
visType : VisType ;
subOptions : SubOptions ;
windowTypes : WindowTypes ;
character : SimpleFilename ;
letter : SimpleFilename ;
tagString : SimpleFilename ;
pattern : LowerP ;
replacement : LowerR ;
newline : ControlJ ;

flags : Flags ;
lhs : LHS ;
rhs : RHS ;
rePattern
    : SlashSym pattern SlashSym ;
rePattRepl
    : SlashSym pattern SlashSym replacement SlashSym ;
setOptions
    : setOption+
    ;
setOption
    : ExOption (EqualOpt value)?
    | ExOption QuestOpt
    | SetNoSym ExOption
    | SetAllSym
    ;

exCommand
	: 		AbbreviateSym (lhs rhs)?
    | adr1? AppendSym ExclSym?
    | 		ArgsSym
    | adr2? ChangeSym ExclSym? countCmd
    | 		ChangeDirSym ExclSym? directory
    | adr2? CopySym adr1 flags?
    | adr2? DeleteSym buffer? countCmd? flags?
    | 		EditSym ExclSym? (PlusSym exCommand)? filename?
    | 		FileSym filename?
    | adr2? GlobalSym rePattern
    | adr1? InsertSym ExclSym?
    | adr2? JoinSym ExclSym? countCmd? flags?
    | adr2? ListSym countCmd? flags?
    | 		MapSym ExclSym? (lhs rhs)?
    | adr1? MarkSym character
    | adr2? MoveSym adr1 flags?
    | 		NextSym ExclSym?
    | adr2? NumberSym countCmd? flags?
    | adr1? OpenSym rePattern flags?
    |       PreserveSym
    | adr2? PrintSym countCmd? flags?
    | adr1? PutSym buffer?
    |       QuitSym ExclSym?
    | adr1? ReadSym ExclSym? filename?
    |       RecoverSym ExclSym? filename
    |       RewindSym ExclSym?
    |       SetSym setOptions? (ColonOptEnd | SetOptEnd)
    |       ShellSym
    | 		SourceSym filename
    | adr2? SubstituteSym rePattRepl subOptions? countCmd? flags?
    | adr2? SubAndSym subOptions? countCmd? flags?
    | adr2? SubTildeSym subOptions? countCmd? flags?
    |		SuspendSym ExclSym?
    |		TagSym ExclSym? tagString
    | 		UnabbreviateSym lhs
    |		UndoSym
    |		UnmapSym ExclSym? lhs
    |		VersionSym
    | adr1? VisualSym visType? countCmd? flags?
    | adr2? WriteSym ExclSym? RShift? filename?
    | adr2? WriteQuitSym ExclSym? RShift? filename?
    | adr2? WriteExitSym ExclSym? filename?
    | adr2? YankSym buffer? countCmd?
    | adr1? WindowSym windowTypes? countCmd? flags?
    | adr1? ExclSym shellCommand
    | adr2? LShiftSym countCmd? flags?
    | adr2? RShiftSym countCmd? flags?
    | 		ControlD
    | adr1? EqualSym flags?
    | adr2? AtExecuteSym buffer adr2? AtTimesSym buffer
    ;

viMotion
    : count? ControlH /* move_cursor_backward */
    | count? LowerH   /* move_cursor_backward */
    | count? ControlJ /* move_cursor_down */
    | count? ControlM /* move_cursor_down */
    | count? ControlN /* move_cursor_down */
    | count? LowerJ   /* move_cursor_down */
    | count? Plus 	  /* move_cursor_down */
    | count? Space	  /* move_cursor_forward */
    | count? LowerL	  /* move_cursor_forward */
    | count? ControlP /* move_cursor_up */
    | count? LowerK   /* move_cursor_up */
    | count? Minus    /* move_cursor_up */
    | count? LParen   /* move_to_sentance_backward */
    | count? RParen   /* move_to_sentance_forward */
    | count? LBrace   /* move_to_paragraph_backward */
    | count? RBrace   /* move_to_paragraph_forward */
    | count? DLBrack  /* move_to_section_backward */
    | count? DRBrack  /* move_to_section_forward */
    | count? Dollar   /* move_to_end_of_line */
    |        Percent  /* move_to_maching_char */
    |        Amp      /* repeat_substitution */
    |        Apos character /* move_to_previous_line */
    |        Grave character /* move_to_previous_context */
    |        Pow      /* move_to_first_non_blank */
    | count? Low      /* current_and_line_above */
    | count? Vert     /* move_to_col */
    | count? Comma    /* find_character_backward*/
    | count? Slash    /* find_re */
    | count? Zero     /* move_to_first_char_in_line */
    | count? Semi     /* repeat_find_ch */
    |        Quest /* find_re_backward */
    | count? LowerB   /* move_to_word_backward */
    | count? UpperB   /* move_to_bigword_backward */
    | count? LowerE   /* move_to_end_of_word */
    | count? UpperE   /* move_to_end_of_bigword */
    | count? LowerF character /* find_char_forward */
    | count? UpperF character /* find_char_backward */
    | count? UpperG   /* move_to_line */
    | count? UpperH   /* move_to_screen_top */
    | count? UpperL   /* move_to_screen_bottom */
    |        UpperM   /* move_to_screen_middle */
    |        LowerN   /* repeat_find_re_forward */
    |        UpperN   /* repeat_find_re_backward */
    | count? LowerT character /* find_char_before_forward */
    | count? UpperT character /* find_char_after_backward */
    | count? LowerW   /* move_to_begin_of_word */
    | count? UpperW   /* move_to_begin_of_bigword */
    ;

viCommand
    : count? ControlU /* scroll_half_backward */
    | count? ControlD /* scroll_half_forward */
    | count? ControlY /* scroll_line_backward */
    | count? ControlE /* scroll_line_forward */
    | count? ControlB /* scroll_page_backward */
    | count? ControlF /* scroll_page_forward */
    |        ControlG /* display_info */
    |        ControlL /* clear_and_redraw */
    |        ControlR /* redraw */
    |        ControlPow /* edit */
    |        ControlLBrack /* terminate_command */
    |        ControlRBrack /* search_for_tag */
    | count? Excl viMotion shellCommand newline /* replace_shell */
    | count? Dot	  /* repeat */
    | count? Colon exCommand ColonEnd /* execute_ex_command */
    | count? LShift viMotion
    | count? RShift viMotion
    |        AtExecuteSym buffer
    |        SubTildeSym
    | count? LowerA
    | count? UpperA
    | buffer? count? LowerC viMotion
    | buffer? count? UpperC
    | buffer? count? LowerD viMotion
    | buffer? UpperD
    | count? LowerI
    | count? UpperI
    | count? UpperJ
    |        LowerM letter
    |        LowerO
    |        UpperO
    | buffer? LowerP
    | buffer? UpperP
    |        UpperQ
    | count? LowerR character
    |        UpperR
    | buffer? count? LowerS
    | buffer? count? UpperS
    |        LowerU        
    |        UpperU
    | buffer? count? LowerX
    | buffer? count? UpperX
    | buffer? count? LowerY viMotion
    | buffer? count? UpperY
    | count? LowerZ
    |        UpperZ UpperZ
    |        viMotion
    ;

inCommand
    : ControlD  /* noop */
    | ControlH  /* backspace autoindent */
    | ControlJ  /* insert_newline */
    | ControlM  /* insert_newline */
    | ControlT  /* move_to_shiftwidth */
    | ControlU  /* move_to_character */
    | ControlV  /* as_literal */
    | ControlQ  /* as_literal */
    | ControlW  /* move_to_word_backward */
    | ControlLBrack /* terminate_input_mode */
    ;

exMoreCommand
    : Slash ExclSym? pattern
    | Quest ExclSym? pattern
    | Colon NextSym
    | Colon PrevSym
    | Colon LowerQ
    | Colon TagSym tagString
    ;

viMoreCommand
    /* motion-ish */
    : count? Space    /* scroll_page_forward */
    | count? LowerF   /* scroll_page_forward */
    | count? ControlF /* scroll_page_forward */
    | count? LowerB   /* scroll_page_backward */
    | count? ControlB /* scroll_page_backward */
    | count? LowerJ   /* scroll_line_forward */
    | count? ControlJ /* scroll_line_forward */
    | count? LowerK   /* scroll_line_backward */
    | count? LowerD   /* scroll_half_forward */
    | count? ControlD /* scroll_half_forward */
    | count? LowerU   /* scroll_half_backward */
    | count? ControlU /* scroll_half_backward */
    | count? LowerS   /* scroll_skip_forward */
    | count? LowerG   /* move_to_begin_of_file */
    | count? UpperG   /* move_to_env_of_file */
    |        LowerR	  /* redraw */
    |        ControlL /* redraw */
    |        UpperR   /* discard_and_redraw */
    |        LowerM letter /* mark */
    |        Apos letter /* move_to_mark */
    |        Apos Apos /* move_to_mark_backward */
    | count? LowerN
    | count? UpperN
    |        LowerV   /* visual */
    |        Equal    /* display_info */
    |        ControlG /* display_info */
    |        LowerQ   /* quit */
    |        UpperZ UpperZ /* quit */
    | count? exMoreCommand newline
    ;
        

        
