import AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def printElement(text, indent):
    return "| " * indent + text + "\n"

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        return "".join([instruction.printTree(indent) for instruction in self.instructions if instruction is not None])
    
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return printElement(self.op, indent) + \
               self.left.printTree(indent + 1) + \
               self.right.printTree(indent + 1)
    
    @addToClass(AST.UnaryOp)
    def printTree(self, indent=0):
        return printElement(self.op, indent) + \
               self.expr.printTree(indent + 1) 

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return printElement(str(self.value), indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return printElement(str(self.value), indent)
    
    @addToClass(AST.String)
    def printTree(self, indent=0):
        return printElement(str(self.value), indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return printElement(str(self.name), indent)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        return printElement("IF", indent) + \
               self.condition.printTree(indent + 1) + \
               printElement("THEN", indent) + \
               self.statement.printTree(indent + 1)
    
    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        return printElement("IF", indent) + \
               self.condition.printTree(indent + 1) + \
               printElement("THEN", indent) + \
               self.true_statement.printTree(indent + 1) + \
               printElement("ELSE", indent) + \
               self.false_statement.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        return printElement("WHILE", indent) + \
               self.condition.printTree(indent + 1) + \
               self.statement.printTree(indent + 1)
        
    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        return printElement("FOR", indent) + \
               printElement(self.variable, indent + 1) + \
               self.range.printTree(indent + 1) + \
               self.statement.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        return printElement("RANGE", indent) + \
               self.start.printTree(indent + 1) + \
               self.end.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        return printElement("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        return printElement("CONTINUE", indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        return printElement("RETURN", indent) + \
               self.value.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        return printElement("PRINT", indent) + \
               "".join([value.printTree(indent + 1) for value in self.values])

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        return "".join([stmt.printTree(indent) for stmt in self.statements if stmt is not None])

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        return "".join([arg.printTree(indent + 1) for arg in self.args])

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        return printElement("VECTOR", indent) + \
               "".join([elem.printTree(indent + 1) for elem in self.elements])

    @addToClass(AST.MatrixIndex)
    def printTree(self, indent=0):
        return printElement("REF", indent) + \
               self.matrix.printTree(indent + 1) + \
               "".join([idx.printTree(indent + 1) for idx in self.indices])
