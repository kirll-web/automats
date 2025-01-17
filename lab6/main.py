import string
import sys


class Token:
    def __init__(self, line, column, value, token_type):
        self.line = line
        self.column = column
        self.value = value
        self.token_type = token_type

    def __str__(self):
        return f"{self.token_type} ({self.line}, {self.column}) \"{self.value}\""

class StringToken(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "STRING")

class Keyword(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "PROGRAM" if value == "program" else "KEYWORD")


class Identifier(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "IDENTIFIER")


class IntegerToken(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "INTEGER")

class FloatToken(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "FLOAT")

class Operator(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "OPERATOR")

class Bad(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value, "Bad")

class Punctuation(Token):
    def __init__(self, line, column, value):
        super().__init__(line, column, value,
                         "SEMICOLON" if value == ";" else "COLON" if value == ":" else "PUNCTUATION")


class EndOfFile(Token):
    def __init__(self, line, column):
        super().__init__(line, column, "", "EOF")

    def __str__(self):
        return f"EOF ({self.line}, {self.column})"


class Lexer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r')  # Открываем файл для чтения
        self.line = 1
        self.column = 0
        self.current_char = None
        self.buffer = ''  # Буфер для текущей строки
        self.advance()  # Инициализируем первый символ

        # Ключевые слова Pascal
        self.keywords = {
            "program", "begin", "end", "var", "if", "then", "else", "for", "while", "array"
        }

        # Операторы и знаки препинания
        self.operators = set(["+", "-", "*", "/", ":=", "=", "<>", "<", ">", "<=", ">="])
        self.punctuations = set([";", ".", "(", ")", ":"])

    def advance(self):
        """Продвигаемся к следующему символу, включая чтение из файла"""
        if self.column < len(self.buffer):
            self.current_char = self.buffer[self.column]
            self.column += 1
        else:
            self.buffer = next(self.file, None)  # Читаем следующую строку
            if self.buffer is None:  # EOF
                self.current_char = None
                self.file.close()  # Закрываем файл при достижении конца
            else:
                self.line += 1
                self.column = 0
                self.advance()  # Читаем первый символ новой строки

    def skip_whitespace(self):
        """Пропускаем пробелы и переносы строк"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_identifier(self):
        """Читаем идентификатор или ключевое слово"""
        start_column = self.column
        value = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char
            self.advance()
        return Identifier(self.line, start_column, value)

    def parse_number(self):
        """Читаем целое число или число с плавающей запятой"""
        start_column = self.column
        value = ''
        has_dot = False
        has_exponent = False

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char in '.eE+-'):
            if self.current_char == '.':
                if has_dot:
                    break
                has_dot = True
            elif self.current_char in 'eE':
                if has_exponent:
                    break
                has_exponent = True
            elif self.current_char in '+-' and not has_exponent:
                break
            value += self.current_char
            self.advance()

        if has_dot or has_exponent:
            return FloatToken(self.line, start_column, value)
        else:
            return IntegerToken(self.line, start_column, int(value))

    def parse_string(self):
        """Читаем строковый литерал, заключенный в кавычки"""
        start_column = self.column
        value = ''
        self.advance()  # Пропускаем начальную кавычку

        while self.current_char is not None:
            if self.current_char == '"':
                self.advance()  # Пропускаем закрывающую кавычку
                return StringToken(self.line, start_column, value)
            value += self.current_char
            self.advance()

        raise ValueError(f"Unterminated string at line {self.line}, column {start_column}")

    def next_token(self):
        """Возвращаем следующий токен"""
        self.skip_whitespace()

        if self.current_char is None:
            return EndOfFile(self.line, self.column)

        if self.current_char.isalpha():
            return self.parse_identifier()

        if self.current_char.isdigit():
            return self.parse_number()

        if self.current_char == '"':
            return self.parse_string()

        if self.current_char in ''.join(self.operators):
            return self.parse_operator()

        if self.current_char in self.punctuations:
            return self.parse_punctuation()

        value = self.current_char
        self.advance()
        return Bad(self.line, self.column, value)

    def parse_operator(self):
        """Читаем оператор"""
        start_column = self.column
        value = self.current_char
        self.advance()
        return Operator(self.line, start_column, value)

    def parse_punctuation(self):
        """Читаем пунктуацию"""
        start_column = self.column
        value = self.current_char
        self.advance()
        return Punctuation(self.line, start_column, value)


def main():
    file_path = 'p1.pas'  # Имя файла с кодом на Pascal
    lexer = Lexer(file_path)

    token = lexer.next_token()
    while not isinstance(token, EndOfFile):
        print(token)
        token = lexer.next_token()

if __name__ == "__main__":
    main()