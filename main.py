import sys
from parser import Mparser
import TreePrinter
from scanner import Scanner
from TypeChecker import TypeChecker
from Interpreter import Interpreter

def main():
    filename = sys.argv[1] if len(sys.argv) >= 2 else "examples/interpreter/matrix.m"
    with open(filename, "r") as file:
        text = file.read()

    ast = Mparser().parse(Scanner().tokenize(text))
    if ast:
        print(ast.printTree())

    errors = TypeChecker().visit(ast)
        
    if errors:
        print(*errors, sep="\n")
    else:
        Interpreter().visit(ast)

if __name__ == "__main__":
    main()
    
