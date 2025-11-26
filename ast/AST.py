class Node:
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class RelOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignOp(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AssignOpOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Variable(Node):
    def __init__(self, name):
        self.name = name


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class IfStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement


class IfElseStatement(Node):
    def __init__(self, condition, true_statement, false_statement):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement


class WhileLoop(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement


class ForLoop(Node):
    def __init__(self, variable, start, end, statement):
        self.variable = variable
        self.start = start
        self.end = end
        self.statement = statement


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Break(Node):
    pass


class Continue(Node):
    pass


class Return(Node):
    def __init__(self, value):
        self.value = value


class Print(Node):
    def __init__(self, values):
        self.values = values


class Block(Node):
    def __init__(self, statements):
        self.statements = statements


class UnaryMinus(Node):
    def __init__(self, expr):
        self.expr = expr


class Transpose(Node):
    def __init__(self, expr):
        self.expr = expr


class MatrixFunction(Node):
    def __init__(self, function, args):
        self.function = function
        self.args = args


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class MatrixIndex(Node):
    def __init__(self, matrix, indices):
        self.matrix = matrix
        self.indices = indices
