from sly import Lexer


class CalcLexer(Lexer):
    literals = {"+", "-", "*", "/", "(", ")", "{", "}", "[", "]", ":", ";", ",", "'", "=", "<", ">"}

    tokens = {
        "DOTADD",
        "DOTSUB",
        "DOTMUL",
        "DOTDIV",
        "ADDASSIGN",
        "SUBASSIGN",
        "MULASSIGN",
        "DIVASSIGN",
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
        "INT",
        "FLOAT",
        "STRING",
    }

    ignore = " \t\n"
    ignore_comment = r"\#.*"

    DOTADD = r"\.\+"
    DOTSUB = r"\.-"
    DOTMUL = r"\.\*"
    DOTDIV = r"\./"
    ADDASSIGN = r"\+="
    SUBASSIGN = r"-="
    MULASSIGN = r"\*="
    DIVASSIGN = r"/="
    LEQ = "<="
    GEQ = ">="
    NEQ = "!="
    EQ = "=="

    INT = r"\d+"
    FLOAT = r"\d*\.\d*"
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
    data = open("./lab1/examples/example0.m").read()

    print("INPUT:\n", data)
    lexer = CalcLexer()

    for tok in lexer.tokenize(data):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
