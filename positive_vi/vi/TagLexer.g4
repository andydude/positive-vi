/* -*- mode: antlr; -*-
 * SPDX-FileCopyrightText: © 2024 Andrew Robbins
 * SPDX-License-Identifier: Apache-2.0
 */
lexer parser CommandLexer;

Esc : '\\' ;

ControlD : '\u0004' ;

ControlJ : '\n' ;

ControlV : '\u0016' ;

ControlW : '\u0017' ;

Addr1 : '.' | '$' ;
Addr2 : Addr1 ',' Addr1 ;

Count : [1-9][0-9]* ;

Flags : '+' | '-' | '#' | 'p' | 'l' ;

buffer : Name ;
file : Name ;

AppendSym : 'a' ('ppend')? ;
ArgsSym : 'ar' ('gs')? ;
ChangeSym : 'c' ('change')? ;
ChangeDirSym : 'chd' ('ir')? ;
ChangeDirSym : 'co' ('py')? | 't' ;


