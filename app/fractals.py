import turtle
from math import sin, cos, radians
from time import time

class LFractal():
    """Generates fractals using the Lindenmayer system"""

    # Define symbol functions
    DRAW    = 'DRAW'
    MOVE    = 'MOVE'
    RIGHT   = 'RIGHT'
    LEFT    = 'LEFT'
    SAVE    = 'SAVE'
    LOAD    = 'LOAD'

    def __init__(self):
        self.alphabet = []
        self.functions = {}
        self.rules = {}
        self._axiom = ''
        self._angle = 0

    def get_tuple(self) -> tuple:
        """Returns the properties of the fractal as a tuple"""
        return (self.alphabet, self.functions, self.rules, self._axiom, self._angle)

    def load_tuple(self, tuple_ : tuple):
        """Loads the properties of the fractal from a tuple"""
        self.alphabet, self.functions, self.rules, self._axiom, self._angle = tuple_

    def add_character(self, character : str, function = '', production_rule = None):
        """Adds a character to the alphabet and defines its function and production rule"""
        if character == '' or character == ' ':
            return
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

    def draw(self, turtle, size : int, iterations : int, max_sequence = 2000000):
        """Draws the fractal for the given number of iterations"""
        self.turtle = turtle
        self.turtle.reset()
        self.turtle.active = True
        start = time()
        
        # Generate fractal sequence
        self.sequence = self._axiom
        for _ in range(iterations):
            next_sequence = ''
            for character in self.sequence:
                next_sequence += self.rules[character]
                if len(next_sequence) > max_sequence:
                    raise Exception(f'Fractal sequence exceeded maximum of {max_sequence} characters')
            self.sequence = next_sequence

        # Center turtle using generated sequence; relatively fast algorithm
        sim_x, sim_y = self.turtle.xcor(), self.turtle.ycor()
        sim_heading = self.turtle.heading()
        sim_stack = []
        min_x = max_x = sim_x
        min_y = max_y = sim_y
        for character in self.sequence:
            function = self.functions[character]
            if function == LFractal.DRAW or function == LFractal.MOVE:
                sim_x = sim_x + round(size * cos(radians(sim_heading)), 10)
                sim_y = sim_y + round(size * sin(radians(sim_heading)), 10)
            elif function == LFractal.RIGHT:
                sim_heading = (sim_heading - self.angle()) % 360
            elif function == LFractal.LEFT:
                sim_heading = (sim_heading + self.angle()) % 360
            elif function == LFractal.SAVE:
                sim_stack.append(((sim_x, sim_y), sim_heading))
            elif function == LFractal.LOAD:
                position, heading = sim_stack.pop()
                sim_x, sim_y = position
                sim_heading = heading
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
        stack = []
        for character in self.sequence:
            if not self.turtle.active:
                self.turtle.reset()
                raise Exception('Fractal generation forcibly stopped')
            
            function = self.functions[character]
            if   function == LFractal.DRAW:
                self.turtle.forward(unit)
            elif function == LFractal.MOVE:
                self.turtle.penup()
                self.turtle.forward(unit)
                self.turtle.pendown()
            elif function == LFractal.RIGHT:
                self.turtle.right(self._angle)
            elif function == LFractal.LEFT:
                self.turtle.left(self._angle)
            elif function == LFractal.SAVE:
                stack.append((self.turtle.pos(), self.turtle.heading()))
            elif function == LFractal.LOAD:
                self.turtle.penup()
                position, heading = stack.pop()
                self.turtle.setposition(position)
                self.turtle.setheading(heading)
                self.turtle.pendown()

        self.time_elapsed = time() - start

def symbol_functions() -> list:
    """Returns a list of symbol function names implemented by the LFractal class"""
    functions = []
    functions.append(LFractal.DRAW)
    functions.append(LFractal.MOVE)
    functions.append(LFractal.RIGHT)
    functions.append(LFractal.LEFT)
    functions.append(LFractal.SAVE)
    functions.append(LFractal.LOAD)
    # ^ Add new implemented functions above this line ^
    return functions

if __name__ == '__main__':
    fractal = LFractal()

    fractal.add_character('F', 'draw', 'F F + [ + F - F - F ] - [ - F + F + F ]')
    fractal.add_character('+', 'right')
    fractal.add_character('-', 'left')
    fractal.add_character('[', 'save')
    fractal.add_character(']', 'load')
    fractal.axiom('F')
    fractal.angle(25)
    
    tim = turtle.Turtle()
    fractal.draw(tim, 10, 3)
    input('Press ENTER to exit')