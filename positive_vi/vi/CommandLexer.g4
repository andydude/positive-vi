/* -*- mode: antlr; -*-
 * SPDX-FileCopyrightText: © 2024 Andrew Robbins
 * SPDX-License-Identifier: Apache-2.0
 */
lexer grammar CommandLexer;

Count : [1-9][0-9]* ;

ControlA : '\u0001' ;
ControlB : '\u0002' ;
ControlC : '\u0003' ;
ControlD : '\u0004' ;
ControlE : '\u0005' ;
ControlF : '\u0006' ;
ControlG : '\u0007' ;
ControlH : '\u0008' ;
ControlI : '\u0009' ;
ControlJ : '\n' ;
ControlK : '\u000B' ;
ControlL : '\u000C' ;
ControlM : '\r' ;
ControlN : '\u000E' ;
ControlO : '\u000F' ;
ControlP : '\u0010' ;
ControlQ : '\u0011' ;
ControlR : '\u0012' ;
ControlS : '\u0013' ;
ControlT : '\u0014' ;
ControlU : '\u0015' ;
ControlV : '\u0016' ;
ControlW : '\u0017' ;
ControlX : '\u0018' ;
ControlY : '\u0019' ;
ControlZ : '\u001A' ;
ControlLBrack : '\u001B' ;
ControlBSlash : '\u001C' ;
ControlRBrack : '\u001D' ;
ControlPow : '\u001E' ;
ControlLow : '\u001F' ;

UpperA : 'A' ;
UpperB : 'B' ;
UpperC : 'C' ;
UpperD : 'D' ;
UpperE : 'E' ;
UpperF : 'F' ;
UpperG : 'G' ;
UpperH : 'H' ;
UpperI : 'I' ;
UpperJ : 'J' ;
UpperK : 'K' ;
UpperL : 'L' ;
UpperM : 'M' ;
UpperN : 'N' ;
UpperO : 'O' ;
UpperP : 'P' ;
UpperQ : 'Q' ;
UpperR : 'R' ;
UpperS : 'S' ;
UpperT : 'T' ;
UpperU : 'U' ;
UpperV : 'V' ;
UpperW : 'W' ;
UpperX : 'X' ;
UpperY : 'Y' ;
UpperZ : 'Z' ;

LowerA : 'a' ;
LowerB : 'b' ;
LowerC : 'c' ;
LowerD : 'd' ;
LowerE : 'e' ;
LowerF : 'f' ;
LowerG : 'g' ;
LowerH : 'h' ;
LowerI : 'i' ;
LowerJ : 'j' ;
LowerK : 'k' ;
LowerL : 'l' ;
LowerM : 'm' ;
LowerN : 'n' ;
LowerO : 'o' ;
LowerP : 'p' ;
LowerQ : 'q' ;
LowerR : 'r' ;
LowerS : 's' ;
LowerT : 't' ;
LowerU : 'u' ;
LowerV : 'v' ;
LowerW : 'w' ;
LowerX : 'x' ;
LowerY : 'y' ;
LowerZ : 'z' ;


