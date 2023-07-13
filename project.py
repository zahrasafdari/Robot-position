from Error_handling import CharError,SyntaxError,SemanticError,TokenError
from lexeme_manager import Lexeme, LexemeTypes
import math
import string
import matplotlib.pyplot as plt
from stmt_coord import coordinates, statements, Nonefunc
from file_manager import FileInput

class LexicalAnalyzer:
    def __init__(self):
        self.file_input = FileInput()
        self.first_lexeme = 0
        self.line_num = 0
        self.last_line_start = 0
        
    #This function get a lexeme
    def variable_lexeme(self):
        self.first_lexeme = self.file_input.pivot
        while True:
            if (
                self.file_input.next()
                not in string.ascii_letters + string.digits
            ):
                value = self.file_input.input[
                    self.first_lexeme: self.file_input.pivot
                ]
                self.file_input.retract()

                if statements.get(value.lower()):
                    return Lexeme(value, LexemeTypes.KEY_WORD)
                return Lexeme(value, LexemeTypes.VARIABLE)
    #This function get a lexeme
    def number_lexeme(self):
        self.first_lexeme = self.file_input.pivot
        while True:
            if self.file_input.next() not in string.digits:
                value = self.file_input.input[
                    self.first_lexeme: self.file_input.pivot
                ]
                self.file_input.retract()
                return Lexeme(value, LexemeTypes.NUMBER)
                   
    def scan_one_comment(self):
        if self.file_input.next() != "/":
            TokenError("//", self).RaiseError()
        while True:
            if self.file_input.next() == "\n":
                return self.file_input.retract()

    def scan_multiple_comment(self):
        while True:
            if self.file_input.next() == "}":
                return
    #This function gets a Lexeme
    def get_token(self):
        while True:
            if self.file_input.endchar():
                return Lexeme(Nonefunc, LexemeTypes.END)

            char = self.file_input.next()

            if char == ":":
                return Lexeme(char, LexemeTypes.ASSIGN)
            elif char == "/":
                self.scan_one_comment()
            elif char == "{":
                self.scan_multiple_comment()
            elif char in string.ascii_letters:
                return self.variable_lexeme()
            elif char in "+" + "-" + string.digits:
                return self.number_lexeme()
            elif char in string.whitespace:
                if char == "\n":
                    self.line_num += 1
                    self.last_line_start = self.file_input.pivot
            else:
                CharError(self).RaiseError()


class SyntaxAnalyzerBase:
    def __init__(self, lexical_analyzer=None, look_ahead=None):
        self.analyzer = lexical_analyzer
        if not lexical_analyzer:
            self.analyzer = LexicalAnalyzer()
        self.look_ahead = look_ahead

    def match(self, lex_type, value=None, raise_error=False):
        self.next()
        if self.look_ahead.type != lex_type:
            args = (
                self,
                f"Expected {lex_type.name } but got { self.look_ahead.type.name}",
            )
            if raise_error:
                raise SyntaxError(*args)
            else:
                SyntaxError(*args).throw()
        if value and self.look_ahead.value != value:
            args = (
                self,
                f"Expected {lex_type.name } but got { self.look_ahead.type.name}",
            )
            if raise_error:
                raise SyntaxError(*args)
            else:
                SyntaxError(*args).throw()

    def next(self):
        self.look_ahead = self.analyzer.get_token()


