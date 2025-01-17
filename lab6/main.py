import re
import sys

# Регулярные выражения для токенов
TOKEN_PATTERNS = [
    ("WHITESPACE", r"\s"),
    ("LINE_COMMENT", r"//.*"),
    ("START_BLOCK_COMMENT", r"\{\s*.*"),  # Многострочные комментарии
    ("END_BLOCK_COMMENT", r"(?:.|\n)*?\}"),  # Многострочные комментарии
    ("BLOCK_COMMENT", r"\{(?:.|\n)*?\}"),  # Многострочные комментарии в одной строке
    ("ARRAY", r"(?i)\bARRAY\b"),
    ("BEGIN", r"(?i)\bBEGIN\b"),
    ("ELSE", r"(?i)\bELSE\b"),
    ("END", r"(?i)\bEND\b"),
    ("IF", r"(?i)\bIF\b"),
    ("OF", r"(?i)\bOF\b"),
    ("OR", r"(?i)\bOR\b"),
    ("PROGRAM", r"(?i)\bPROGRAM\b"),
    ("PROCEDURE", r"(?i)\bPROCEDURE\b"),
    ("THEN", r"(?i)\bTHEN\b"),
    ("TYPE", r"(?i)\bTYPE\b"),
    ("VAR", r"(?i)\bVAR\b"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("STRING", r"'(?:[^'\\]|\\.)*'"),
    ("FLOAT", r"\b\d+\.\d+\b"),
    ("INTEGER", r"\b\d+\b"),
    ("MULTIPLICATION", r"\*"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("DIVIDE", r"/"),
    ("SEMICOLON", r";"),
    ("COMMA", r","),
    ("LEFT_PAREN", r"\("),
    ("RIGHT_PAREN", r"\)"),
    ("LEFT_BRACKET", r"\["),
    ("RIGHT_BRACKET", r"\]"),
    ("EQ", r"="),
    ("GREATER", r">"),
    ("LESS", r"<"),
    ("LESS_EQ", r"<="),
    ("GREATER_EQ", r">="),
    ("NOT_EQ", r"<>"),
    ("COLON", r":"),
    ("ASSIGN", r":="),
    ("DOT", r"\."),

]

class PascalLexer:
    def __init__(self, input_file):
        self.file = open(input_file, 'r', encoding='utf-8')
        self.line_number = 0
        self.current_line = ''
        self.position = 0

    def next_line(self):
        self.current_line = self.file.readline()
        if self.current_line:
            self.line_number += 1
            self.position = 0
            return True
        return False

    def next_token(self):
        while True:
            if self.position >= len(self.current_line):
                if not self.next_line():
                    return None

            text = self.current_line[self.position:]
            i = 0
            while i < len(TOKEN_PATTERNS):
                token_type, pattern = TOKEN_PATTERNS[i]
                regex = re.compile(pattern)
                match = regex.match(text)
                if match:
                    value = match.group(0)
                    start_position = self.position + 1
                    self.position += len(value)

                    if token_type in ["WHITESPACE"]:
                        text = text[1:]
                        i = 0
                        continue
                    if token_type in ["START_BLOCK_COMMENT"]:
                        while True:
                            if not self.next_line():
                                return f"BAD: ({self.line_number},{start_position}) \"{value}\""
                            regex = re.compile(r"(?:.|\n)*?\}")
                            match = regex.match(self.current_line)
                            if match:
                                value += match.group(0)
                                self.position += len(match.group(0))
                                return f"BLOCK_COMMENT ({self.line_number},{start_position}) \"{value}\""
                            else:
                                value += self.current_line
                    if len(value) > 256:
                        return f"BAD: ({self.line_number},{start_position}) \"{value}\""
                    return f"{token_type} ({self.line_number},{start_position}) \"{value}\""
                i += 1

            if self.position < len(self.current_line):
                bad_char = self.current_line[self.position]
                start_position = self.position + 1
                self.position += 1
                return f"BAD: ({self.line_number},{start_position}) \"{bad_char}\""

    def close(self):
        self.file.close()
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python PascalLexer.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    lexer = PascalLexer(input_file)

    with open(output_file, 'w', encoding='utf-8') as output:
        while True:
            token = lexer.next_token()
            if token is None:
                break
            print(token)
            output.write(token + '\n')

    lexer.close()

