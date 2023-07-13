
# the error class inherit from Exception class which is a existed python class.

class ErrorFrame(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def RaiseError(self):
        print("\n" + self.__class__.__name__ + " : " + self.message + "\n")
        exit()


class CharError(ErrorFrame):
    def __init__(self, lexical_analyzer):
        line = lexical_analyzer.line_num + 1
        character_number = (
            lexical_analyzer.file_input.pivot - lexical_analyzer.last_line_start
        )
        message = f"Character '{lexical_analyzer.file_input.char()}' is invalid in line {line}, number {character_number}"
        super().__init__(message)


class TokenError(ErrorFrame):
    def __init__(self, guess, lexical_analyzer):
        line = lexical_analyzer.line_num + 1
        character_number = (
            lexical_analyzer.file_input.pivot
            -
            lexical_analyzer.last_line_start
        )
        message = f"could not recognize token in line {line}, number {character_number}, do you mean '{guess}' ?"
        super().__init__(message)


class SyntaxError(ErrorFrame):
    def __init__(self, syntax_analyzer, description=""):
        line = syntax_analyzer.analyzer.line_num + 1
        character_number = (
            syntax_analyzer.analyzer.file_input.pivot
            - syntax_analyzer.analyzer.last_line_start
        )
        message = f"invalid '{syntax_analyzer.look_ahead.value}' token in line {line}, number {character_number}\n{description}"
        super().__init__(message)


class SemanticError(ErrorFrame):
    pass