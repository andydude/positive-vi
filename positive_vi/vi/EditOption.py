from enum import Enum


class EditOpt(Enum):
    o_autoindent 	= "autoindent"
    o_autoprint 	= "autoprint"
    o_autowrite 	= "autowrite"
    o_beautify 		= "beautify"
    o_directory 	= "directory"
    o_edcompatible 	= "edcompatible"
    o_errorbells 	= "errorbells"
    o_exrc 			= "exrc"
    o_ignorecase 	= "ignorecase"
    o_list 			= "list"
    o_magic 		= "magic"
    o_mesg 			= "mesg"
    o_number 		= "number"
    o_paragraphs	= "paragraphs"
    o_prompt 		= "prompt"
    o_readonly  	= "readonly"
    o_redraw 		= "redraw"
    o_remap 		= "remap"
    o_report 		= "report"
    
    # Buffer.scroll_half (scr.line - 1)/2
    o_scroll 		= "scroll"
    o_sections  	= "sections"
    o_shell 		= "shell"  # Env.SHELL
    o_shiftwidth 	= "shiftwidth"
    o_showmatch 	= "showmatch"
    o_showmode  	= "showmode"
    o_slowopen  	= "slowopen"
    o_tabstop 		= "tabstop"
    o_taglength 	= "taglength"
    o_tags 			= "tags"
    o_term 			= "term"  # Env.TERM
    o_terse 		= "terse"
    o_warn 			= "warn"

    # Buffer.scroll_page (scr.line - 1)
    o_window 		= "window"
    o_wrapmargin 	= "wrapmargin"
    o_wrapscan  	= "wrapscan"
    o_writeany  	= "writeany"
