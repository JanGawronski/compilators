import sys
from .parser import Mparser

from scanner.main import Scanner

if __name__ == "__main__":

    lexer = Scanner()
    parser = Mparser()

    filename = sys.argv[1] if len(sys.argv) > 1 else "parser/examples/example3.m"
    with open(filename, "r") as file:
        text = file.read()

    parser.parse(lexer.tokenize(text))
