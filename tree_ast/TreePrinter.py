from __future__ import print_function
import tree_ast.AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        result = ""
        for stmt in self.statements:
            if stmt is not None:
                result += stmt.printTree(indent)
        return result
    
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        result = "| " * indent + self.op + "\n"
        result += self.left.printTree(indent + 1)
        result += self.right.printTree(indent + 1)
        return result
    
    @addToClass(AST.UnaryOp)
    def printTree(self, indent=0):
        result = "| " * indent + self.op + "\n"
        result += self.expr.printTree(indent + 1)
        return result

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return "| " * indent + str(self.value) + "\n"

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return "| " * indent + str(self.value) + "\n"

    @addToClass(AST.String)
    def printTree(self, indent=0):
        return "| " * indent + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return "| " * indent + self.name + "\n"

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        result = "| " * indent + "IF\n"
        result += self.condition.printTree(indent + 1)
        result += "| " * indent + "THEN\n"
        result += self.statement.printTree(indent + 1)
        return result

    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        result = "| " * indent + "IF\n"
        result += self.condition.printTree(indent + 1)
        result += "| " * indent + "THEN\n"
        result += self.true_statement.printTree(indent + 1)
        result += "| " * indent + "ELSE\n"
        result += self.false_statement.printTree(indent + 1)
        return result

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        result = "| " * indent + "WHILE\n"
        result += self.condition.printTree(indent + 1)
        result += self.statement.printTree(indent + 1)
        return result

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        result = "| " * indent + "FOR\n"
        result += "| " * (indent + 1) + self.variable + "\n"
        result += AST.Range(self.start, self.end).printTree(indent + 1)
        result += self.statement.printTree(indent + 1)
        return result

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        result = "| " * indent + "RANGE\n"
        result += self.start.printTree(indent + 1)
        result += self.end.printTree(indent + 1)
        return result

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        return "| " * indent + "BREAK\n"

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        return "| " * indent + "CONTINUE\n"

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        result = "| " * indent + "RETURN\n"
        result += self.value.printTree(indent + 1)
        return result

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        result = "| " * indent + "PRINT\n"
        for value in self.values:
            result += value.printTree(indent + 1)
        return result

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        result = ""
        for stmt in self.statements:
            if stmt is not None:
                result += stmt.printTree(indent)
        return result

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        result = "| " * indent + self.function + "\n"
        for arg in self.args:
            result += arg.printTree(indent + 1)
        return result

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        result = "| " * indent + "VECTOR\n"
        for elem in self.elements:
            result += elem.printTree(indent + 1)
        return result

    @addToClass(AST.MatrixIndex)
    def printTree(self, indent=0):
        result = "| " * indent + "REF\n"
        result += self.matrix.printTree(indent + 1)
        for idx in self.indices:
            result += idx.printTree(indent + 1)
        return result
