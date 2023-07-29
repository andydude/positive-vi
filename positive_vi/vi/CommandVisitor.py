# Generated from CommandParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .CommandParser import CommandParser
    from .CommandParserVisitor import CommandParserVisitor
else:
    from CommandParser import CommandParser
    from CommandParserVisitor import CommandParserVisitor

# This class defines a complete generic visitor for a parse tree produced by CommandParser.

class CommandVisitor(CommandParserVisitor):

    # Visit a parse tree produced by CommandParser#adr1.
    def visitAdr1(self, ctx:CommandParser.Adr1Context):
        if ctx.getText() == '.':
            return ['addr', 'cur']
        elif ctx.getText() == '$':
            return ['addr', 'end']
        elif ctx.Count():
            count = int(self.Count().symbol.text)
            return ['addr', 'num', count]
        else:
            raise ValueError


    # Visit a parse tree produced by CommandParser#adr2.
    def visitAdr2(self, ctx:CommandParser.Adr2Context):
        if ctx.getText() == '%':
            return ['addr-range',
                    ['addr', 'num', 1],
                    ['addr', 'end']]
        elif ctx.Adr():
            addrs = list(map(
                self.visitAdr1,
                ctx.adr1()))
            return ['addr-range'] + addrs
        else:
            raise ValueError


    # Visit a parse tree produced by CommandParser#count.
    def visitCount(self, ctx:CommandParser.CountContext):
        print("A", repr(ctx))
        if ctx is None:
            return [None]
        elif ctx.CountCmd():
            return [int(ctx.Count().symbol.text)]
        else:
            print(repr(ctx.toStringTree()))

    # Visit a parse tree produced by CommandParser#count.
    def visitCountCmd(self, ctx:CommandParser.CountCmdContext):
        print("C", repr(ctx))
        if ctx is None:
            return [None]
        elif ctx.CountCmd():
            return [int(ctx.CountCmd().symbol.text)]
        else:
            print(repr(ctx.toStringTree()))


    # Visit a parse tree produced by CommandParser#buffer.
    def visitBuffer(self, ctx:CommandParser.BufferContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#filename.
    def visitFilename(self, ctx:CommandParser.FilenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#directory.
    def visitDirectory(self, ctx:CommandParser.DirectoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#shellCommand.
    def visitShellCommand(self, ctx:CommandParser.ShellCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#visType.
    def visitVisType(self, ctx:CommandParser.VisTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#subOptions.
    def visitSubOptions(self, ctx:CommandParser.SubOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#windowTypes.
    def visitWindowTypes(self, ctx:CommandParser.WindowTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#character.
    def visitCharacter(self, ctx:CommandParser.CharacterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#letter.
    def visitLetter(self, ctx:CommandParser.LetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#tagString.
    def visitTagString(self, ctx:CommandParser.TagStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#setValue.
    def visitValue(self, ctx:CommandParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#pattern.
    def visitPattern(self, ctx:CommandParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#replacement.
    def visitReplacement(self, ctx:CommandParser.ReplacementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#newline.
    def visitNewline(self, ctx:CommandParser.NewlineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#flags.
    def visitFlags(self, ctx:CommandParser.FlagsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#lhs.
    def visitLhs(self, ctx:CommandParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#rhs.
    def visitRhs(self, ctx:CommandParser.RhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#rePattern.
    def visitRePattern(self, ctx:CommandParser.RePatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#rePattRepl.
    def visitRePattRepl(self, ctx:CommandParser.RePattReplContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#setOptions.
    def visitSetOptions(self, ctx:CommandParser.SetOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#setOption.
    def visitSetOption(self, ctx:CommandParser.SetOptionContext):
        return self.visitChildren(ctx)

    
    # Visit a parse tree produced by CommandParser#exCommand.
    def visitExCommand(self, ctx:CommandParser.ExCommandContext):
        if ctx.AbbreviateSym():
            lhs = self.visitLhs(vtx.lhs())
            rhs = self.visitRhs(vtx.rhs())
            return ["abbreviate", lhs, rhs]
        elif ctx.AppendSym():
            adr1 = self.visitAdr1(ctx.adr1())
            excl = True if ctx.ExclSym() else False
            return ["append", adr1, excl]
        elif ctx.ArgsSym():
            return ["args"]
        elif ctx.ChangeSym():
            adr2 = list(map(self.visitAdr2, ctx.adr2()))
            excl = True if ctx.ExclSym() else False
            count = self.visitCountCmd(ctx.countCmd())
            return ["change", adr2, excl, count]
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#viMotion.
    def visitViMotion(self, ctx:CommandParser.ViMotionContext):
        if ctx.ControlH():
            return ["move_cursor_backward"] + self.visitCount(ctx.count())
        elif ctx.LowerH():
            return ["move_cursor_backward"] + self.visitCount(ctx.count())
        elif ctx.ControlJ():
            return ["move_cursor_down"] + self.visitCount(ctx.count())
        elif ctx.ControlM():
            return ["move_cursor_down"] + self.visitCount(ctx.count())
        elif ctx.ControlN():
            return ["move_cursor_down"] + self.visitCount(ctx.count())
        elif ctx.LowerJ():
            return ["move_cursor_down"] + self.visitCount(ctx.count())
        else:
            raise ValueError


    # Visit a parse tree produced by CommandParser#viCommand.
    def visitViCommand(self, ctx:CommandParser.ViCommandContext):
        if ctx.ControlU():
            return ["scroll_half_backward"] + self.visitCount(ctx.count())
        elif ctx.ControlD():
            return ["scroll_half_forward"] + self.visitCount(ctx.count())
        elif ctx.ControlY():
            return ["scroll_line_backward"] + self.visitCount(ctx.count())
        elif ctx.ControlE():
            return ["scroll_line_forward"] + self.visitCount(ctx.count())
        elif ctx.ControlB():
            return ["scroll_page_backward"] + self.visitCount(ctx.count())
        elif ctx.ControlF():
            return ["scroll_page_forward"] + self.visitCount(ctx.count())
        elif ctx.ControlG():
            return ["display_info"]
        elif ctx.ControlL():
            return ["clear_and_redraw"]
        elif ctx.ControlR():
            return ["redraw"]
        elif ctx.ControlLBrack():
            return ["end_command_mode"]
        elif ctx.ControlRBrack():
            return ["search_for_tag"]
        elif ctx.Excl():
            return ["replace_shell"] + self.visitCount(ctx.count())
        elif ctx.Dot():
            return ["repeat"] + self.visitCount(ctx.count())
        elif ctx.Colon():
            exOperands = self.visitExCommand(ctx.exCommand())
            return ["exec"] + self.visitCount(ctx.count()) + [exOperands]
        elif ctx.LowerI():
            return ["input_mode"] + self.visitCount(ctx.count())
        elif ctx.viMotion():
            moOperands = self.visitViMotion(ctx.viMotion())
            return ["motion"] + self.visitCount(ctx.count()) + [moOperands]
        else:
            printf("End of vicommand")
            raise ValueError


    # Visit a parse tree produced by CommandParser#inCommand.
    def visitInCommand(self, ctx:CommandParser.InCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#exMoreCommand.
    def visitExMoreCommand(self, ctx:CommandParser.ExMoreCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#viMoreCommand.
    def visitViMoreCommand(self, ctx:CommandParser.ViMoreCommandContext):
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by CommandParser#viMoreCommand.
    def visitStart(self, ctx:CommandParser.StartContext):
        return self.visitViCommand(ctx.viCommand())

