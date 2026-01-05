class Node:
    def __str__(self):
        return self.printTree()

class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class BinExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

class UnaryOp(Node):
    def __init__(self, op, expr, lineno):
        self.op = op
        self.expr = expr
        self.lineno = lineno

class Variable(Node):
    def __init__(self, name, lvalue, lineno):
        self.name = name
        self.lvalue = lvalue
        self.lineno = lineno

class IntNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class FloatNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class String(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class IfStatement(Node):
    def __init__(self, condition, statement, lineno):
        self.condition = condition
        self.statement = statement
        self.lineno = lineno

class IfElseStatement(Node):
    def __init__(self, condition, true_statement, false_statement, lineno):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement
        self.lineno = lineno

class WhileLoop(Node):
    def __init__(self, condition, statement, lineno):
        self.condition = condition
        self.statement = statement
        self.lineno = lineno

class ForLoop(Node):
    def __init__(self, variable, start, end, statement, lineno):
        self.variable = variable
        self.start = start
        self.end = end
        self.statement = statement
        self.lineno = lineno

class Range(Node):
    def __init__(self, start, end, lineno):
        self.start = start
        self.end = end
        self.lineno = lineno

class Break(Node):
    def __init__(self, lineno):
        self.lineno = lineno

class Continue(Node):
    def __init__(self, lineno):
        self.lineno = lineno

class Return(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

class Print(Node):
    def __init__(self, values, lineno):
        self.values = values
        self.lineno = lineno

class Block(Node):
    def __init__(self, statements, lineno):
        self.statements = statements
        self.lineno = lineno

class MatrixFunction(Node):
    def __init__(self, function, args, lineno):
        self.function = function
        self.args = args
        self.lineno = lineno

class Vector(Node):
    def __init__(self, elements, lineno):
        self.elements = elements
        self.lineno = lineno

class MatrixIndex(Node):
    def __init__(self, matrix, indices, lineno):
        self.matrix = matrix
        self.indices = indices
        self.lineno = lineno