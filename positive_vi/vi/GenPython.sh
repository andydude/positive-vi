#!/bin/sh
antlr4 -Dlanguage=Python3 CommandParser.g4 CommandLexer.g4 -visitor -no-listener
