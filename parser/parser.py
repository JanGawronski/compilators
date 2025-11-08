from sly import Parser

from scanner.main import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", ">", "<", LEQ, GEQ, NEQ, EQ),
        ("left", "+", "-", DOTADD, DOTSUB),
        ("left", "*", "/", DOTMUL, DOTDIV, UMINUS),
    )

    @_('stmt_list')
    def program(self, p):
        return p.stmt_list

    @_('stmt_list stmt')
    def stmt_list(self, p):
        return p.stmt_list + [p.stmt]
    
    @_('"{" stmt_list "}"')
    def stmt(self, p):
        return ('block', p.stmt_list)
    
    @_('"{" "}"')
    def stmt(self, p):
        return ('block', [])

    @_('stmt')
    def stmt_list(self, p):
        return [p.stmt]
    
    @_('expr ";"')
    def stmt(self, p):
        return p.expr

    @_('expr "=" expr ";"')
    def stmt(self, p):
        return ('assign', p.expr0, p.expr1)

    @_('expr ADDASSIGN expr ";"')
    def stmt(self, p):
        return ('assign_op', p.expr0, '+=', p.expr1)

    @_('expr SUBASSIGN expr ";"')
    def stmt(self, p):
        return ('assign_op', p.expr0, '-=', p.expr1)

    @_('expr MULASSIGN expr ";"')
    def stmt(self, p):
        return ('assign_op', p.expr0, '*=', p.expr1)

    @_('expr DIVASSIGN expr ";"')
    def stmt(self, p):
        return ('assign_op', p.expr0, '/=', p.expr1)

    @_('PRINT expr_list ";"')
    def stmt(self, p):
        return ('print', p.expr_list)
    
    @_('IF "(" expr ")" stmt ELSE stmt')
    def stmt(self, p):
        return ('ifelse', p.expr, p.stmt0, p.stmt1)

    @_('IF "(" expr ")" stmt')
    def stmt(self, p):
        return ('if', p.expr, p.stmt)

    @_('WHILE "(" expr ")" stmt')
    def stmt(self, p):
        return ('while', p.expr, p.stmt)

    @_('FOR ID "=" expr ":" expr stmt')
    def stmt(self, p):
        return ('for', p.ID, p.expr0, p.expr1, p.stmt)

    @_('BREAK ";"')
    def stmt(self, p):
        return ('break',)

    @_('CONTINUE ";"')
    def stmt(self, p):
        return ('continue',)

    @_('RETURN expr ";"')
    def stmt(self, p):
        return ('return', p.expr)

    @_('expr "," expr_list')
    def expr_list(self, p):
        return [p.expr] + p.expr_list

    @_('expr')
    def expr_list(self, p):
        return [p.expr]
    
    @_('expr "[" expr_list "]"')
    def expr(self, p):
        return ('index', p.expr, p.expr_list)

    @_('"[" expr_list "]"')
    def expr(self, p):
        return ('list', p.expr_list)

    @_('expr "+" expr')
    def expr(self, p):
        return ("+", p.expr0, p.expr1)
    
    @_('expr "-" expr')
    def expr(self, p):
        return ("-", p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ("*", p.expr0, p.expr1)
    
    @_('expr "/" expr')
    def expr(self, p):
        return ("/", p.expr0, p.expr1)
    
    @_('expr "\'"')
    def expr(self, p):
        return ('transpose', p.expr)
    
    @_('expr DOTADD expr')
    def expr(self, p):
        return ('dotadd', p.expr0, p.expr1)

    @_('expr DOTSUB expr')
    def expr(self, p):
        return ('dotsub', p.expr0, p.expr1)

    @_('expr DOTMUL expr')
    def expr(self, p):
        return ('dotmul', p.expr0, p.expr1)

    @_('expr DOTDIV expr')
    def expr(self, p):
        return ('dotdiv', p.expr0, p.expr1)

    @_('expr EQ expr')
    def expr(self, p):
        return ('EQ', p.expr0, p.expr1)

    @_('expr NEQ expr')
    def expr(self, p):
        return ('NEQ', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('LT', p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ('GT', p.expr0, p.expr1)

    @_('expr LEQ expr')
    def expr(self, p):
        return ('LEQ', p.expr0, p.expr1)

    @_('expr GEQ expr')
    def expr(self, p):
        return ('GEQ', p.expr0, p.expr1)
    
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('uminus', p.expr)
    
    @_('INT')
    def expr(self, p):
        return int(p.INT)
    
    @_('FLOAT')
    def expr(self, p):
        return float(p.FLOAT)
    
    @_('STRING')
    def expr(self, p):
        return str(p.STRING)
    
    @_('ID')
    def expr(self, p):
        return ('var', p.ID)

    @_('ZEROS "(" expr_list ")"')
    def expr(self, p):
        return ('zeros', p.expr_list)

    @_('ONES "(" expr_list ")"')
    def expr(self, p):
        return ('ones', p.expr_list)

    @_('EYE "(" expr_list ")"')
    def expr(self, p):
        return ('eye', p.expr_list)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} (value: {p.value})")
            self.errok()
        else:
            print("Syntax error at EOF")
