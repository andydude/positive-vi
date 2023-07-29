from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
import struct

PROGRAM = 'od'
DEFAULT_BASE = 'o'
DEFAULT_TYPE = 'oS'

CHAR_NAMES_C0 = [
    'nul',
    'soh',
    'stx',
    'etx',
    'eot',
    'enq',
    'ack',
    'bel',
    'bs',
    'ht',
    'nl',
    'vt',
    'ff',
    'cr',
    'so',
    'si',
    'dle',
    'dc1',
    'dc2',
    'dc3',
    'dc4',
    'nak',
    'syn',
    'etb',
    'can',
    'em',
    'sub',
    'esc',
    'fs',
    'gs',
    'rs',
    'us',
    'sp',
]
CHAR_NAME_127 = 'del'
CHAR_NAMES_C1 = [
    'del',  # 0x7F
    'pad',  # 0x80
    'hop',
    'bph',
    'nbh',
    'ind',
    'nel',
    'ssa',
    'esa',
    'hts',
    'htj',
    'lts',
    'pld',
    'plu',
    'ri',
    'ss2',
    'ss3',
    'dcs',
    'pu1',
    'pu2',
    'sts',
    'cch',
    'mw',
    'spa',
    'epa',
    'sos',
    'sgc',
    'sci',
    'csi',
    'st',
    'osc',
    'pm',
    'asc',
    'nbs',
]
CHAR_NAME_173 = 'shy'

