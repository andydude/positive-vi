import io
import os
import sys
import pprint
from antlr4 import CommonTokenStream
from antlr4 import InputStream
from argparse import ArgumentParser
from CommandLexer import CommandLexer
from CommandParser import CommandParser
from CommandVisitor import CommandVisitor


DEBUG = True

def reads(cmd: str, start='start'):
    lexer = CommandLexer(InputStream(cmd))
    parser = CommandParser(CommonTokenStream(lexer))
    visitor = CommandVisitor()
    try:
        tree = getattr(parser, start)()
        if DEBUG:
            lisp_tree_str = tree.toStringTree(recog=parser)

            print(lisp_tree_str)
        return tree.accept(visitor)
    except Exception as exc:
        print(repr(exc))
        raise exc
        return None

    
def read(reader, start='start'):
    # TODO remove eagerness
    return reads(reader.read(), start=start)


def handler_with(reader, writer,
                 command: str = "",
                 filename: str = "",
                 stdin: bool = False,
                 rule: str = 'start'):
    # if stdin:
    #     input_stream = InputStream(sys.stdin.read())
    # elif command:
    #     input_stream = io.StringIO(command)
    # elif filename:
    #     input_stream = FileStream(filename, "utf-8")
    # else:
    #     raise ValueError
    if stdin:
        input_stream = sys.stdin
    elif command:
        input_stream = io.StringIO(command)
    elif filename:
        input_stream = open(filename, encoding="utf-8")
    else:
        raise ValueError

    # main logic
    content = reader(input_stream, start=rule)
    if DEBUG:
        #from pprint import pprint
        print(content)
    #writer(content, sys.stdout)

def add_arguments(parser):
    parser.add_argument("filename", default="", nargs='?')
    parser.add_argument("-c", "--command", default="")
    parser.add_argument("-s", "--stdin", action="store_true", default=False)
    parser.add_argument("-r", "--rule", action="store", default='start')
    return parser


def main_with(reader, writer):
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args())
    handler_with(reader, writer, **options)

if __name__ == '__main__':
    main_with(read, None)
