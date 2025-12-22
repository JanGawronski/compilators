from SymbolTable import SymbolTable
import AST

class TypeChecker(object):
    symbol_table = SymbolTable(None, "global")

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def visit_Program(self, node):
        for instruction in node.instructions:
            try:
                self.visit(instruction)
            except Exception as e:
                print(e)

    def visit_BinExpr(self, node):
        left_type, left_value = self.visit(node.left)
        right_type, right_value = self.visit(node.right)
        op = node.op 
        if op in ('+', '-'):
            if left_type == 'int' and right_type == 'int':
                return ('int', None)
            elif (left_type == 'int' and right_type == 'float') or (left_type == 'float' and right_type == 'int') or (left_type == 'float' and right_type == 'float'):
                return ('float', None)
            else:
                raise TypeError(f"Type error in binary expression: {left_type} {op} {right_type} on line {node.lineno}")
        
        elif op == '*':
            if left_type == 'int' and right_type == 'int':
                return ('int', None)
            elif (left_type == 'int' and right_type == 'float') or (left_type == 'float' and right_type == 'int') or (left_type == 'float' and right_type == 'float'):
                return ('float', None)
            elif (left_type == 'matrix' and right_type == 'matrix'):
                if left_value[1] is not None and right_value[0] is not None and left_value[1] != right_value[0]:
                    raise TypeError(f"Dimension mismatch in matrix multiplication: {left_value} * {right_value} on line {node.lineno}")
                return ('matrix', (left_value[0], right_value[1]))
            elif (left_type in ('vector', 'matrix') and right_type in ('int', 'float')) or (left_type in ('int', 'float') and right_type in ('vector', 'matrix')):
                return (left_type if left_type in ('vector', 'matrix') else right_type, left_value if left_type in ('vector', 'matrix') else right_value)
            else:
                raise TypeError(f"Type error in binary expression: {left_type} {op} {right_type} on line {node.lineno}")

        elif op == '/':
            if left_type == 'int' and right_type == 'int':
                return ('int', None)
            elif (left_type == 'int' and right_type == 'float') or (left_type == 'float' and right_type == 'int') or (left_type == 'float' and right_type == 'float'):
                return ('float', None)
            elif (left_type in ('vector', 'matrix') and right_type in ('int', 'float')):
                return left_type, left_value
            else:
                raise TypeError(f"Type error in binary expression: {left_type} {op} {right_type} on line {node.lineno}")
        
        elif op in ('.+', '.-', '.*', './'):
            if left_type == right_type and left_type in ('vector', 'matrix'):
                if left_value == right_value:
                    return (left_type, left_value)
                if left_type == 'vector': 
                    if left_value is not None and right_value is not None and left_value != right_value:
                        raise TypeError(f"Dimension mismatch in binary expression: {left_value} {op} {right_value} on line {node.lineno}")
                    return (left_type, left_value if left_value is not None else right_value)
                if left_type == 'matrix':
                    if left_value[0] is not None and right_value[0] is not None and left_value[0] != right_value[0]:
                        raise TypeError(f"Dimension mismatch in binary expression: {left_value} {op} {right_value} on line {node.lineno}")
                    if left_value[1] is not None and right_value[1] is not None and left_value[1] != right_value[1]:
                        raise TypeError(f"Dimension mismatch in binary expression: {left_value} {op} {right_value} on line {node.lineno}")
                    
                    return (left_type, (left_value[0] if left_value[0] is not None else right_value[0],
                                        left_value[1] if left_value[1] is not None else right_value[1]))
            else:
                raise TypeError(f"Type error in binary expression: {left_type} {op} {right_type} on line {node.lineno}")
            
        elif op in ("==", '!='):
            if left_type == right_type:
                return 'bool'
            else:
                raise TypeError(f"Type error in equality comparison: {left_type} {op} {right_type} on line {node.lineno}")
            
        elif op in ('<', '>', '<=', '>='):
            if (left_type in ('int', 'float')) and (right_type in ('int', 'float')):
                return 'bool'
            else:
                raise TypeError(f"Type error in comparison: {left_type} {op} {right_type} on line {node.lineno}")
            
        elif op in ('+=', '-=', '*=', '/='):
            if left_type == right_type and left_type in ('int', 'float'):
                return (left_type, None)
            else:
                raise TypeError(f"Type error in assignment operation: {left_type} {op} {right_type} on line {node.lineno}")
            
        elif op == '=':
            if type(node.left) == AST.MatrixIndex:
                if right_type in ('int', 'float'):
                    return (right_type, right_value)
                else:
                    raise TypeError(f"Type error in assignment to matrix index: {left_type} = {right_type} on line {node.lineno}")
            self.symbol_table.put(node.left.name, (right_type, right_value))
            return (right_type, right_value)
        
    def visit_UnaryOp(self, node):
        expr, expr_value = self.visit(node.expr)
        op = node.op
        if op == '-':
            if expr in ('int', 'float'):
                return (expr, None)
            else:
                raise TypeError(f"Type error in unary operation: {op}{expr} on line {node.lineno}")
        elif op == "'":
            if expr == 'matrix':
                return (expr, (expr_value[1], expr_value[0]))
            else:
                raise TypeError(f"Type error in transpose operation: {expr}{op} on line {node.lineno}")

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            if node.lvalue:
                self.symbol_table.put(node.name, ("undefined", None))
                return ("undefined", None)
            else:
                raise NameError(f"Undefined variable '{node.name}' on line {node.lineno}")
        return symbol

    def visit_IntNum(self, node):
        return ('int', node.value)
    
    def visit_FloatNum(self, node):
        return ('float', node.value)
    
    def visit_String(self, node):
        return ('string', node.value)
    
    def visit_IfStatement(self, node):
        try:
            condition_type = self.visit(node.condition)
            if condition_type != 'bool':
                raise TypeError(f"Condition in if statement must be boolean on line {node.lineno}")
        except Exception as e:
            print(e)
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfElseStatement(self, node):
        try:
            condition_type = self.visit(node.condition)
            if condition_type != 'bool':
                raise TypeError(f"Condition in if-else statement must be boolean on line {node.lineno}")
        except Exception as e:
            print(e)
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.true_statement)
        self.symbol_table = self.symbol_table.popScope()
        self.symbol_table = self.symbol_table.pushScope("else")
        self.visit(node.false_statement)
        self.symbol_table = self.symbol_table.popScope()

    def visit_WhileLoop(self, node):
        try:
            condition_type = self.visit(node.condition)
            if condition_type != 'bool':
                raise TypeError(f"Condition in while loop must be boolean on line {node.lineno}")
        except Exception as e:
            print(e)
        self.symbol_table = self.symbol_table.pushScope("while")
        self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()
    
    def visit_ForLoop(self, node):
        try:
            start_type, start_value = self.visit(node.start)
            end_type, end_value = self.visit(node.end)
            if start_type != 'int' or end_type != 'int':
                raise TypeError(f"Start and end expressions in for loop must be integers on line {node.lineno}")
        except Exception as e:
            print(e)
        self.symbol_table = self.symbol_table.pushScope("for")
        self.symbol_table.put(node.variable, ('int', None))
        self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Range(self, node):
        start_type, start_value = self.visit(node.start)
        end_type, end_value = self.visit(node.end)
        if start_type != 'int' or end_type != 'int':
            raise TypeError(f"Start and end expressions in range must be integers on line {node.lineno}")
        return 'range'
    
    def visit_Break(self, node):
        scope = self.symbol_table
        while scope is not None:
            if scope.name in ("while", "for"):
                return
            scope = scope.getParentScope()
        raise SyntaxError(f"'break' statement not within loop on line {node.lineno}")
    
    def visit_Continue(self, node):
        scope = self.symbol_table
        while scope is not None:
            if scope.name in ("while", "for"):
                return
            scope = scope.getParentScope()
        raise SyntaxError(f"'continue' statement not within loop on line {node.lineno}")
    
    def visit_Return(self, node):
        return self.visit(node.value)
    
    def visit_Print(self, node):
        for value in node.values:
            self.visit(value)

    def visit_Block(self, node):
        self.symbol_table = self.symbol_table.pushScope("block")
        for statement in node.statements:
            try:
                self.visit(statement)
            except Exception as e:
                print(e)
        self.symbol_table = self.symbol_table.popScope()

    def visit_MatrixFunction(self, node):
        if len(node.args) not in (1, 2):
            raise TypeError(f"Matrix function '{node.function}' expects 1 or 2 arguments (got {len(node.args)}) on line {node.lineno}")

        if len(node.args) == 1:
            arg_type, arg_value = self.visit(node.args[0])
            if arg_type != 'int':
                raise TypeError(f"Matrix function '{node.function}' expects integer argument (got {arg_type}) on line {node.lineno}")
            return ('matrix', (arg_value, arg_value))

        elif len(node.args) == 2:
            arg1_type, arg1_value = self.visit(node.args[0])
            arg2_type, arg2_value = self.visit(node.args[1])
            if arg1_type != 'int' or arg2_type != 'int':
                raise TypeError(f"Matrix function '{node.function}' expects integer arguments (got {arg1_type}, {arg2_type}) on line {node.lineno}")
            return ('matrix', (arg1_value, arg2_value))

    def visit_Vector(self, node):
        elements = [self.visit(element) for element in node.elements]
        if all(t[0] == 'int' or t[0] == 'float' for t in elements):
            return ('vector', len(elements))

        if all(t[0] == 'vector' for t in elements):
            lengths = set(elem[1] for elem in elements if elem[1] is not None)
            if len(lengths) > 1:
                raise TypeError(f"All vectors in vector of vectors must have the same length on line {node.lineno}")
            if len(lengths) == 1:
                return ('matrix', (lengths.pop(), len(elements)))
            else:
                return ('matrix', (None, len(elements)))
            
        raise TypeError(f"Invalid elements in vector on line {node.lineno}")
    
    def visit_MatrixIndex(self, node):
        type, dimensions = self.visit(node.matrix)
        if type != 'matrix':
            raise TypeError(f"Attempting to index a non-matrix type '{type}' on line {node.lineno}")
        if len(node.indices) != 2:
            raise TypeError(f"Matrix indexing requires 2 indices (got {len(node.indices)}) on line {node.lineno}")
        index0_type, index0_value = self.visit(node.indices[0])
        index1_type, index1_value = self.visit(node.indices[1])
        if index0_type != 'int' or index1_type != 'int':
            raise TypeError(f"Matrix indices must be integers (got {index0_type}, {index1_type}) on line {node.lineno}")

        if dimensions[0] is not None and index0_value is not None and index0_value >= dimensions[0]:
            raise IndexError(f"Row index {index0_value} out of bounds for matrix with {dimensions[0]} rows on line {node.lineno}")
        
        if dimensions[1] is not None and index1_value is not None and index1_value >= dimensions[1]:
            raise IndexError(f"Column index {index1_value} out of bounds for matrix with {dimensions[1]} columns on line {node.lineno}")
        
        return ('float', None)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')