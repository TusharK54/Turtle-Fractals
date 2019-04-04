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
textbox_content = tk.StringVar()
fractal_key = tk.StringVar()

# Add fractal option menu widget
fractal_list = {repr(f) : f for f in fractals.get_fractals(turtle)}
fractal_key.set(list(fractal_list.values())[0])
fractal_menu = tk.OptionMenu(panel, fractal_key, *list(fractal_list.values()))
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

textbox_label = tk.Label(textbox, anchor = 'center', relief = 'groove', text = '\nTurtle Fractal Drawer\n\nby Tushar Khan\n')
textbox_label.pack(fill = 'x')

# Add tracer to textbox_content variable to change textbox in real time
def update_textbox(*_):
    textbox_label.configure(text = textbox_content.get())
textbox_content.trace('w', update_textbox)

# Define and configure button functions
def draw_fractal():
    textbox_content.set('\n\nDrawing fractal...\n\n')
    fractal = fractal_list[fractal_key.get()]
    fractal.draw(size_scale.get(), iterations_scale.get())
    screen.update()
    textbox_content.set(f'''\nDONE
in {round(fractal.time_elapsed, 10)} s
{fractal.structures} fractal structure{'s' if fractal.structures > 1 else ''}\n''')
    draw_button.configure(state = 'normal')

def reset_canvas():
    turtle.penup()
    screen.resetscreen()
    turtle.pendown()

draw_button.configure(command = draw_fractal)
reset_button.configure(command = reset_canvas)

# Run tkinter loop
root.mainloop()