from sly import Parser

from scanner.main import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    # TODO: dodac negacje unarna do skanera UNMINUS
    precedence = (
        ("nonassoc", LEQ, GEQ, NEQ, EQ),
        ("left", "+", "-", DOTADD, DOTSUB),
        ("left", "*", "/", DOTMUL, DOTDIV, UNMINUS),
    )

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

    @_("expr ADDASSIGN term")
    def expr(self, p):
        return p.expr / p.term

    @_("instructions_opt")
    def program(p):
        pass

    @_("instructions")
    def instructions_opt(p):
        pass

    @_("")
    def instructions_opt(p):
        pass

    @_("instructions instruction")
    def instructions(p):
        pass

    @_("instruction")
    def instructions(p):
        pass

    # to finish the grammar
    # ....
