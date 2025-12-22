import sys
from parser import Mparser
import TreePrinter
from scanner import Scanner
from TypeChecker import TypeChecker

def main():
    filename = sys.argv[1] if len(sys.argv) >= 2 else "examples/checker/opers.m"

    with open(filename, "r") as file:
        text = file.read()

    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    if not ast:
        print(ast)
    else:
        print(ast.printTree())
        TypeChecker().visit(ast)

if __name__ == "__main__":
    main()
