import re
import sys
from turtledemo.penrose import start

# Регулярные выражения для токенов
TOKEN_PATTERNS = {
    "WHITESPACE": r"\s",
    "LINE_COMMENT": r"//.*",
    "BLOCK_COMMENT": r"\{(?:.|\n)*?\}",  # Многострочные комментарии в одной строке
    "START_BLOCK_COMMENT": r"\{\s*.*",  # Многострочные комментарии
    "END_BLOCK_COMMENT": r"(?:.|\n)*?\}",  # Многострочные комментарии
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "STRING": r"'(?:[^'\\]|\\.)*'",
    "INTEGER": r"^(?<![\d.])\b\d+\b(?![\d.])$",  # Окончательная версия для целых чисел
    "FLOAT":  r"^\d+\.\d+([eE][+-]?\d+)?$|^\d+[eE][+-]?\d+$",  # Числа с плавающей точкой или экспонентой
    "PLUS": r"\+",
    "MINUS": r"-",
    "DIVIDE": r"/",
    "SEMICOLON": r";",
    "COMMA": r",",
    "LEFT_PAREN": r"\(",
    "RIGHT_PAREN": r"\)",
    "LEFT_BRACKET": r"\[",
    "RIGHT_BRACKET": r"\]",
    "EQ": r"=",
    "GREATER": r">",
    "LESS": r"<",
    "LESS_EQ": r"<=",
    "GREATER_EQ": r">=",
    "NOT_EQ": r"<>",
    "COLON": r":",
    "ASSIGN": r":=",
    "DOT": r"\.",
}

KEYS_PATTERNS = {
    "ARRAY": r"(?i)\bARRAY\b",
    "BEGIN": r"(?i)\bBEGIN\b",
    "ELSE": r"(?i)\bELSE\b",
    "END": r"(?i)\bEND\b",
    "IF": r"(?i)\bIF\b",
    "OF": r"(?i)\bOF\b",
    "OR": r"(?i)\bOR\b",
    "PROGRAM": r"(?i)\bPROGRAM\b",
    "PROCEDURE": r"(?i)\bPROCEDURE\b",
    "THEN": r"(?i)\bTHEN\b",
    "TYPE": r"(?i)\bTYPE\b",
    "VAR": r"(?i)\bVAR\b",
}

delimeters = {"\"", " ",  "(", ")", "+", "-", "\t","\n", ";", ":", ",", ".", "[", "]", "{", "}", "*", "/", "'",  "\xa0"}

class Token:
    def __init__(self, name,  line_number, start_position, value,):
        self.name = name
        self.value = value
        self.line_number = line_number
        self.start_position = start_position

