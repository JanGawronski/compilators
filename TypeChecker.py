from SymbolTable import SymbolTable
import AST

class TypeChecker(object):
    
    def __init__(self) -> None:
        self.symbol_table = SymbolTable(None, "global")
        self.functions = \
            {(sign, (x, y)): (max(x, y), ("no_check", "no_check")) for x in ["float", "int"] for y in ["float", "int"] for sign in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']} | \
            {(sign, (x, x)): (x, ("same_dim", "left_input_dim")) for x in ["vector", "matrix"] for sign in ['.+', '.-', '.*', './', "+", "-"]} | \
            {('*', ('matrix', 'matrix')): ('matrix', ("matrix_mult_dim", "matrix_mult_result"))} | \
            {(sign, (x, y)): (x, ("no_check", "no_check")) for x in ["vector", "matrix"] for y in ["int", "float"] for sign in ['*', '/', '*=', '-=']} | \
            {('*', (x, y)): (y, ("no_check", "no_check")) for x in ["int", "float"] for y in ["vector", "matrix"]} | \
            {(sign, (x, x)): ('bool', ("no_check", "no_check")) for x in ["int", "float", "string", "matrix", "vector"] for sign in ['==', '!=']} | \
            {(sign, (x, y)): ('bool', ("no_check", "no_check")) for x in ["int", "float"] for y in ["int", "float"] for sign in ['<', '<=', '>', '>=']} | \
            {('\'', 'matrix'): ('matrix', ("no_check", "tranpose"))} | \
            {('-', x): (x, ("no_check", "no_check")) for x in ["int", "float"]}

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def visit_Program(self, node):
        for instruction in node.instructions:
            _, _, errors = self.visit(instruction)
            for error in errors:
                print(error)

    def visit_BinExpr(self, node):
        left_type, left_value, left_errors = self.visit(node.left)
        right_type, right_value, right_errors = self.visit(node.right)
        op = node.op

        if left_errors or right_errors:
            return ('error', None, left_errors + right_errors)

        if op == '=':
            if type(node.left) == AST.MatrixIndex:
                if left_type == "float" and right_type in ('int', 'float'):
                    return (right_type, right_value, [])
                elif left_type == right_type == 'vector':
                    if left_value is not None and right_value is not None and left_value != right_value:
                        return ('error', None, [f"Dimension mismatch in assignment to vector index: {left_value} = {right_value} on line {node.lineno}"])
                    return (right_type, right_value, [])
                elif left_type == right_type == 'matrix':
                    if left_value[0] is not None and right_value[0] is not None and left_value[0] != right_value[0] or \
                       left_value[1] is not None and right_value[1] is not None and left_value[1] != right_value[1]:
                        return ('error', None, [f"Dimension mismatch in assignment to matrix index: {left_value} = {right_value} on line {node.lineno}"])
                    return (right_type, right_value, [])
                else:
                    return ('error', None, [f"Type error in assignment to matrix index: {left_type} = {right_type} on line {node.lineno}"])
            self.symbol_table.put(node.left.name, (right_type, right_value))
            return (right_type, right_value, [])
        
        if (op, (left_type, right_type)) not in self.functions:
            return ('error', None, [f"Type error: {left_type} {op} {right_type} on line {node.lineno}"])

        output_type, (check_input, check_output) = self.functions[(op, (left_type, right_type))]

        if check_input == "same_dim":
            if left_type == 'vector':
                if left_value is not None and right_value is not None and left_value != right_value:
                    return ('error', None, [f"Dimension mismatch in binary expression: {left_value} {op} {right_value} on line {node.lineno}"])
            elif left_type == 'matrix':
                if left_value[0] is not None and right_value[0] is not None and left_value[0] != right_value[0] or \
                   left_value[1] is not None and right_value[1] is not None and left_value[1] != right_value[1]:
                    return ('error', None, [f"Dimension mismatch in binary expression: {left_value} {op} {right_value} on line {node.lineno}"])
                
        if check_input == "matrix_mult_dim":
            if left_value[1] is not None and right_value[0] is not None and left_value[1] != right_value[0]:
                return ('error', None, [f"Dimension mismatch in matrix multiplication: {left_value} * {right_value} on line {node.lineno}"])

        if check_output == "no_check":
            return (output_type, None, [])
        if check_output == "left_input_dim":
            return (output_type, left_value, [])
        if check_output == "matrix_mult_result":
            return (output_type, (left_value[0], right_value[1]), [])
        
    def visit_UnaryOp(self, node):
        expr, expr_value, errors = self.visit(node.expr)
        op = node.op

        if errors:
            return ('error', None, errors)

        if (op, expr) not in self.functions:
            return ('error', None, [f"Type error in unary operation: {op}{expr} on line {node.lineno}"])
        
        output_type, (check_input, check_output) = self.functions[(op, expr)]

        if check_output == "tranpose":
            return (output_type, (expr_value[1], expr_value[0]), [])
        
        return (output_type, None, [])

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            if node.lvalue:
                self.symbol_table.put(node.name, ("undefined", None))
                return ("undefined", None, [])
            else:
                return ('error', None, [f"Undefined variable '{node.name}' on line {node.lineno}"])
        return symbol[0], symbol[1], []

    def visit_IntNum(self, node):
        return ('int', node.value, [])
    
    def visit_FloatNum(self, node):
        return ('float', node.value, [])
    
    def visit_String(self, node):
        return ('string', node.value, [])
    
    def visit_IfStatement(self, node):
        condition_type, _, errors = self.visit(node.condition)

        self.symbol_table = self.symbol_table.pushScope("if")
        _, _, inside_errors = self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()

        if errors:
            return ('error', None, errors + inside_errors)
        
        if condition_type != 'bool':
            return ('error', None, [f"Condition in if statement must be boolean on line {node.lineno}"] + inside_errors)
        
        if inside_errors:
            return ('error', None, inside_errors)
        
        return (None, None, [])

    def visit_IfElseStatement(self, node):
        condition_type, _, errors = self.visit(node.condition)

        self.symbol_table = self.symbol_table.pushScope("if")
        _, _, if_errors = self.visit(node.true_statement)
        self.symbol_table = self.symbol_table.popScope()

        self.symbol_table = self.symbol_table.pushScope("else")
        _, _, else_errors = self.visit(node.false_statement)
        self.symbol_table = self.symbol_table.popScope()

        if errors:
            return ('error', None, errors + if_errors + else_errors)
        
        if condition_type != 'bool':
            return ('error', None, [f"Condition in if-else statement must be boolean on line {node.lineno}"] + if_errors + else_errors)

        if if_errors or else_errors:
            return ('error', None, if_errors + else_errors)

        return (None, None, [])

    def visit_WhileLoop(self, node):
        condition_type, _, errors = self.visit(node.condition)

        self.symbol_table = self.symbol_table.pushScope("while")
        _, _, inside_errors = self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()
    
        if errors:
            return ('error', None, errors + inside_errors)

        if condition_type != 'bool':
            return ('error', None, [f"Condition in while loop must be boolean on line {node.lineno}"] + inside_errors)
        
        if inside_errors:
            return ('error', None, inside_errors)
        
        return (None, None, [])

    def visit_ForLoop(self, node):
        start_type, start_value, start_errors = self.visit(node.start)
        end_type, end_value, end_errors = self.visit(node.end)

        self.symbol_table = self.symbol_table.pushScope("for")
        self.symbol_table.put(node.variable, ('int', None))
        _, _, inside_errors = self.visit(node.statement)
        self.symbol_table = self.symbol_table.popScope()

        if start_errors or end_errors:
            return ('error', None, start_errors + end_errors + inside_errors)
        
        if start_type != 'int' or end_type != 'int':
            return ('error', None, [f"Start and end expressions in for loop must be integers on line {node.lineno}"] + inside_errors)
        
        if inside_errors:
            return ('error', None, inside_errors)
        
        return (None, None, [])

    def visit_Range(self, node):
        start_type, start_value, start_errors = self.visit(node.start)
        end_type, end_value, end_errors = self.visit(node.end)

        if not start_errors and start_type != 'int':
            start_errors.append(f"Start expression in range must be integer on line {node.lineno}")

        if not end_errors and end_type != 'int':
            end_errors.append(f"End expression in range must be integer on line {node.lineno}")

        if start_errors or end_errors:
            return ('error', None, start_errors + end_errors)

        return ('range', (start_value, end_value), [])
    
    def visit_Break(self, node):
        scope = self.symbol_table
        while scope is not None:
            if scope.name in ("while", "for"):
                return (None, None, [])
            scope = scope.getParentScope()
        return ('error', None, [f"'break' statement not within loop on line {node.lineno}"])
    
    def visit_Continue(self, node):
        scope = self.symbol_table
        while scope is not None:
            if scope.name in ("while", "for"):
                return (None, None, [])
            scope = scope.getParentScope()
        return ('error', None, [f"'continue' statement not within loop on line {node.lineno}"])
    
    def visit_Return(self, node):
        return self.visit(node.value)
    
    def visit_Print(self, node):
        errors = []
        for value in node.values:
            errors.extend(self.visit(value)[2])
        if errors:
            return ('error', None, errors)
        return (None, None, [])

    def visit_Block(self, node):
        self.symbol_table = self.symbol_table.pushScope("block")
        errors = []
        for statement in node.statements:
            errors.extend(self.visit(statement)[2])
        self.symbol_table = self.symbol_table.popScope()
        if errors:
            return ('error', None, errors)
        return (None, None, [])

    def visit_MatrixFunction(self, node):
        if len(node.args) == 0:
            return ('error', None, [f"Matrix function '{node.function}' expects 1 or 2 arguments (got {len(node.args)}) on line {node.lineno}"])

        errors = []
        if len(node.args) > 2:
            errors.append(f"Matrix function '{node.function}' expects 1 or 2 arguments (got {len(node.args)}) on line {node.lineno}")

        if len(node.args) == 1:
            arg_type, arg_value, errors = self.visit(node.args[0])
            if errors:
                return ('error', None, errors)
            if arg_type != 'int':
                return ('error', None, [f"Matrix function '{node.function}' expects integer argument (got {arg_type}) on line {node.lineno}"])
            return ('matrix', (arg_value, arg_value), [])

        elif len(node.args) >= 2:
            arg1_type, arg1_value, arg1_errors = self.visit(node.args[0])
            arg2_type, arg2_value, arg2_errors = self.visit(node.args[1])
            if arg1_errors and arg2_errors:
                return ('error', None, errors + arg1_errors + arg2_errors)

            if arg1_errors and arg2_type != 'int':
                return ('error', None, errors + arg1_errors + [f"Matrix function '{node.function}' expects integer argument (got error, {arg2_type}) on line {node.lineno}"])
            if arg2_errors and arg1_type != 'int':
                return ('error', None, errors + arg2_errors + [f"Matrix function '{node.function}' expects integer argument (got {arg1_type}, error) on line {node.lineno}"])

            if arg1_type != 'int' or arg2_type != 'int':
                return ('error', None, errors + [f"Matrix function '{node.function}' expects integer arguments (got {arg1_type}, {arg2_type}) on line {node.lineno}"])
            return ('matrix', (arg1_value, arg2_value), errors)

    def visit_Vector(self, node):
        elements = [self.visit(element) for element in node.elements]
        errors = []
        for _, _, elem_errors in elements:
            errors.extend(elem_errors)

        if errors:
            return ('error', None, errors)

        if all(t[0] == 'int' or t[0] == 'float' for t in elements):
            return ('vector', len(elements), [])

        if all(t[0] == 'vector' for t in elements):
            lengths = set(elem[1] for elem in elements if elem[1] is not None)
            if len(lengths) > 1:
                return ('error', None, [f"All vectors in vector of vectors must have the same length on line {node.lineno}"])
            if len(lengths) == 1:
                return ('matrix', (lengths.pop(), len(elements)), [])
            else:
                return ('matrix', (None, len(elements)), [])
            
        return ('error', None, [f"Invalid elements in vector on line {node.lineno}"])
    
    def visit_MatrixIndex(self, node):
        type, dimensions, errors = self.visit(node.matrix)
        if errors:
            return ('error', None, errors)

        def correct_index(dimension, index):
            if dimension is None or index is None:
                return True
            return 0 <= index < dimension
        
        def correct_range(dimension, start, end):
            if dimension is None:
                return True
            if start is not None and end is not None:
                return 0 <= start <= end < dimension
            if start is not None:
                return 0 <= start < dimension
            if end is not None:
                return 0 <= end < dimension
            return True

        if type == 'vector':
            if len(node.indices) == 0:
                return ('error', None, [f"Vector indexing requires 1 index or range (got {len(node.indices)}) on line {node.lineno}"])

            errors = []
            if len(node.indices) > 1:
                errors.append(f"Vector indexing requires 1 index or range (got {len(node.indices)}) on line {node.lineno}")
            
            index_type, index_value, index_errors = self.visit(node.indices[0])

            if index_errors:
                return ('error', None, errors + index_errors)
            
            if index_type == "range":
                start, end = index_value
                if correct_range(dimensions, start, end):
                    return ('vector', (end - start + 1) if (start is not None and end is not None) else None, errors)
                else:
                    return ("error", None, errors + [f"Vector range [{start}:{end}] out of bounds for vector of length {dimensions} on line {node.lineno}"])
            elif index_type == 'int':
                if correct_index(dimensions, index_value):
                    return ('float', None, errors)
                else:
                    return ('error', None, errors + [f"Vector index {index_value} out of bounds for vector of length {dimensions} on line {node.lineno}"])
            else:
                return ('error', None, errors + [f"Vector index must be integer or range (got {index_type}) on line {node.lineno}"])
            
        elif type == 'matrix':
            if len(node.indices) == 0:
                return ('error', None, [f"Matrix indexing requires 2 indices or ranges (got {len(node.indices)}) on line {node.lineno}"])

            errors = []
            if len(node.indices) > 2:
                errors.append(f"Matrix indexing requires 2 indices or ranges (got {len(node.indices)}) on line {node.lineno}")

            index0_type, index0_value, index0_errors = self.visit(node.indices[0])
            index1_type, index1_value, index1_errors = self.visit(node.indices[1])

            if index0_errors and index1_errors:
                return ('error', None, errors + index0_errors + index1_errors)

            rows, cols = dimensions

            index_errors = []
            if not index0_errors:
                if index0_type == "range":
                    start, end = index0_value
                    if not correct_range(rows, start, end):
                        index_errors.append(f"Matrix range [{start}:{end}] out of bounds for matrix with {rows} rows on line {node.lineno}")
                elif index0_type == 'int':
                    if not correct_index(rows, index0_value):
                        index_errors.append(f"Matrix index {index0_value} out of bounds for matrix with {rows} rows on line {node.lineno}")
                else:
                    index_errors.append(f"Matrix index must be integer or range (got {index0_type}) on line {node.lineno}")

            if not index1_errors:
                if index1_type == "range":
                    start, end = index1_value
                    if not correct_range(cols, start, end):
                        index_errors.append(f"Matrix range [{start}:{end}] out of bounds for matrix with {cols} columns on line {node.lineno}")
                elif index1_type == 'int':
                    if not correct_index(cols, index1_value):
                        index_errors.append(f"Matrix index {index1_value} out of bounds for matrix with {cols} columns on line {node.lineno}")
                else:
                    index_errors.append(f"Matrix index must be integer or range (got {index1_type}) on line {node.lineno}")

            if index_errors or index0_errors or index1_errors:
                return ('error', None, errors + index0_errors + index1_errors + index_errors)

            if index0_type == 'int' and index1_type == 'int':
                return ('float', None, errors)
            
            if index0_type == 'range' and index1_type == 'int':
                start, end = index0_value
                return ('vector', (end - start + 1) if (start is not None and end is not None) else None, errors)
            
            if index0_type == 'int' and index1_type == 'range':
                start, end = index1_value
                return ('vector', (end - start + 1) if (start is not None and end is not None) else None, errors)

            if index0_type == 'range' and index1_type == 'range':
                start0, end0 = index0_value
                start1, end1 = index1_value
                dim0 = (end0 - start0 + 1) if (start0 is not None and end0 is not None) else None
                dim1 = (end1 - start1 + 1) if (start1 is not None and end1 is not None) else None
                return ('matrix', (dim0, dim1), errors)
        else:
            return ('error', None, [f"Indexing requires vector or matrix type (got {type}) on line {node.lineno}"])

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')