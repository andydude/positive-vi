# positive-vi
Implementation of vi in Python

The goal is to implement `vi` according to POSIX, no more, no less. Well actually, we do implement `more` and `ex` because of their similarity to `vi`, but again, the goal is to implement exactly what is in POSIX, which means:

- **no visual mode** the specification does not distinguish between open, normal, and visual modes, so these must be a single mode that corresponds to *Normal Mode* in Vim.
- **no insert mode** the specification refers to **input mode**, and so that is the mode we implement, which corresponds to *Insert Mode* in Vim.

There is only one exception, currently, to the rule that all features must be specified by POSIX:

- **od** is allowed to have an extra non-standard command-line option `-r` for reversing the dump from hex to binary. The default is still octal, but it is possible to specify hex and decimal just as POSIX specifies.

## Modes

With the above rules in mind, here are the modes that we implement in Positive `vi`:

- **Command** (Vim calls this Normal)
- **Command/Line** (Vim calls this Cmd-Line)
- **Command/Pending** (Vim calls this Cmd-Pending)
- **Input** (Vim calls this Insert)
- **Input/Replace** (Vim calls this Replace)

## Commands

All commands are prefixed with `p`.

- `pod` - Positive Octal Dump. Add `-Ax -tx1` for hex.
- `pmore` - Positive More Pager
- `pex` - Positive **Ex**tended Editor
- `pvi` - Positive **Vi**sual Editor

## Install

Download this repo, change directory, and
`python3 ./setup.py install`, or
`pip3 install -e git+https://github.com/andydude/positive-vi.git#egg=positive_vi`

## Usage

`pvi MyFile.txt`