class Formatter:
    def __init__(self,
                 file,
                 count=0,
                 skip=0,
                 base=DEFAULT_BASE,
                 type=[],
                 verbose=False,
                 reverse=False):
        self.file = file
        self.reverse = reverse
        self.verbose = verbose
        self.count = count
        self.skip = skip
        self.plain = False
        if isinstance(base, str):
            base = parse_base(base)
            if base == 'p':
                self.plain = True
                base = 16
        self.base = base
        if isinstance(type, list):
            # First, type is a list because
            # of action=append, and so we get the first
            if len(type) > 0:
                type = type[0]
            else:
                type = DEFAULT_TYPE
        if isinstance(type, str):
            # Second, type is a str because
            # we haven't parsed it yet
            type = parse_type(type)
        if isinstance(type, list):
            # Third, type is a list because
            # we parsed it into distinct types.
            # We will only use the first one.
            if len(type) > 1:
                raise NotImplementedError("use only one type specifier")
            type = type[0]

        self.type_fmt  = type.fmt
        self.type_char = type.char
        self.type_base = type.base
        self.type_size = type.size

        if self.file == []:
            self.file = ['-']
        for fn in self.file:
            if fn == '-':
                fn = '/dev/stdin'
            if self.reverse:
                with open(fn, 'r') as reader:
                    with open('/dev/stdout', 'wb') as writer:
                        self.decode(reader, writer)
            else:
                with open(fn, 'rb') as reader:
                    self.encode(reader)

    def decode(self, reader, writer):
        self.nbytes = 16

        while True:
            line = reader.readline()
            line = line.strip('\n')
            if line is None:
                break
            if line == '':
                break
            if self.plain:
                raise NotImplementedError
            else:
                groups = line.split(' ')
                # print(repr(groups))
                skip = self.skip
                body = groups
                if self.base != -1:
                    skip = self.decode_head(groups[0])
                    body = groups[1:]
                bytes_ = self.decode_body(body)
                writer.write(bytes_)

    def decode_head(self, skip):
        if self.base == 8:
            return int(skip, 8)
        elif self.base == 10:
            return int(skip, 10)
        elif self.base == 16:
            return int(skip, 16)
        elif self.base == -1:
            return -1
        else:
            raise ValueError("unknown addr base")

    def decode_body(self, strings_):
        body = [
            self.decode_byte_from_body(string_)
            for string_ in strings_
        ]
        return b''.join(body)

    def decode_byte_from_body(self, string_):
        if self.type_size == 1:
            raise ValueError
        elif self.type_size == 2:
            return self.decode_byte_2(string_)
        elif self.type_size == 4:
            return self.decode_byte_4(string_)
        elif self.type_size == 8:
            return self.decode_byte_8(string_)
        else:
            raise ValueError


    def decode_byte_2(self, string_):
        num = -1
        if self.type_char == TypeChar.Base8:
            num = int(string_, 8)
        elif self.type_char == TypeChar.Base10S:
            num = int(string_, 10)
            return struct.pack("<h", num)
        elif self.type_char == TypeChar.Base10U:
            num = int(string_, 10)
        elif self.type_char == TypeChar.Base16:
            num = int(string_, 16)
        elif self.type_char == TypeChar.Floating:
            num = float(string_)
            return struct.pack("<e", num)
        else:
            raise ValueError(self.type_char)
        return struct.pack("<H", num)

    def decode_byte_4(self, string_):
        num = -1
        if self.type_char == TypeChar.Base8:
            num = int(string_, 8)
        elif self.type_char == TypeChar.Base10S:
            num = int(string_, 10)
            return struct.pack("<i", num)
        elif self.type_char == TypeChar.Base10U:
            num = int(string_, 10)
        elif self.type_char == TypeChar.Base16:
            num = int(string_, 16)
        elif self.type_char == TypeChar.Floating:
            num = float(string_)
            return struct.pack("<f", num)
        else:
            raise ValueError(self.type_char)
        return struct.pack("<I", num)

    def decode_byte_8(self, string_):
        num = -1
        if self.type_char == TypeChar.Base8:
            num = int(string_, 8)
        elif self.type_char == TypeChar.Base10S:
            num = int(string_, 10)
            return struct.pack("<q", num)
        elif self.type_char == TypeChar.Base10U:
            num = int(string_, 10)
        elif self.type_char == TypeChar.Base16:
            num = int(string_, 16)
        elif self.type_char == TypeChar.Floating:
            num = float(string_)
            return struct.pack("<d", num)
        else:
            raise ValueError(self.type_char)
        return struct.pack("<Q", num)

    def encode(self, reader):
        self.nbytes = 16

        while True:
            body = reader.read(self.nbytes)
            assert isinstance(body, bytes)
            if len(body) == 0:
                break

            print("{}{}{}".format(
                self.encode_head(),
                '' if self.plain else ' ',
                self.encode_body(body)))

            self.skip += len(body)

    def encode_head(self):
        if self.base == 8:
            return "{:06o}".format(self.skip)
        elif self.base == 10:
            return "{:06d}".format(self.skip)
        elif self.base == 16:
            return "{:06x}".format(self.skip)
        elif self.base == -1:
            return ""
        else:
            raise ValueError("unknown addr base")

    def encode_body(self, body):
        sep = '' if self.plain else ' '
        return sep.join(self.encode_byte_from_body(body))

    def encode_char_name(self, char):
        if char <= 32:
            return '{: >3}'.format(CHAR_NAMES_C0[char])
        elif 32 < char and char < 127:
            return '{: >3}'.format(chr(char))
        elif 0x7F <= char and char <= 0xA0:
            try:
                return '{: >3}'.format(CHAR_NAMES_C1[char - 0x7F])
            except:
                return '?'
        elif char == 0xAD:
            return '{: >3}'.format(CHAR_NAME_173)
        else:
            return '{: >3}'.format(chr(char))
        # else:
        #     return "{:03o}".format(char)
        #     # return '{: >3}'.format(chr(char))

    def encode_byte_from_body(self, body):
        if self.type_size == 1:
            xs = [
                self.encode_byte_1(byte)
                for byte in list(body)
            ]
            if self.type_char == TypeChar.NamedChar:
                if len(xs[0]) == 4:
                    xs[1] = xs[1][1:]
            return xs
        elif self.type_size == 2:
            return [
                self.encode_byte_2(byte)
                for byte in chunks(body, 2)
            ]
        elif self.type_size == 4:
            return [
                self.encode_byte_4(byte)
                for byte in chunks(body, 4)
            ]
        elif self.type_size == 8:
            return [
                self.encode_byte_8(byte)
                for byte in chunks(body, 8)
            ]
        else:
            raise ValueError

    def encode_byte_1(self, byte):
        if self.type_char == TypeChar.Base8:
            return "{:03o}".format(byte)
        elif self.type_char == TypeChar.Base10S:
            return "{:03d}".format(byte)
        elif self.type_char == TypeChar.Base10U:
            return "{:03d}".format(byte)
        elif self.type_char == TypeChar.Base16:
            return "{:02x}".format(byte)
        elif self.type_char == TypeChar.RawChar:
            return "{:02x}".format(byte)
        elif self.type_char == TypeChar.NamedChar:
            return self.encode_char_name(byte)
        else:
            raise ValueError(self.type_char)

    def encode_byte_2(self, bytes_):
        byte = struct.unpack("<H", bytes_)[0]
        if self.type_char == TypeChar.Base8:
            return "{:06o}".format(byte)
        elif self.type_char == TypeChar.Base10S:
            byte = struct.unpack("<h", bytes_)[0]
            return "{:06d}".format(byte)
        elif self.type_char == TypeChar.Base10U:
            return "{:06u}".format(byte)
        elif self.type_char == TypeChar.Base16:
            return "{:04x}".format(byte)
        elif self.type_char == TypeChar.Floating:
            byte = struct.unpack("<e", bytes_)[0]
            return "{:06f}".format(byte)
        else:
            raise ValueError(self.type_char)

    def encode_byte_4(self, bytes_):
        byte = struct.unpack("<I", bytes_)[0]
        if self.type_char == TypeChar.Base8:
            return "{:012o}".format(byte)
        elif self.type_char == TypeChar.Base10S:
            byte = struct.unpack("<i", bytes_)[0]
            return "{:012d}".format(byte)
        elif self.type_char == TypeChar.Base10U:
            return "{:012d}".format(byte)
        elif self.type_char == TypeChar.Base16:
            return "{:08x}".format(byte)
        elif self.type_char == TypeChar.Floating:
            byte = struct.unpack("<f", bytes_)[0]
            return "{:f}".format(byte)
        else:
            raise ValueError(self.type_char)

    def encode_byte_8(self, bytes_):
        byte = struct.unpack("<Q", bytes_)[0]
        if self.type_char == TypeChar.Base8:
            return "{:016o}".format(byte)
        elif self.type_char == TypeChar.Base10S:
            byte = struct.unpack("<q", bytes_)[0]
            return "{: 16d}".format(byte)
        elif self.type_char == TypeChar.Base10U:
            return "{: 16d}".format(byte)
        elif self.type_char == TypeChar.Base16:
            return "{:016x}".format(byte)
        elif self.type_char == TypeChar.Floating:
            byte = struct.unpack("<d", bytes_)[0]
            return "{:f}".format(byte)
        else:
            raise ValueError(self.type_char)


