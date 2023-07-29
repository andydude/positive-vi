# Generated from CommandParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .CommandParser import CommandParser
else:
    from CommandParser import CommandParser

# This class defines a complete generic visitor for a parse tree produced by CommandParser.

class CommandParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CommandParser#start.
    def visitStart(self, ctx:CommandParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#adr1.
    def visitAdr1(self, ctx:CommandParser.Adr1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#adr2.
    def visitAdr2(self, ctx:CommandParser.Adr2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#count.
    def visitCount(self, ctx:CommandParser.CountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#countCmd.
    def visitCountCmd(self, ctx:CommandParser.CountCmdContext):
        return self.visitChildren(ctx)


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


    # Visit a parse tree produced by CommandParser#value.
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#viMotion.
    def visitViMotion(self, ctx:CommandParser.ViMotionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#viCommand.
    def visitViCommand(self, ctx:CommandParser.ViCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#inCommand.
    def visitInCommand(self, ctx:CommandParser.InCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#exMoreCommand.
    def visitExMoreCommand(self, ctx:CommandParser.ExMoreCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#viMoreCommand.
    def visitViMoreCommand(self, ctx:CommandParser.ViMoreCommandContext):
        return self.visitChildren(ctx)



del CommandParser