BSlash 		: '\\' ;
Slash		: '/' ;
Zero		: '0' ;
Semi		: ';' ;
Dot			: '.' ;
Tilde		: '~' ;
Equal		: '=' ;
Vert		: '|' ;
Low			: '_' ;
Pow			: '^' ;
Plus		: '+' ;
Minus		: '-' ;
LShift		: '<' ('<')? ;
RShift		: '>' ('>')? ;
Dollar		: '$' ;
Percent		: '%' ;
DLBrack		: '[[' ;
DRBrack		: ']]' ;
Amp			: '&' ;
Apos		: ['] ;
Grave		: '`' ;
Comma		: ',' ;
Excl		: '!' ;
Colon		: ':' -> pushMode(CMD_LINE);
Quest		: '?' ;
Space		: ' ' ;
LParen		: '(' ;
RParen		: ')' ;
LBrace		: '{' ;
RBrace		: '}' ;


// BEGIN MODE CMD_LINE
mode CMD_LINE;

Adr1 
	: '.' 
	| '$' 
	| CountCmd
	;

Adr2 
	: Adr1 ',' Adr1 
    | '%'
	;

PlusSym		: '+' ;
CountCmd : [1-9][0-9]* ;
Flags
    : '+' | '-' | '#' | 'p' | 'l' ;
UnnamedBuffer : 'UNNAMED' ;
SimpleFilename : [A-Za-z_.\-] ;
StringFilename : ["] ["] ;
ShellCommand : 'echo' ;
VisType : 'visType' ;
SubOptions : 'subOpt' ;
WindowTypes : 'winType' ;

SlashSym
    : '/' ;
ExclSym
	: '!' ;
QuestSym
    : '?' ;
AbbreviateSym
    : 'ab' ('rev' ('iate')?)? ;
AppendSym
    : 'a' ('ppend')? ;
ArgsSym
    : 'ar' ('gs')? ;
ChangeSym
    : 'change' | 'c' ;
ChangeDirSym
    : 'chd' ('ir')? ;
CopySym
    : 'co' ('py')? | 't' ;
DeleteSym
	: 'd' ('elete')? ;
EditSym
	: 'e' ('dit')? ;
FileSym
	: 'f' ('ile')? ;
InsertSym
	: 'i' ('nsert')? ;
JoinSym
	: 'j' ('oin')? ;
ListSym
	: 'l' ('ist')? ;
MapSym
	: 'map' ;
MarkSym
	: 'ma' ('rk')? | 'k' ;
MoveSym
	: 'm' ('ove')? ;
NextSym
	: 'n' ('ext')? ;
NumberSym
	: 'nu' ('mber')? | '#' ;
OpenSym
	: 'o' ('pen')? ;
PreserveSym
	: 'pre' ('serve')? ;
PrintSym
	: 'p' ('rint')? ;
PutSym
	: 'pu' ('t')? ;
PrevSym
	: 'prev' ('ious')? ;
QuitSym
	: 'q' ('uit')? ;
ReadSym
	: 'r' ('ead')? ;
RecoverSym
	: 'rec' ('over')? ;
RewindSym
	: 'rew' ('ind')? ;
SetSym
	: 'se' ('t')? -> pushMode(EDIT_OPT);
ShellSym
	: 'sh' ('ell')? ;
SourceSym
	: 'so' ('urce')? ;
SubstituteSym
	: 's' ('ubstitute')? ;
SubAndSym
	: '&' ;
SubTildeSym
	: '˜' ;
SuspendSym
	: 'su' ('spend')?
    | 'st' ('op')?
    ;
TagSym
	: 'ta' ('g')? ;
UnabbreviateSym
	: 'una' ('bbrev' ('iate')?)? ;
UndoSym
	: 'u' ('ndo')? ;
UnmapSym
	: 'unm' ('ap')? ;
VersionSym
	: 've' ('rsion')? ;
VisualSym
	: 'vi' ('sual')? ;
WriteSym
	: 'w' ('rite')? ;
WriteQuitSym
    : 'wq' ;
WriteExitSym
    : 'x' ('it')? ;
GlobalSym
	: 'g' ('lobal')? | 'v' ;
YankSym
	: 'ya' ('nk')? ;
WindowSym
	: 'z' ;
LShiftSym
	: '<' ('<')? ;
RShiftSym
	: '>' ('>')? ;
EqualSym
	: '=' ;
AtExecuteSym
	: '@' ;
AtTimesSym
    : '*' ;

ColonEnd : '\n' -> popMode;

// END MODE CMD_LINE
// BEGIN MODE EDIT_OPT
mode EDIT_OPT;

QuestOpt : '?' ;
EqualOpt : '=' ;
CountOpt : [1-9][0-9]* ;
SetNoSym : 'no' ;
SetAllSym : 'all' ;
LHS : 'LHS' ;
RHS : 'RHS' ;
fragment AutoIndentOpt
    : 'autoindent' | 'ai' ;
fragment AutoPrintOpt
    : 'autoprint' | 'ap' ;
fragment AutoWriteOpt
    : 'autowrite' | 'aw' ;
fragment DirectoryOpt
    : 'directory' | 'dir' ;
fragment EdCompatibleOpt
    : 'edcompatible' | 'ed' ;
fragment ErrorBellsOpt
    : 'errorbells' | 'eb' ;
fragment ExRcOpt
    : 'exrc' ;
fragment IgnoreCaseOpt
    : 'ignorecase' | 'ic' ;
fragment ListOpt
    : 'list' ;
fragment MagicOpt
    : 'magic' ;
fragment MesgOpt
    : 'mesg' ;
fragment NumberOpt
    : 'number' | 'nu' ;
fragment ParaOpt
    : 'paragraphs' | 'para' ;
fragment PromptOpt
    : 'prompt' ;
fragment ReadOnlyOpt
    : 'readonly' ;
fragment RedrawOpt
    : 'redraw' ;
fragment RemapOpt
    : 'remap' ;
fragment ReportOpt
    : 'report' ;
fragment ScrollOpt
    : 'scroll' | 'scr' ;
fragment SectionsOpt
    : 'sections' ;
fragment ShellOpt
    : 'shell' ;
fragment ShiftWidthOpt
    : 'shiftwidth' | 'sw' ;
fragment SlowMatchOpt
    : 'slowmatch' | 'sm' ;
fragment ShowModeOpt
    : 'showmode' ;
fragment SlowOpenOpt
    : 'slowopen' ;
fragment TabStopOpt
    : 'tabstop' | 'ts' ;
fragment TagLengthOpt
    : 'taglength' | 'tl' ;
fragment TagsOpt
    : 'tags' ;
fragment TermOpt
    : 'term' ;
fragment TerseOpt
    : 'terse' ;
fragment WarnOpt
    : 'warn' ;
fragment WindowOpt
    : 'window' ;
fragment WrapMarginOpt
    : 'wrapmargin' | 'wm' ;
fragment WrapScanOpt
    : 'wrapscan' | 'ws' ;
fragment WriteAnyOpt
    : 'writeany' | 'wa' ;

ExOption
    : AutoIndentOpt
    | AutoPrintOpt
    | AutoWriteOpt
    | DirectoryOpt
    | EdCompatibleOpt
    | ErrorBellsOpt
    | ExRcOpt
    | IgnoreCaseOpt
    | ListOpt
    | MagicOpt
    | MesgOpt
    | NumberOpt
    | ParaOpt
    | PromptOpt
    | ReadOnlyOpt
    | RedrawOpt
    | RemapOpt
    | ReportOpt
    | ScrollOpt
    | SectionsOpt
    | ShellOpt
    | ShiftWidthOpt
    | SlowMatchOpt
    | ShowModeOpt
    | SlowOpenOpt
    | TabStopOpt
    | TagLengthOpt
    | TagsOpt
    | TermOpt
    | TerseOpt
    | WarnOpt
    | WindowOpt
    | WrapMarginOpt
    | WrapScanOpt
    | WriteAnyOpt
    ;

WsOpt : ' ' -> skip;
ColonOptEnd : '\n' -> popMode;
SetOptEnd : EOF -> popMode;
// END MODE EDIT_OPT
