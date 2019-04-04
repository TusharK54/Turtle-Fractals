import tkinter as tk
from turtle import RawTurtle, TurtleScreen
from time import time

import fractals
    
# Create top-level window
root = tk.Tk()
root.title('Turtle Fractals')

# Set window parameters
window_height = 750
canvas_width = window_height
panel_width = 300
panel_bg = 'lightblue'

# Add canvas and control panel
canvas = tk.Canvas(root, width = canvas_width, height = window_height, cursor = 'crosshair')
panel = tk.Frame(root, width = panel_width, height = window_height, bg = panel_bg)
canvas.pack(side = 'left', fill = 'both', expand = True)
panel.pack(side = 'right', fill = 'y', expand = False)
panel.pack_propagate(False)

# Create turtle objects
screen = TurtleScreen(canvas)
turtle = RawTurtle(screen)

# Create application variables
speed = tk.IntVar()
fractal = tk.StringVar()

# Add fractal option menu widget
fractal_list = {repr(f) : f for f in fractals.get_fractals(turtle)}
fractal.set(list(fractal_list.values())[0])
fractal_menu = tk.OptionMenu(panel, fractal, *list(fractal_list.values()))
fractal_menu.configure(anchor = 'center')
tk.Label(panel, text = 'Fractal:', anchor = 'w', padx = 9).pack(fill = 'x')
fractal_menu.pack(fill = 'x')
    
# Add scale widgets
iterations_scale  = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 10, label = 'Iterations:',)
speed_scale       = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 300, label = 'Speed:', variable = speed)
size_scale        = tk.Scale(panel, orient = 'horizontal', from_ = 100, to = 500, label = 'Size:', resolution = 10)
iterations_scale.pack(fill = 'x')
speed_scale.pack(fill = 'x')
size_scale.pack(fill = 'x')

# Add tracer to speed variable to change turtle speed in real time
def adjust_speed(*_):
    screen.tracer(speed.get(), 10)
speed.trace('w', adjust_speed)
    
# Add buttons
draw_button = tk.Button(panel, text = 'Draw')
reset_button = tk.Button(panel, text = 'Reset')
draw_button.pack(fill = 'both')
reset_button.pack(fill = 'both')

# Add text box
textbox_pad = 10
textbox = tk.Frame(panel, width = panel_width, relief = 'groove', pady = textbox_pad, padx = textbox_pad, bg = panel_bg)
textbox.pack(side = 'bottom', fill = 'x')

textbox_label = tk.Label(textbox, anchor = 'center', relief = 'groove', text = '\nTurtle Fractal Drawer\nby Tushar Khan\n')
textbox_label.pack(fill = 'x')

# Define various textbox states
def textbox_drawing():
    content = '\nDrawing fractal...\n\n'
    textbox_label.configure(text = content)

def textbox_done():
    content = f'\nDONE\nTime: {round(fractal_list[fractal.get()].time_elapsed, 10)} s\n'
    textbox_label.configure(text = content)

# Define and configure button functions
def draw_fractal():
    fractal_list[fractal.get()].draw(size_scale.get(), iterations_scale.get())
    screen.update()
    textbox_done()
    draw_button.configure(state = 'normal')

def reset_canvas():
    turtle.penup()
    screen.resetscreen()
    turtle.pendown()

draw_button.configure(command = draw_fractal)
reset_button.configure(command = reset_canvas)

# Run tkinter loop
root.mainloop()