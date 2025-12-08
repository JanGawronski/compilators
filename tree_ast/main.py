import sys
from parser.parser import Mparser

import tree_ast.TreePrinter
from scanner.main import Scanner


def main():
    filename = sys.argv[1] if len(sys.argv) >= 2 else "tree_ast/examples/example3.m"

    with open(filename, "r") as file:
        text = file.read()

    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    if not ast:
        print(ast)
    else:
        print(ast.printTree())

if __name__ == "__main__":
    main()
