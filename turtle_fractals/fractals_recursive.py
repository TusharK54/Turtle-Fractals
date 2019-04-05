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
    fractal = KochCurve(tim)

    fractal.draw(10, 2)
    print(f'{fractal.structures} fractal structures')
    input('Press ENTER to exit')