
class FileInput:
    def __init__(self):
        self.input = open(
            'C:\\Users\\Morteza\\Desktop\\compilers\\robot_input.txt', "r").read() + "\n"
        self.pivot = -1
        self.__end = len(self.input)
        
    def char(self):
        return self.input[self.pivot]

    def next(self):
        self.pivot += 1
        return self.input[self.pivot]

    def retract(self):
        self.pivot -= 1
        return self.input[self.pivot]


    def endchar(self):
        return self.pivot + 1 >= self.__end