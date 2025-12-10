from sly import Lexer


class Scanner(Lexer):
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

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"({self.lineno}): Illegal character {t.value[0]}")
        self.index += 1

    ignore = " \t"
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

    FLOAT = r"(\d+\.\d*|\.\d+)([Ee][+-]?\d+)?"
    INT = r"\d+"
    @_(r'"[^"]*"')
    def STRING(self, t):
        self.lineno += t.value.count("\n")
        return t

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
    data = open("./scanner/examples/example0.m").read()

    print("INPUT:\n", data)
    lexer = Scanner()

    for tok in lexer.tokenize(data):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
