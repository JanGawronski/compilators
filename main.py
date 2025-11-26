import sys
from parser.parser import Mparser

from scanner.main import Scanner


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    # Create lexer and parser
    lexer = Scanner()
    parser = Mparser()

    # Parse the input
    try:
        ast = parser.parse(lexer.tokenize(text))

        # If parsing was successful and AST was created, print it
        if ast is not None:
            print(ast.printTree())
    except Exception as e:
        print(f"Error during parsing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
