from .EditOption import EditOpt
from collections.abc import MutableMapping
from os import getenv


BOOLS = [
    EditOpt.o_autoindent,
    EditOpt.o_autoprint,
    EditOpt.o_autowrite,
    EditOpt.o_beautify,
    EditOpt.o_edcompatible,
    EditOpt.o_errorbells,
    EditOpt.o_exrc,
    EditOpt.o_ignorecase,
    EditOpt.o_list,
    EditOpt.o_magic,
    EditOpt.o_mesg,
    EditOpt.o_number,
    EditOpt.o_prompt,
    EditOpt.o_readonly,
    EditOpt.o_redraw,
    EditOpt.o_remap,
    EditOpt.o_showmatch,
    EditOpt.o_showmode,
    EditOpt.o_slowopen,
    EditOpt.o_terse,
    EditOpt.o_warn,
    EditOpt.o_wrapscan,
    EditOpt.o_writeany,
]


TYPES = {
    EditOpt.o_directory: str,
    EditOpt.o_paragraphs: str,
    EditOpt.o_report: int,
    EditOpt.o_scroll: int,
    EditOpt.o_sections: str,
    EditOpt.o_shell: str,
    EditOpt.o_shiftwidth: int,
    EditOpt.o_tabstop: int,
    EditOpt.o_taglength: int,
    EditOpt.o_tags: str,
    EditOpt.o_term: str,
    EditOpt.o_window: int,
    EditOpt.o_wrapmargin: int,
}


class EditOptionMap(MutableMapping):

    def __init__(self, window):
        assert isinstance(window, int)
        scroll = int(window//2)

        # Default null/zero
        self.v = dict()
        for k, t in TYPES.items():
            if t == int:
                self.v[k] = 0
            elif t == str:
                self.v[k] = ''
        for k in BOOLS:
            self.v[k] = False

        # Default according to POSIX
        self.v[EditOpt.o_autoprint] = True
        self.v[EditOpt.o_magic] = True
        self.v[EditOpt.o_mesg] = True
        self.v[EditOpt.o_prompt] = True
        self.v[EditOpt.o_remap] = True
        self.v[EditOpt.o_report] = 5
        self.v[EditOpt.o_scroll] = scroll
        self.v[EditOpt.o_shell] = getenv('SHELL')
        self.v[EditOpt.o_shiftwidth] = 8
        self.v[EditOpt.o_tabstop] = 8
        self.v[EditOpt.o_term] = getenv('TERM')
        self.v[EditOpt.o_warn] = True
        self.v[EditOpt.o_window] = window
        self.v[EditOpt.o_wrapscan] = True

    def __getitem__(self, item):
        assert isinstance(item, EditOpt)
        return self.v[item]

    def __setitem__(self, item, value):
        assert isinstance(item, EditOpt)
        if item in BOOL:
            assert isinstance(value, bool)
        elif item in TYPES.keys():
            assert isinstance(value, TYPES[item])
        else:
            raise ValueError
        self.v[item] = value

    def __delitem__(self, item):
        del self.v[item]

    def __iter__(self):
        return iter(self.v.items())

    def __len__(self):
        return len(self.v)