class TypeFormat(Enum):
    Integerish 		= 1  # [d, o, u, x]
    Floatish 		= 2  # [f]
    Character 		= 3  # [a, c]


class TypeChar(Enum):
    """
    grammar;

    start = Typecode+ ;

    TypeCode
    	= CharTypeCode
        | IntTypeCode
          IntSizeCode
        | FloatTypeCode
          FloatSizeCode
        ;

    CharTypeCode = [ac] ;
    IntTypeCode = [doux] ;
    FloatTypeCode = [f] ;
    IntSizeCode = [CSILQ] | Integer;
    FloatSizeCode = [eFDLQ] | Integer;
    Integer = [0-9]+ ;
    """
    NamedChar 	= 'a'
    RawChar 	= 'c'
    Base10S 	= 'd'
    Floating 	= 'f'
    Base8 		= 'o'
    Base10U 	= 'u'
    Base16 		= 'x'



@dataclass
class TypeGroup:
    fmt: TypeFormat
    char: TypeChar
    base: int
    size: int


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parse_base(s):
    if s == 'o':
        return 8
    elif s == 'd':
        return 10
    elif s == 'u':
        return 10
    elif s == 'x':
        return 16
    elif s == 'n':
        return -1
    elif s == 'p':
        # Non-standard extension (from xxd)
        return -1
    else:
        raise ValueError

def parse_count(s):
    return int(s, 10)

def parse_skip(s):
    return int(s, 10)

