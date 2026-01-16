from inspect import indentsize
import AST
import Types
import Memory
import Exceptions
from utils import on, when

class Interpreter:
    def __init__(self):
        self.memory = Memory.Memory()
        self.bin_exprs = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            ".+": lambda a, b: a + b,
            ".-": lambda a, b: a - b,
            ".*": lambda a, b: a.ebe_mul(b),
            "./": lambda a, b: a / b,
            "+=": lambda a, b: a + b,
            "-=": lambda a, b: a - b,
            "*=": lambda a, b: a * b, 
            "/=": lambda a, b: a / b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
        }
        self.unary_ops = {
            "-": lambda x: -x,
            "\'": Types.Matrix.transpose
        }
        self.functions = {
            "eye": Types.Matrix.eye,
            "zeros": Types.Matrix.zeros,
            "ones": Types.Matrix.ones,
        }
            
    @on('node')
    def visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')

    @when(AST.Program)
    def visit(self, node):
        try:
            for instruction in node.instructions:
                self.visit(instruction)
        except Exceptions.Return:
            pass
                
    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op in ["=", "+=", "-=", "*=", "/="]:
            if node.op != "=":
                right = self.bin_exprs[node.op[0]](left, right)
            if type(node.left) == AST.MatrixIndex:
               indices = [self.visit(index) for index in node.left.indices]
               matrix = self.visit(node.left.matrix)
               if len(indices) == 1:
                   matrix.set(right, indices[0])
               else:
                   matrix.set(right, indices[0], indices[1])
               self.memory.put(node.left.matrix, matrix)
            else:
                self.memory.put(node.left.name, right)
            return
        return self.bin_exprs[node.op](left, right)
                
    @when(AST.UnaryOp)
    def visit(self, node):
        return self.unary_ops[node.op](self.visit(node.expr))
        
    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.IfStatement)
    def visit(self, node):
        if self.visit(node.condition):
            self.memory.push_scope()
            self.visit(node.statement)
            self.memory.pop_scope()

    @when(AST.IfElseStatement)
    def visit(self, node):
        if self.visit(node.condition):
            self.memory.push_scope()
            self.visit(node.true_statement)
            self.memory.pop_scope()
        else:
            self.memory.push_scope()
            self.visit(node.false_statement)
            self.memory.pop_scope()
            
    @when(AST.WhileLoop)
    def visit(self, node):
        while self.visit(node.condition):
            self.memory.push_scope()
            try:
                self.visit(node.statement)
            except Exceptions.Continue:
               self.memory.pop_scope()
               continue
            except Exceptions.Break:
                self.memory.pop_scope()
                return
            self.memory.pop_scope()

    @when(AST.ForLoop)
    def visit(self, node):
        range_expr = self.visit(node.range)
        for i in range(range_expr.start, range_expr.end):
            self.memory.push_scope()
            self.memory.put(node.variable, i)
            try:
                self.visit(node.statement)
            except Exceptions.Continue:
               self.memory.pop_scope()
               continue
            except Exceptions.Break:
                self.memory.pop_scope()
                return
            self.memory.pop_scope()

    @when(AST.Range)
    def visit(self, node):
        return Types.Range(self.visit(node.start), self.visit(node.end))
    
    @when(AST.Break)
    def visit(self, node):
        raise Exceptions.Break
        
    @when(AST.Continue)
    def visit(self, node):
        raise Exceptions.Continue

    @when(AST.Return)
    def visit(self, node):
        raise Exceptions.Return(self.visit(node.value))

    @when(AST.Print)
    def visit(self, node):
        print(*[self.visit(value) for value in node.values])

    @when(AST.Block)
    def visit(self, node):
        self.memory.push_scope()
        try:
            for statement in node.statements:
                self.visit(statement)
        except Exceptions.Return:
            pass 
        self.memory.pop_scope()

    @when(AST.MatrixFunction)
    def visit(self, node):
        args = [self.visit(arg) for arg in node.args]
        if len(args) == 1:
            return self.functions[node.function](args[0])
        else:
            return self.functions[node.function](args[0], args[1])

    @when(AST.Vector)
    def visit(self, node):
        elements = [self.visit(e) for e in node.elements]
        if type(elements[0]) == Types.Vector:
            return Types.Matrix([e.vector for e in elements])
        else:
            return Types.Vector(elements)
        
    @when(AST.MatrixIndex)
    def visit(self, node):
        matrix = self.visit(node.matrix)
        indices = [self.visit(index) for index in node.indices]
        if len(indices) == 1:
            return matrix.get(indices[0])
        else:
            return matrix.get(indices[0], indices[1])
