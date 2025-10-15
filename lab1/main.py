# calclex.py

from sly import Lexer


class CalcLexer(Lexer):
    literals = {"+", "-", "*", "/", "(", ")", "{", "}", "[", "]", ":", ";", ",", "'", "=", "<", ">"}

    # Set of token names.   This is always required
    tokens = {
        "MPLUS",
        "MMINUS",
        "MMUL",
        "MDIV",
        "PLUSEQ",
        "MINEQ",
        "MULEQ",
        "DIVEQ",
        "LEQ",
        "GEQ",
        "NEQ",
        "EQ",
        "IF",
        "ELSE",
        "FOR",
        "WHILE",
        "BREAK",
        "CONTINUE",
        "RETURN",
        "EYE",
        "ZEROS",
        "ONES",
        "PRINT",
        "ID",
        "NUM",
        "FLOAT",
        "STRING",
    }

    # String containing ignored characters between tokens
    ignore = " \t\n"
    ignore_comment = r"\#.*"

    # Regular expression rules for tokens
    MPLUS = r"\.\+"
    MMINUS = r"\.-"
    MMUL = r"\.\*"
    MDIV = r"\./"
    PLUSEQ = r"\+="
    MINEQ = r"-="
    MULEQ = r"\*="
    DIVEQ = r"/="
    LEQ = "<="
    GEQ = ">="
    NEQ = "!="
    EQ = "=="

    NUM = r"\d+"
    FLOAT = r"\d+\.\d+"
    STRING = r'"[^"]*"'

    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["if"] = "IF"
    ID["else"] = "ELSE"
    ID["for"] = "FOR"
    ID["while"] = "WHILE"
    ID["break"] = "BREAK"
    ID["continue"] = "CONTINUE"
    ID["return"] = "RETURN"
    ID["eye"] = "EYE"
    ID["zeros"] = "ZEROS"
    ID["ones"] = "ONES"
    ID["print"] = "PRINT"


if __name__ == "__main__":
    # Bardziej rozbudowany przykład do testowania
    data = """
# To jest komentarz, ktory powinien zostac zignorowany
A = zeros(5); # inicjalizacja macierzy
B = A'; # transpozycja

if (x <= 5) {
    y = x * 2.5;
    print "Wartosc y to:", y;
}
"""

    print("INPUT:\n", data)
    lexer = CalcLexer()

    # Pętla iterująca przez wszystkie tokeny znalezione w danych
    for tok in lexer.tokenize(data):
        print(f"type={tok.type:<10} value={tok.value!r:<20} lineno={tok.lineno}")