class RobotPathAnalyzer(SyntaxAnalyzerBase):
    def check_requirements(self):
        for bound in coordinates:
            if not bound in statements:
                SemanticError(
                    f"'{bound}' variable is required for parsing robot path"
                ).throw()

        if not statements["uz"] > statements["lz"]:
            SemanticError("uz have to be bigger than lz").throw()

        if not statements["uy"] > statements["ly"]:
            SemanticError("uy have to be bigger than ly").throw()

        if not statements["ux"] > statements["lx"]:
            SemanticError("ux have to be bigger than lx").throw()

        if not (statements["lx"] <= statements["ox"] <= statements["ux"]):
            SemanticError("ox is not in x bound").throw()
        if not (statements["ly"] <= statements["oy"] <= statements["uy"]):
            SemanticError("oy is not in y bound").throw()
        if not (statements["lz"] <= statements["oz"] <= statements["uz"]):
            SemanticError("oz is not in z bound").throw()

    def check_path(self, x, y, z):
        if (
            (x, y, z) in statements.get("n", [])
            or not (statements["lx"] <= x <= statements["ux"])
            or not (statements["ly"] <= y <= statements["uy"])
            or not (statements["lz"] <= z <= statements["uz"])
        ):
            raise SyntaxError(self)

    def move(self, x_move, y_move, z_move):
        self.check_path(self.x + x_move, self.y + y_move, self.z + z_move)
        self.ax.quiver(self.x, self.y, self.z, x_move,
                       y_move, z_move, color="#666b6a")
        
        self.x += x_move
        self.y += y_move
        self.z += z_move
        print(f"({self.x}, {self.y}, {self.z})")

    def parse_movement(self):
        try:
            self.match(LexemeTypes.KEY_WORD, raise_error=True)
            if self.look_ahead.value.lower() == "end":
                print(f"L={self.count -1}")
                distance = math.sqrt(
                    (self.x - statements["ox"]) ** 2
                    + (self.y - statements["oy"]) ** 2
                    + (self.z - statements["oz"]) ** 2
                )
                print(f"D={distance}")
                self.ax.scatter(self.x, self.y, self.z, color="black")
                loc = 'left'
                self.ax.set_title( f"L={self.count -1}\nD={distance}", loc=loc)
                self.ax.quiver(
                    statements["ox"],
                    statements["oy"],
                    statements["oz"],
                    self.x - statements["ox"],
                    self.y - statements["oy"],
                    self.z - statements["oz"],
                    color="#003B36",
                )

                return

            elif self.look_ahead.value.lower() == "west":
                self.move(statements["west"], 0, 0)

            elif self.look_ahead.value.lower() == "east":
                self.move(statements["east"], 0, 0)

            elif self.look_ahead.value.lower() == "north":
                self.move(0, statements["north"], 0)

            elif self.look_ahead.value.lower() == "south":
                self.move(0, statements["south"], 0)

            elif self.look_ahead.value.lower() == "up":
                self.move(0, 0, statements["up"])

            elif self.look_ahead.value.lower() == "down":
                self.move(0, 0, statements["down"])

            self.count += 1
        except SyntaxError:
            # when the robot hits the obstacle raise Error and show the relative statement number.
            print(f"Error in instr {self.count}")
        self.parse_movement()

    def parse(self):
        font = {
            'size': 20
        }
        self.check_requirements()
        self.count = 1
        self.x = statements["ox"]
        self.y = statements["oy"]
        self.z = statements["oz"]

        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#AFD0BF')
        self.ax = plt.axes(projection="3d")
        self.ax.set_facecolor("#AFD0BF")
        self.ax.set_xlabel("X", **font)
        # self.ax.subplots_adjust(left=0.5, right=0.5)
        self.ax.set_ylabel("Y", **font)
        self.ax.set_zlabel("Z", **font)
        self.ax.view_init(10, 10)
        for obstacle_position in statements.get("n", []):
            self.ax.scatter(*obstacle_position, color="#B10F2E")

        print(f"({self.x}, {self.y}, {self.z})")

        self.parse_movement()

        plt.show()


class SyntaxAnalyzer(SyntaxAnalyzerBase):
    def parse_list_variable(self, variable_lexeme):
        statements[variable_lexeme.value.lower()] = []
        n = int(self.look_ahead.value)
        for _ in range(n):
            self.match(LexemeTypes.NUMBER)
            x = self.look_ahead
            self.match(LexemeTypes.NUMBER)
            y = self.look_ahead
            self.match(LexemeTypes.NUMBER)
            z = self.look_ahead
            statements[variable_lexeme.value.lower()].append(
                (int(x.value), int(y.value), int(z.value))
            )

    def parse_single_variable(self, variable_lexeme):
        statements[variable_lexeme.value.lower()] = int(
            self.look_ahead.value)

    def parse_variable(self):
        variable_lexeme = self.look_ahead
        self.match(LexemeTypes.ASSIGN)
        self.match(LexemeTypes.NUMBER)

        if variable_lexeme.value.lower() == "n":
            self.parse_list_variable(variable_lexeme)
        elif variable_lexeme.value.lower() in coordinates:
            self.parse_single_variable(variable_lexeme)
        else:
            raise SyntaxError(self, "Invalid Variable")

    def parse(self):
        while True:
            self.next()
            if self.look_ahead.type == LexemeTypes.END:
                break
            if self.look_ahead.type == LexemeTypes.VARIABLE:
                self.parse_variable()
            if self.look_ahead.type == LexemeTypes.KEY_WORD:
                if self.look_ahead.value.lower() != "begin":
                    raise SyntaxError()
                RobotPathAnalyzer(self.analyzer, self.look_ahead).parse()


SyntaxAnalyzer().parse()
