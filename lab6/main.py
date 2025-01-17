import re
import sys

# Регулярные выражения для токенов
TOKEN_PATTERNS = [
    ("WHITESPACE", r"\s"),
    ("LINE_COMMENT", r"//.*"),
    ("BLOCK_COMMENT", r"\{(?:.|\n)*?\}"),  # Многострочные комментарии в одной строке
    ("START_BLOCK_COMMENT", r"\{\s*.*"),  # Многострочные комментарии
    ("END_BLOCK_COMMENT", r"(?:.|\n)*?\}"),  # Многострочные комментарии

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
    ("INTEGER", r"\b\d+\b"),
    ("FLOAT", r"^\d+(\.\d+)?([eE][+-]?\d+)?$"),  # Числа с плавающей точкой или экспонентой
    ("INTEGER", r"^(?<![\d.])\b\d+\b(?![\d.])$"),
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

class Token:
    def __init__(self, name, value, line_number, start_position):
        self.name = name
        self.value = value
        self.line_number = line_number
        self.start_position = start_position

class PascalLexer:
    def __init__(self, input_file_name):
        self.file = open(input_file_name, 'r', encoding='utf-8')
        self.line_number = 0
        self.current_line = ''
        self.current_words = []
        self.position_word = 0
        self.position = 0

    def next_line(self):
        self.current_line = next(self.file, None)  # Возвращает None на конце файла

        if not self.current_line  is None:
            self.current_line = self.current_line.strip()
            self.line_number += 1
            self.position = 0
            self.current_words = self.current_line.split(" ")
            self.position_word = 0

            return True
        return False

    def next_token(self):
        while True:
            if self.position_word >= len(self.current_words):
                if not self.next_line():
                    return None

            text = self.current_words[self.position_word]
            i = 0
            while i < len(TOKEN_PATTERNS):
                token_type, pattern = TOKEN_PATTERNS[i]
                regex = re.compile(pattern)
                match = regex.fullmatch(text)
                if match:
                    value = match.group(0)
                    start_position = self.position + 1
                    self.position += len(value)
                    self.position_word += 1

                    if token_type in ["START_BLOCK_COMMENT"]:
                        while True:
                            if self.position_word >= len(self.current_words) and not self.next_line():
                                return Token("BAD", value, self.line_number, start_position)
                            regex = re.compile(r"(?:.|\n)*?\}")
                            match = regex.match(self.current_words[self.position_word])
                            if match:
                                value += f"\n{match.group(0)}"
                                self.position_word += 1
                                return Token("BLOCK_COMMENT", value, self.line_number, start_position)
                            else:
                                value += f"\n{self.current_words[self.position_word]}"
                                self.position_word += 1
                    if token_type in ["LINE_COMMENT"]:
                        value += " ".join(self.current_words[self.position_word:])
                        self.next_line()
                        return Token(token_type, value, self.line_number, start_position)

                    if len(value) > 256:
                        return Token("BAD", value, self.line_number, start_position)
                    return Token(token_type, value, self.line_number, start_position)
                i += 1

            bad_char = self.current_words[self.position_word]
            start_position = self.position + len(bad_char)
            self.position_word += 1
            return Token("BAD", bad_char, self.line_number, start_position)

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
            if token.name == "LINE_COMMENT" or token.name == "BLOCK_COMMENT":
                continue

            print(f"{token.name} ({token.line_number}, {token.start_position}) \"{token.value}\"")
            output.write(f"{token.name} ({token.line_number}, {token.start_position}) \"{token.value}\"")

    lexer.close()

