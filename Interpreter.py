import AST
import Types
from utils import on, when

class Interpreter:

    @on('node')
    def visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')
    
    @when(AST.BinExpr)
    def visit(self, node):
        pass

    @when(AST.UnaryOp)
    def visit(self, node):
        pass

    @when(AST.Variable)
    def visit(self, node):
        pass

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
        pass

    @when(AST.IfElseStatement)
    def visit(self, node):
        pass

    @when(AST.WhileLoop)
    def visit(self, node):
        pass

    @when(AST.ForLoop)
    def visit(self, node):
        pass

    @when(AST.Range)
    def visit(self, node):
        return Types.Range(node.start, node.end)

    @when(AST.Break)
    def visit(self, node):
        pass

    @when(AST.Continue)
    def visit(self, node):
        pass

    @when(AST.Return)
    def visit(self, node):
        pass

    @when(AST.Print)
    def visit(self, node):
        pass

    @when(AST.Block)
    def visit(self, node):
        pass

    @when(AST.MatrixFunction)
    def visit(self, node):
        pass

    @when(AST.Vector)
    def visit(self, node):
        pass

    @when(AST.MatrixIndex)
    def visit(self, node):
        pass


