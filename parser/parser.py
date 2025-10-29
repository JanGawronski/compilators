from sly import Parser

from scanner.main import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", LEQ, GEQ, NEQ, EQ),
        ("left", "+", "-", DOTADD, DOTSUB),
        ("left", "*", "/", DOTMUL, DOTDIV, UMINUS),
    )

    @_("instructions_opt")
    def program(p):
        return p.instructions_opt

    @_("instructions")
    def instructions_opt(p):
        return p.instructions

    @_("")
    def instructions_opt(p):
        return []

    @_("instructions instruction")
    def instructions(p):
        return p.instructions + [p.instruction]

    @_("instruction")
    def instructions(p):
        return [p.instruction]

    @_('expr "+" term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr "-" term')
    def expr(self, p):
        return p.expr - p.term

    @_('expr "*" term')
    def expr(self, p):
        return p.expr * p.term

    @_('expr "/" term')
    def expr(self, p):
        return p.expr / p.term

    @_('"-" expr %prec UMINUS')
    def expr(p):
        return -p.expr

    @_("expr ADDASSIGN term")
    def expr(self, p):
        return p.expr / p.term
