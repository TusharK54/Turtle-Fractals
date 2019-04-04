import turtle
from time import time

class Fractal():
    """Generates fractals using recursion"""
    def __init__(self, turtle):
        self.turtle = turtle
    
    def setup(self, unit):
        self.turtle.reset()
        self.structures = 0

    def draw(self, unit, iterations):
        self.setup(unit)
        start = time()
        self._recursive_draw(unit, iterations)
        self.time_elapsed = time() - start

    def _recursive_draw(self, unit, iterations):
        self.structures += 1

    def __repr__(self):
        return self.__class__.__name__

class KochCurve(Fractal):
    def setup(self, unit):
        Fractal.setup(self, unit)
        self.turtle.penup()
        x = self.turtle.xcor() - unit * 3 / 2
        y = self.turtle.ycor() - (unit / 2 * 3 ** 0.5) / 3
        self.turtle.setposition(x, y)
        self.turtle.pendown()

    def _recursive_draw(self, unit, iterations):
        Fractal._recursive_draw(self, unit, iterations)
        self._recursive_draw(unit/3, iterations-1) if iterations > 1 else self.turtle.forward(unit)
        self.turtle.left(60)
        self._recursive_draw(unit/3, iterations-1) if iterations > 1 else self.turtle.forward(unit)
        self.turtle.right(120)
        self._recursive_draw(unit/3, iterations-1) if iterations > 1 else self.turtle.forward(unit)
        self.turtle.left(60)
        self._recursive_draw(unit/3, iterations-1) if iterations > 1 else self.turtle.forward(unit)

    def __repr__(self):
        return 'Koch Curve'

class SierpinskiTriangle(Fractal):
    def setup(self, unit):
        Fractal.setup(self, unit)
        self.turtle.penup()
        x = self.turtle.xcor() - unit
        y = self.turtle.ycor() - (unit * 3 ** 0.5) / 2
        self.turtle.setposition(x, y)
        self.turtle.pendown()

        # Draw outer triangle
        self.turtle.left(60)
        self.turtle.forward(unit*2)
        self.turtle.right(120)
        self.turtle.forward(unit*2)
        self.turtle.right(120)
        self.turtle.forward(unit*2)
        self.turtle.backward(unit)
        self.turtle.right(180)

    def _recursive_draw(self, unit, iterations):
        Fractal._recursive_draw(self, unit, iterations)
        self.turtle.left(120)
        self.turtle.forward(unit/2)
        if iterations > 1: self._recursive_draw(unit/2, iterations-1)
        self.turtle.forward(unit/2)
        self.turtle.right(120)
        self.turtle.forward(unit/2)
        if iterations > 1: self._recursive_draw(unit/2, iterations-1)
        self.turtle.forward(unit/2)
        self.turtle.right(120)
        self.turtle.forward(unit/2)
        if iterations > 1: self._recursive_draw(unit/2, iterations-1)
        self.turtle.forward(unit/2)
        self.turtle.left(120)

    def __repr__(self):
        return 'Sierpiński\'s Triangle'

class Circles(Fractal):
    def _recursive_draw(self, unit, iterations):
        Fractal._recursive_draw(self, unit, iterations)
        # Draw center circle
        self.turtle.penup()
        self.turtle.setposition(self.turtle.xcor(), self.turtle.ycor() - unit)
        self.turtle.pendown()
        self.turtle.circle(unit)
        self.turtle.penup()
        self.turtle.setposition(self.turtle.xcor(), self.turtle.ycor() + unit)
        self.turtle.pendown()

        if iterations > 1:
            # Draw circle to right
            self.turtle.penup()
            self.turtle.setx(self.turtle.xcor() + unit)
            self.turtle.pendown()
            self._recursive_draw(unit/2, iterations-1)
            self.turtle.penup()
            self.turtle.setx(self.turtle.xcor() - unit)
            self.turtle.pendown()

            # Draw circle to left
            self.turtle.penup()
            self.turtle.setx(self.turtle.xcor() - unit)
            self.turtle.pendown()
            self._recursive_draw(unit/2, iterations-1)
            self.turtle.penup()
            self.turtle.setx(self.turtle.xcor() + unit)
            self.turtle.pendown()

            # Draw circle above
            self.turtle.penup()
            self.turtle.sety(self.turtle.ycor() + unit)
            self.turtle.pendown()
            self._recursive_draw(unit/2, iterations-1)
            self.turtle.penup()
            self.turtle.sety(self.turtle.ycor() - unit)
            self.turtle.pendown()

            # Draw circle below
            self.turtle.penup()
            self.turtle.sety(self.turtle.ycor() - unit)
            self.turtle.pendown()
            self._recursive_draw(unit/2, iterations-1)
            self.turtle.penup()
            self.turtle.sety(self.turtle.ycor() + unit)
            self.turtle.pendown()

    def __repr__(self):
        return 'Recursive Circles'

class LSystem(Fractal):
    """Generates fractals using the Lindenmayer system"""
    def __init__(self, turtle):
        Fractal.__init__(self, turtle)
        self.alphabet = []
        self.functions = {}
        self.rules = {}
        self._axiom = ''
        self._angle = 0

        self.add_character('L', 'LEFT')
        self.add_character('R', 'RIGHT')

    def add_character(self, character, function, production_rule = None):
        """Adds a character to the alphabet and defines its function and production rule"""
        character = character.upper()
        function = function.upper()
        if production_rule != None: 
            production_rule = production_rule.replace(' ', '').replace(',', '').upper()
        
        if character not in self.alphabet:
            self.alphabet.append(character)
        self.functions[character] = function
        if production_rule != None:
            self.rules[character] = production_rule
        else:
            self.rules[character] = character
    
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

    def get_functions(self):
        """Returns a list of function names implemented by this class"""
        functions = []
        functions.append('DRAW')
        functions.append('MOVE')
        functions.append('RIGHT')
        functions.append('LEFT')
        # ^ Add new implemented functions above this line ^
        return functions

    def draw(self, unit, iterations):
        self.setup(unit)
        start = time()
        
        # Draw the fractal using generated sequence
        sequence = self._generate_sequence(iterations)
        for character in sequence:
            function = self.functions[character]
            
            # Define various functions
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
            else:
                print(f'Ignoring unknown function: {function}')

        self.time_elapsed = time() - start

    def _generate_sequence(self, iterations):
        """Generates the fractal sequence using production rules for the given number of iterations"""
        # TODO: center turtle using sequence
        # x_min, x_max, y_min, y_max = self.turtle.xcor(), self.turtle.xcor(), self.turtle.ycor(),self.turtle.ycor()
        sequence = self._axiom
        for _ in range(iterations):
            next_sequence = ''
            for character in sequence:
                next_sequence += self.rules[character]
            sequence = next_sequence

        # TODO: Add support for this (currently incorrect)
        for character in sequence:
            if self.functions[character] == 'DRAW':
                self.structures += 1
        return sequence

def get_fractals(turtle):
    """Returns a list of instances of all fractal classes implemented in this module"""
    fractals = []
    fractals.append(KochCurve(turtle))
    fractals.append(SierpinskiTriangle(turtle))
    fractals.append(Circles(turtle))

    # ^ Add new implemented fractals above this line ^
    return fractals

if __name__ == '__main__':
    tim = turtle.Turtle()
    fractal = LSystem(tim)

    fractal.add_character('A', 'draw', 'B r A r B')
    fractal.add_character('B', 'draw', 'A l B l A')
    fractal.axiom('A')
    fractal.angle(60)

    fractal.draw(7, 6)
    print(f'{fractal.structures} fractal structures')
    input('Press ENTER to exit')