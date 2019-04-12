import turtle
from math import sin, cos, radians
from time import time

class LFractal():
    """Generates fractals using the Lindenmayer system"""
    def __init__(self, turtle):
        self.turtle = turtle
        self.turtle.reset()
        self.alphabet = []
        self.functions = {}
        self.rules = {}
        self._axiom = ''
        self._angle = 0

    def add_character(self, character, function = '', production_rule = None):
        """Adds a character to the alphabet and defines its function and production rule"""
        character = character.upper()
        function = function.upper()
        if production_rule != None: 
            production_rule = production_rule.replace(' ', '').replace(',', '').upper()
        
        if character not in self.alphabet: self.alphabet.insert(0, character)
        self.functions[character] = function
        self.rules[character] = production_rule if production_rule != None else character

    def axiom(self, string = None):
        """Defines the axiom of the system; returns the axiom if no argument is provided"""
        if string != None:
            self._axiom = string.replace(' ', '').replace(',', '').upper()
        return self._axiom

    def angle(self, degrees = None):
        """Defines the angle of rotation; returns the angle if no argument is provided"""
        if degrees != None:
            self._angle = degrees
        return self._angle

    def draw(self, size, iterations):
        """Draws the fractal for the given number of iterations"""
        self.turtle.reset()
        self.structures = 0
        start = time()
        
        # Generate fractal sequence
        sequence = self._axiom
        for _ in range(iterations):
            next_sequence = ''
            for character in sequence:
                next_sequence += self.rules[character]
            sequence = next_sequence

        # Center turtle using generated sequence; relatively fast algorithm
        sim_x, sim_y = self.turtle.xcor(), self.turtle.ycor()
        sim_heading = self.turtle.heading()
        sim_pos_stack = []
        min_x = max_x = sim_x
        min_y = max_y = sim_y
        for character in sequence:
            function = self.functions[character]
            if function == 'DRAW' or function =='MOVE':
                sim_x = sim_x + round(size * cos(radians(sim_heading)), 10)
                sim_y = sim_y + round(size * sin(radians(sim_heading)), 10)
            elif function == 'RIGHT':
                sim_heading = (sim_heading - self.angle()) % 360
            elif function == 'LEFT':
                sim_heading = (sim_heading + self.angle()) % 360
            elif function == 'SAVE POS':
                sim_pos_stack.append((sim_x, sim_y))
            elif function == 'LOAD POS':
                sim_x, sim_y = sim_pos_stack.pop()
            min_x = min(min_x, sim_x)
            max_x = max(max_x, sim_x)
            min_y = min(min_y, sim_y)
            max_y = max(max_y, sim_y)

        self.turtle.penup()
        self.turtle.setx(self.turtle.xcor() - (max_x + min_x) / 2)
        self.turtle.sety(self.turtle.ycor() - (max_y + min_y) / 2)
        self.turtle.pendown()

        # TODO:
        # Scale unit length to fit fractal within specified size
        length_x = max_x - min_x
        length_y = max_y - min_y
        length = max(length_x, length_y)
        unit = size

        # Draw fractal using generated sequence
        position_stack = []
        for character in sequence:
            function = self.functions[character]
            if   function == 'DRAW':
                self.turtle.forward(unit)
            elif function == 'MOVE':
                self.turtle.penup()
                self.turtle.forward(unit)
                self.turtle.pendown()
            elif function == 'RIGHT':
                self.turtle.right(self._angle)
            elif function == 'LEFT':
                self.turtle.left(self._angle)
            elif function == 'SAVE POS':
                position_stack.append(self.turtle.pos())
            elif function == 'LOAD POS':
                self.turtle.penup()
                self.turtle.setposition(position_stack.pop())
                self.turtle.pendown()

        self.time_elapsed = time() - start

    @staticmethod
    def get_functions():
        """Returns a list of function names implemented by this class"""
        functions = []
        functions.append('DRAW')
        functions.append('MOVE')
        functions.append('RIGHT')
        functions.append('LEFT')
        functions.append('SAVE POS')
        functions.append('LOAD POS')
        # ^ Add new implemented functions above this line ^
        return functions

if __name__ == '__main__':
    tim = turtle.Turtle()
    fractal = LFractal(tim)

    fractal.add_character('F', 'draw', 'F F + [ + F - F - F ] - [ - F + F + F ]')
    fractal.add_character('+', 'right')
    fractal.add_character('-', 'left')
    fractal.add_character('[', 'save pos')
    fractal.add_character(']', 'load pos')
    fractal.axiom('F')
    fractal.angle(25)

    fractal.draw(10, 3)
    print(f'{fractal.structures} fractal structures')
    input('Press ENTER to exit')