def parse_type_prefix(s, ssize):
    if ssize is None:
        ssize = 1
    if len(s) > 1:
        stype = s[0]
        srest = s[1:]
    else:
        stype = s
        srest = ''
    sffix = parse_type_suffix(srest, stype)
    if stype in ['a', 'c']:
        if stype == 'a':
            tych = TypeChar.NamedChar
        elif stype == 'c':
            tych = TypeChar.RawChar
        return TypeGroup(
            fmt=TypeFormat.Character,
            char=tych,
            base=0,
            size=ssize)
    elif stype in ['d', 'o', 'u', 'x']:
        if stype in ['d', 'u']:
            base = 10
            if stype == 'd':
                tych = TypeChar.Base10S
            elif stype == 'u':
                tych = TypeChar.Base10U
        elif stype == 'o':
            base = 8
            tych = TypeChar.Base8
        elif stype == 'x':
            base = 16
            tych = TypeChar.Base16
        return TypeGroup(
            fmt=TypeFormat.Integerish,
            char=tych,
            base=base,
            size=(sffix * ssize))
    elif stype == 'f':
        return TypeGroup(
            fmt=TypeFormat.Floatish,
            char=TypeChar.Floating,
            base=10,
            size=(sffix * ssize))
    else:
        raise ValueError("unknown prefix in type string {:s}".format(s))

def parse_type_suffix(s, prefix):
    """
    The only job of this function is to return
    a size in bytes associated with the type.
    """
    if s == '':
        return 1
    elif s == 'e':
        return 2
    elif s == 'F':
        return 4
    elif s == 'D':
        return 8
    elif s == 'Q':  # Non-standard extension (from util-linux/od)
        return 16
    elif s == 'C':
        return 1
    elif s == 'S':
        return 2
    elif s == 'I':
        return 4
    elif s == 'L':
        if prefix == 'f':
            # floating (long double) type
            return 10
        else:
            # integer (long int) type
            return 8
    else:
        raise ValueError("unknown suffix in type string {:s}".format(s))

def parse_type_integer(s):
    return int(s, 10) if len(s) else None

def parse_type(s):
    """
    The string shall consist of the type specification characters
    a, c, d, f, o, u, and x, specifying named character, character,
    signed decimal, floating point, octal, unsigned decimal, and
    hexadecimal, respectively.

    The type specification characters d, f, o, u, and x can be
    followed by an optional unsigned decimal integer that specifies
    the number of bytes to be transformed by each instance of
    the output type.

    The type specification character f can be followed by an optional
    F, D, or L indicating that the conversion should be applied to an
    item of type float, double, or long double, respectively.

    The type specification characters d, o, u, and x can be followed
    by an optional C, S, I, or L indicating that the conversion should be
    applied to an item of type char, short, int, or long, respectively.

    Multiple types can be concatenated within the same type and
    multiple -t options can be specified. Output lines shall be written
    for each type specified in the order in which the type specification
    characters are specified.
    """
    accum = []
    pair = ([], [])
    for c in list(s):
        if c.isdigit():
            pair[1].append(c)
        else:
            if len(pair[1]):
                group = \
                    parse_type_prefix(str(''.join(pair[0])),
                    parse_type_integer(str(''.join(pair[1]))))
                accum.append(group)
                pair = ([], [])
            pair[0].append(c)
    group = \
        parse_type_prefix(str(''.join(pair[0])),
        parse_type_integer(str(''.join(pair[1]))))
    accum.append(group)
    return accum

def add_arguments(parser):
    parser.add_argument('-A',
                        action='store',
                        default=DEFAULT_BASE,
                        dest='base',
                        help="Specify the input offset base (default o=8, d=10, x=16).")
    parser.add_argument('-j',
                        action='store',
                        default=0,
                        dest='skip',
                        type=parse_skip,
                        help="Jump over skip bytes from the beginning of the input.")
    parser.add_argument('-N',
                        action='store',
                        default=-1,
                        dest='count',
                        type=parse_count,
                        help="Format no more than count bytes of input.")
    parser.add_argument('-t',
                        action='append',
                        default=[],
                        dest='type',
                        help="Specify one or more output types. " +
                        "- (a c)         - Character types, " +
                        "- (f#)          - Floating types, " +
                        "- (d# o# u# x#) - Integer types. " +
                        "The number indicates the how many bytes to represent.")
    parser.add_argument('-v',
                        action='store_true',
                        default=False,
                        dest='verbose',
                        help="Write all input data.")
    # Non-standard extension (from xxd)
    parser.add_argument('-r',
                        action='store_true',
                        default=False,
                        dest='reverse',
                        help="Reverse from formatted bytes to binary. (Non-standard)")
    parser.add_argument('file',
                        action='store',
                        nargs='*')
    return parser


def od_main():
    parser = add_arguments(ArgumentParser(PROGRAM))
    arguments = parser.parse_args()
    options = vars(arguments)
    # print(repr(options))
    Formatter(**options)


if __name__ == '__main__':
    od_main()