class PascalLexer:
    def __init__(self, input_file_name):
        self.file = open(input_file_name, 'r', encoding='utf-8')
        self.line_number = 0
        self.current_line = ''
        self.position = 0
        self.line = 1
        self.current_char = None
        self.buffer = ''  # Буфер для текущей строки
        self.next_line()  # Инициализируем первый символ
        self.current_value = None
        self.start_position = 0

    def next_line(self):
        self.current_line = next(self.file, None)  # Возвращает None на конце файла

        if not self.current_line is None:
            self.current_line = self.current_line.strip().replace( "\xa0", " ")
            self.line_number += 1
            self.position = 0

            return True
        self.current_line = ""
        return False

    def parse_block_comment(self):
        self.current_value = self.current_line[self.position]
        self.start_position = self.position
        while True:
            self.position += 1
            if self.position >= len(self.current_line) and not self.next_line():
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("Bad", self.line_number, start, value)

            if self.position < len(self.current_line):
                self.current_value += self.current_line[self.position]
                if self.current_line[self.position] == "}":
                    value = self.current_value
                    self.current_value = None
                    start = self.start_position
                    self.start_position = self.position
                    self.position +=1
                    return Token("BLOCK_COMMENT", self.line_number, start, value)

    def parse_string(self):
        self.current_value = self.current_line[self.position]
        self.start_position = self.position
        while True:
            self.position += 1
            if self.position >= len(self.current_line):
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("Bad", self.line_number, start, value)

            self.current_value += self.current_line[self.position]
            if self.current_line[self.position] == "\"":
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                self.position += 1
                return Token("STRING", self.line_number, start, value)

    def parse_divide(self):
        self.current_value = self.current_line[self.position]
        self.start_position = self.position
        self.position += 1
        if self.position >= len(self.current_line):
            value = self.current_value
            self.current_value = None
            start = self.start_position
            self.start_position = self.position
            return Token("DIVIDE", self.line_number, start, value)

        self.current_value += self.current_line[self.position]

        if self.current_value == "//":
            while self.position < len(self.current_line) - 1:
                self.position += 1
                self.current_value += self.current_line[self.position]
            value = self.current_value
            self.current_value = None
            start = self.start_position
            self.start_position = self.position
            self.position += 1
            return Token("LINE_COMMENT", self.line_number, start, value)
        else:
            value = self.current_value[0: -1]
            self.current_value = None
            start = self.start_position
            self.start_position = self.position
            self.position -= 1
            return Token("DIVIDE", self.line_number, start, value)

    def parse_digit(self):
        self.current_value = self.current_line[self.position]
        self.start_position = self.position
        regexF = re.compile(TOKEN_PATTERNS["FLOAT"])
        regexI = re.compile(TOKEN_PATTERNS["INTEGER"])

        while (regexI.fullmatch(self.current_value) or regexF.fullmatch(self.current_value)) or self.current_value[
            -1] == "." or self.current_value[-1] == "e" or "e-" in self.current_value:
            self.position += 1
            if self.position >= len(self.current_line):

                match = regexF.fullmatch(self.current_value)
                if match:
                    value = self.current_value
                    self.current_value = None
                    start = self.start_position
                    self.start_position = self.position



                    return Token("FLOAT", self.line_number, start, value)

                match = regexI.fullmatch(self.current_value)
                if match:
                    value = self.current_value
                    self.current_value = None
                    start = self.start_position
                    self.start_position = self.position
                    return Token("INTEGER", self.line_number, start, value)
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("Bad", self.line_number, start, value)

            if self.current_line[self.position] == ".":
                if self.position + 1 < len(self.current_line) and self.current_line[self.position + 1] == ".":
                    # Обработка ".."
                    if self.current_value.isdigit():
                        match = regexF.fullmatch(self.current_value)
                        if match:
                            value = self.current_value
                            self.current_value = None
                            start = self.start_position
                            self.start_position = self.position
                            if len(value) > 16:
                                return Token("BAD", self.line_number, start, value)
                            return Token("FLOAT", self.line_number, start, value)

                        match = regexI.fullmatch(self.current_value)
                        if match:
                            value = self.current_value
                            self.current_value = None
                            start = self.start_position
                            self.start_position = self.position
                            if len(value) > 16:
                                return Token("Bad", self.line_number, start, value)
                            return Token("INTEGER", self.line_number, start, value)
                        value = self.current_value
                        self.current_value = None
                        start = self.start_position
                        self.start_position = self.position
                        return Token("BAD", self.line_number, start, value)
                    else:
                        value = self.current_value
                        self.current_value = None
                        start = self.start_position
                        self.start_position = self.position
                        return Token("BAD", self.line_number, start, value)
                elif not self.current_value.isdigit():
                    # Если не число перед ".", то ошибка
                    while self.position < len(self.current_line) and self.current_line[self.position] not in delimeters:
                        self.position += 1
                        if self.position < len(self.current_line):
                            self.current_value += self.current_line[self.position]
                    self.current_value += self.current_line[self.position]
                    value = self.current_value
                    self.current_value = None
                    start = self.start_position
                    self.start_position = self.position
                    self.position += 1
                    return Token("Bad", self.line_number, start, value)

            self.current_value += self.current_line[self.position]

        if self.current_value[-1] in delimeters:
            self.current_value = self.current_value[0:-1]

            match = regexF.fullmatch(self.current_value)
            if match:
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("FLOAT", self.line_number, start, value)

            match = regexI.fullmatch(self.current_value)
            if match:
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("INTEGER", self.line_number, start, value)
            self.current_value += self.current_line[self.position]

        while self.position < len(self.current_line) - 1 and self.current_line[self.position] not in delimeters or \
                self.current_line[self.position] == ".":
            self.position += 1
            self.current_value += self.current_line[self.position]

        if self.current_line[self.position] in delimeters:
            self.position -= 1
            self.current_value = self.current_value[0: -1]
        value = self.current_value
        self.current_value = None
        start = self.start_position
        self.start_position = self.position
        return Token("Bad", self.line_number, start, value)

    def parse_identifier(self):
        self.current_value = self.current_line[self.position]
        self.start_position = self.position
        regex = re.compile(TOKEN_PATTERNS["IDENTIFIER"])

        while regex.fullmatch(self.current_value):
            self.position += 1
            if self.position >= len(self.current_line):
                value = self.current_value
                self.current_value = None
                start = self.start_position
                self.start_position = self.position
                return Token("IDENTIFIER", self.line_number, start, value)

            self.current_value += self.current_line[self.position]

        if self.current_value[-1] in delimeters:
            self.current_value = self.current_value[0:-1]

            for pattern in KEYS_PATTERNS:
                regexK = re.compile(KEYS_PATTERNS[pattern], re.IGNORECASE)
                if regexK.fullmatch(self.current_value):
                    value = self.current_value
                    self.current_value = None
                    start = self.start_position
                    self.start_position = self.position
                    return Token(pattern, self.line_number, start, value)

            value = self.current_value
            self.current_value = None
            start = self.start_position
            self.start_position = self.position
            if value.isidentifier() and regex.fullmatch(value):
                return Token("IDENTIFIER", self.line_number, start, value)
            else:  return Token("BAD", self.line_number, start, value)

        while self.position < len(self.current_line)  and self.current_line[self.position] not in delimeters:
            self.position += 1
            if self.position < len(self.current_line) :
                self.current_value += self.current_line[self.position]

        value = self.current_value
        self.current_value = None
        start = self.start_position
        self.start_position = self.position
        return Token("Bad", self.line_number, start, value)


    def next_token(self):
        while True:
            while self.position >= len(self.current_line):
                if not self.next_line():
                    return None



                #TODO ОБРАБОТАТЬ 123.123.123
            if self.current_line[self.position] == "{":
                return self.parse_block_comment()

            if self.current_line[self.position].isspace():
                self.position += 1
                continue

            if self.current_line[self.position].isdigit():
                 return self.parse_digit()

            if self.current_line[self.position].isalpha():
                return self.parse_identifier()

            if self.current_line[self.position] == '"':
                return self.parse_string()

            if self.current_line[self.position] == '+':
                pos = self.position
                self.position += 1
                return Token("PLUS", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '-':
                pos = self.position
                self.position += 1
                return Token("MINUS", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '/':
                return self.parse_divide()

            if self.current_line[self.position] == ';':
                pos = self.position
                self.position += 1
                return Token("SEMICOLON", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == ',':
                pos = self.position
                self.position += 1
                return Token("COMMA", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '(':
                pos = self.position
                self.position += 1
                return Token("LEFT_PAREN", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == ')':
                pos = self.position
                self.position += 1
                return Token("RIGHT_PAREN", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '[':
                pos = self.position
                self.position += 1
                return Token("LEFT_BRACKET", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == ']':
                pos = self.position
                self.position += 1
                return Token("RIGHT_BRACKET", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '=':
                pos = self.position
                self.position += 1
                return Token("EQ", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '>':
                pos = self.position
                self.position += 1
                return Token("GREATER", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '<':
                pos = self.position
                self.position += 1
                return Token("LESS", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position:self.position + 2] == '<=':
                pos = self.position
                self.position += 2
                return Token("LESS_EQ", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position:self.position + 2] == '>=':
                pos = self.position
                self.position += 2
                return Token("GREATER_EQ", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position:self.position + 2] == '<>':
                pos = self.position
                self.position += 2
                return Token("NOT_EQ", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == ':':
                if self.position + 1 < len(self.current_line) and self.current_line[self.position + 1] == '=':
                    pos = self.position
                    self.position += 2
                    return Token("ASSIGN", self.line_number, pos, self.current_line[pos] +  self.current_line[pos+1])
                else:
                    pos = self.position
                    self.position += 1
                    return Token("COLON", self.line_number, pos, self.current_line[pos])

            if self.current_line[self.position] == '.':
                pos = self.position
                self.position += 1
                return Token("DOT", self.line_number, pos, self.current_line[pos])



            self.position += 1 #fixme mock





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
            # if token.name == "LINE_COMMENT" or token.name == "BLOCK_COMMENT":
            #     continue

            print(f"{token.name} ({token.line_number}, {token.start_position}) \"{token.value}\"")
            output.write(f"{token.name} ({token.line_number}, {token.start_position}) \"{token.value}\"")
    lexer.close()

