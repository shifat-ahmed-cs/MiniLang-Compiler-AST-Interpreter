"""
Handwritten Lexer for MiniLang.
"""
from enum import Enum, auto
from typing import List, NamedTuple

class TokenType(Enum):
    LET = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    EOF = auto()

class Token(NamedTuple):
    type: TokenType
    value: str
    line: int

KEYWORDS = {
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT
}

class Lexer:
    def __init__(self, source: str):
        self.src = source
        self.pos = 0
        self.line = 1

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.src):
            ch = self.src[self.pos]

            if ch in ' \t\r':
                self.pos += 1
            elif ch == '\n':
                self.line += 1
                self.pos += 1
            elif ch == '#':  # Comment
                while self.pos < len(self.src) and self.src[self.pos] != '\n':
                    self.pos += 1
            elif ch.isdigit():
                num_str = ""
                while self.pos < len(self.src) and (self.src[self.pos].isdigit() or self.src[self.pos] == '.'):
                    num_str += self.src[self.pos]
                    self.pos += 1
                tokens.append(Token(TokenType.NUMBER, num_str, self.line))
            elif ch.isalpha() or ch == '_':
                ident = ""
                while self.pos < len(self.src) and (self.src[self.pos].isalnum() or self.src[self.pos] == '_'):
                    ident += self.src[self.pos]
                    self.pos += 1
                t_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
                tokens.append(Token(t_type, ident, self.line))
            elif ch == '=':
                if self.pos + 1 < len(self.src) and self.src[self.pos + 1] == '=':
                    tokens.append(Token(TokenType.EQUAL_EQUAL, "==", self.line))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.EQUAL, "=", self.line))
                    self.pos += 1
            elif ch == '+':
                tokens.append(Token(TokenType.PLUS, "+", self.line))
                self.pos += 1
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, "-", self.line))
                self.pos += 1
            elif ch == '*':
                tokens.append(Token(TokenType.STAR, "*", self.line))
                self.pos += 1
            elif ch == '/':
                tokens.append(Token(TokenType.SLASH, "/", self.line))
                self.pos += 1
            elif ch == '<':
                tokens.append(Token(TokenType.LESS, "<", self.line))
                self.pos += 1
            elif ch == '>':
                tokens.append(Token(TokenType.GREATER, ">", self.line))
                self.pos += 1
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, "(", self.line))
                self.pos += 1
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ")", self.line))
                self.pos += 1
            elif ch == '{':
                tokens.append(Token(TokenType.LBRACE, "{", self.line))
                self.pos += 1
            elif ch == '}':
                tokens.append(Token(TokenType.RBRACE, "}", self.line))
                self.pos += 1
            elif ch == ';':
                tokens.append(Token(TokenType.SEMICOLON, ";", self.line))
                self.pos += 1
            else:
                self.pos += 1
        tokens.append(Token(TokenType.EOF, "", self.line))
        return tokens
