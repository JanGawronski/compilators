import sys

from sly import Parser

from scanner.main import Scanner

sys.path.append("..")
import tree_ast.AST as AST


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
        ("nonassoc", ">", "<", LEQ, GEQ, NEQ, EQ),
        ("left", "+", "-", DOTADD, DOTSUB),
        ("left", "*", "/", DOTMUL, DOTDIV),
        ("right", UMINUS),
    )

    @_("stmt_list")
    def program(self, p):
        return AST.Program(p.stmt_list)

    @_("stmt_list stmt")
    def stmt_list(self, p):
        return p.stmt_list + [p.stmt]

    @_('"{" stmt_list "}"')
    def stmt(self, p):
        return AST.Block(p.stmt_list)

    @_('"{" "}"')
    def stmt(self, p):
        return AST.Block([])

    @_("stmt")
    def stmt_list(self, p):
        return [p.stmt]

    @_('expr ";"')
    def stmt(self, p):
        return p.expr

    @_('expr "=" expr ";"')
    @_('expr ADDASSIGN expr ";"')
    @_('expr SUBASSIGN expr ";"')
    @_('expr MULASSIGN expr ";"')
    @_('expr DIVASSIGN expr ";"')
    def stmt(self, p):
        return AST.BinExpr(p[1], p.expr0, p.expr1)

    @_('PRINT expr_list ";"')
    def stmt(self, p):
        return AST.Print(p.expr_list)

    @_('IF "(" expr ")" stmt ELSE stmt')
    def stmt(self, p):
        return AST.IfElseStatement(p.expr, p.stmt0, p.stmt1)

    @_('IF "(" expr ")" stmt %prec IFX')
    def stmt(self, p):
        return AST.IfStatement(p.expr, p.stmt)

    @_('WHILE "(" expr ")" stmt')
    def stmt(self, p):
        return AST.WhileLoop(p.expr, p.stmt)

    @_('FOR ID "=" expr ":" expr stmt')
    def stmt(self, p):
        return AST.ForLoop(p.ID, p.expr0, p.expr1, p.stmt)

    @_('BREAK ";"')
    def stmt(self, p):
        return AST.Break()

    @_('CONTINUE ";"')
    def stmt(self, p):
        return AST.Continue()

    @_('RETURN expr ";"')
    def stmt(self, p):
        return AST.Return(p.expr)

    @_('expr "," expr_list')
    def expr_list(self, p):
        return [p.expr] + p.expr_list

    @_("expr")
    def expr_list(self, p):
        return [p.expr]

    @_('expr "[" expr_list "]"')
    def expr(self, p):
        return AST.MatrixIndex(p.expr, p.expr_list)

    @_('"[" expr_list "]"')
    def expr(self, p):
        return AST.Vector(p.expr_list)

    @_('expr "+" expr')
    @_('expr "-" expr')
    @_('expr "*" expr')
    @_('expr "/" expr')
    @_("expr DOTADD expr")
    @_("expr DOTSUB expr")
    @_("expr DOTMUL expr")
    @_("expr DOTDIV expr")
    @_("expr EQ expr")
    @_("expr NEQ expr")
    @_('expr "<" expr')
    @_('expr ">" expr')
    @_("expr LEQ expr")
    @_("expr GEQ expr")
    def expr(self, p):
        return AST.BinExpr(p[1], p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.UnaryOp("-", p.expr)

    @_('expr "\'"')
    def expr(self, p):
        return AST.UnaryOp("\'", p.expr)

    @_("INT")
    def expr(self, p):
        return AST.IntNum(int(p.INT))

    @_("FLOAT")
    def expr(self, p):
        return AST.FloatNum(float(p.FLOAT))

    @_("STRING")
    def expr(self, p):
        return AST.String(str(p.STRING))

    @_("ID")
    def expr(self, p):
        return AST.Variable(p.ID)

    @_('ZEROS "(" expr_list ")"')
    @_('ONES "(" expr_list ")"')
    @_('EYE "(" expr_list ")"')
    def expr(self, p):
        return AST.MatrixFunction(p[0], p.expr_list)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} (value: {p.value})")
            self.errok()
        else:
            print("Syntax error at EOF")
