import turtle
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

    def draw(self, unit, iterations):
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

        # TODO: center turtle using sequence

        # Draw the fractal using generated sequence
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

        self.time_elapsed = time() - start

    @staticmethod
    def get_functions():
        """Returns a list of function names implemented by this class"""
        functions = []
        functions.append('DRAW')
        functions.append('MOVE')
        functions.append('RIGHT')
        functions.append('LEFT')
        #functions.append('SAVE POS')
        #functions.append('LOAD POS')
        # ^ Add new implemented functions above this line ^
        return functions

if __name__ == '__main__':
    tim = turtle.Turtle()
    fractal = LFractal(tim)

    fractal.add_character('F', 'draw', 'F L F R R F L F')
    fractal.add_character('R', 'right')
    fractal.add_character('L', 'left')
    fractal.axiom('F rr F rr F rr')
    fractal.angle(60)

    fractal.draw(10, 3)
    print(f'{fractal.structures} fractal structures')
    input('Press ENTER to exit')