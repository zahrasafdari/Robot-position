from enum import Enum

class LexemeTypes(Enum):
    ASSIGN = ord(":")
    NUMBER = 256
    VARIABLE = 257
    KEY_WORD = 258
    END = 259

class Lexeme:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        return f"Lexeme({self.value},{self.type})"