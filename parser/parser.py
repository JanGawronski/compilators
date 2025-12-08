import sys

from sly import Parser

from scanner.main import Scanner

sys.path.append("..")
import tree_ast.AST as AST


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', '<', '>', 'LEQ', 'GEQ', 'NEQ', 'EQ'),
        ('left', '+', '-'),
        ('left', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ('left', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', "'"),
    )

    @_('instructions')
    def program(self, p):
        return AST.Program(p.instructions)

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('statement ";"')
    def instruction(self, p):
        return p.statement

    @_('"{" instructions "}"')
    def instruction(self, p):
        return AST.Block(p.instructions)
    
    @_('"{" "}"')
    def instruction(self, p):
        return AST.Block([])

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.IfStatement(p.condition, p.instruction)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.IfElseStatement(p.condition, p.instruction0, p.instruction1)
    
    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.WhileLoop(p.condition, p.instruction)
    
    @_('FOR ID "=" expr ":" expr instruction')
    def instruction(self, p):
        return AST.ForLoop(p.ID, p.expr0, p.expr1, p.instruction)

    @_('EQ', 'NEQ', 'LEQ', 'GEQ', '">"', '"<"')
    def comparator(self, p):
        return p[0]

    @_('expr comparator expr')
    def condition(self, p):
        return AST.BinExpr(p.comparator, p.expr0, p.expr1)

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assign_op(self, p):
        return p[0]

    @_('element assign_op expr')
    def statement(self, p):
        return AST.BinExpr(p[1], p.element, p.expr)

    @_('ID assign_op expr')
    def statement(self, p):
        return AST.BinExpr(p[1], AST.Variable(p.ID), p.expr)

    @_('function_name "(" var_args ")"')
    def expr(self, p):
        return AST.MatrixFunction(p[0], p.var_args)
    
    @_('EYE', 'ONES', 'ZEROS')
    def function_name(self, p):
        return p[0]

    @_('"[" var_args "]"')
    def matrix(self, p):
        return AST.Vector(p.var_args)

    @_('var "[" var_args "]"')
    def element(self, p):
        return AST.MatrixIndex(AST.Variable(p.var), p.var_args)

    @_('ID')
    def var(self, p):
        return AST.Variable(p.ID)

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p.expr0, p.expr1)

    @_('var', 'matrix', 'element')
    def expr(self, p):
        return p[0]

    @_('INT')
    def expr(self, p):
        return AST.IntNum(int(p.INT))

    @_('FLOAT')
    def expr(self, p):
        return AST.FloatNum(float(p.FLOAT))

    @_('STRING')
    def expr(self, p):
        return AST.String(str(p.STRING))

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.UnaryOp("-", p.expr)

    @_('expr "\'"')
    def expr(self, p):
        return AST.UnaryOp("\'", p.expr)

    @_('BREAK')
    def statement(self, p):
        return AST.Break()

    @_('CONTINUE')
    def statement(self, p):
        return AST.Continue()

    @_('RETURN expr')
    def statement(self, p):
        return AST.Return(p.expr)

    @_('PRINT var_args')
    def statement(self, p):
        return AST.Print(p.var_args)

    @_('var_args "," expr')
    def var_args(self, p):
        return p.var_args + [p.expr]

    @_('expr')
    def var_args(self, p):
        return [p.expr]

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} (value: {p.value})")
            self.errok()
        else:
            print("Syntax error at EOF")