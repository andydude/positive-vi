from enum import Enum

class Mode(Enum):
    CMD = 1
    INP = 2

class CommandMode(Enum):
    CMD_EXTEND 		= 10
    CMD_VISUAL 		= 11
    CMD_LINE 		= 12
    CMD_PENDING		= 13
    CMD_MORE		= 14

class InputMode(Enum):
    INP_INSERT 		= 21
    INP_REPLACE 	= 22
