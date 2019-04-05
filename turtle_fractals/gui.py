import tkinter as tk
from turtle import RawTurtle, TurtleScreen
from time import time

import turtle_fractals

# Set window parameters
window_height = 750
canvas_width = window_height
panel_width = 300
panel_bg = 'pink'

# Create top-level window and add canvas and control panel
root = tk.Tk()
root.title('Turtle Fractals')
canvas = tk.Canvas(root, width = canvas_width, height = window_height, cursor = 'crosshair')
panel = tk.Frame(root, width = panel_width, height = window_height, bg = panel_bg)
canvas.pack(side = 'left', fill = 'both', expand = True)
panel.pack(side = 'right', fill = 'y', expand = False)
panel.pack_propagate(False)

# Create turtle objects
screen = TurtleScreen(canvas)
turtle = RawTurtle(screen)

# Load fractals into a dictionary
fractal_dict = {} # TODO: Extract from file
    # TEMP BELOW
k_curve = turtle_fractals.LFractal(turtle)
k_curve.add_character('F', 'draw', 'F L F R R F L F')
k_curve.add_character('R', 'right')
k_curve.add_character('L', 'left')
k_curve.axiom('F rr F rr F rr')
k_curve.angle(60)
fractal_dict['Koch Snowflake'] = k_curve

triangle = turtle_fractals.LFractal(turtle)
triangle.add_character('F', 'draw', 'F L G R F R G L F')
triangle.add_character('G', 'draw', 'GG')
triangle.add_character('R', 'right')
triangle.add_character('L', 'left')
triangle.axiom('F l G l G')
triangle.angle(120)
fractal_dict['Sierpinski Triangle'] = triangle

dragon = turtle_fractals.LFractal(turtle)
dragon.add_character('X', production_rule = 'X R Y F R')
dragon.add_character('Y', production_rule = 'L F X L Y')
dragon.add_character('F', 'draw')
dragon.add_character('R', 'right')
dragon.add_character('L', 'left')
dragon.axiom('F X')
dragon.angle(90)
fractal_dict['Dragon Curve'] = dragon
    # TEMP ABOVE
fractal = turtle_fractals.LFractal(turtle)

# Add fractal editor frame
editor_pad = 10
editor_frame = tk.Frame(panel, width = panel_width, bg = 'lightblue', pady = editor_pad)
editor_frame.pack(side = 'top', fill = 'both')

editor_frame.columnconfigure(0, weight = 10)
editor_frame.columnconfigure(1, weight = 1)
editor_frame.columnconfigure(2, weight = 12)

# Add load fractal option menu widget
fractal_var = tk.StringVar()
fractal_var.set('Custom')
fractal_menu = tk.OptionMenu(editor_frame, fractal_var, *list(fractal_dict.keys()))
fractal_menu.grid(row = 1, columnspan = 3, sticky = 'ew')

# Add editor frame labels
label_pad = 5
tk.Label(editor_frame, text = 'Load Fractal:',     anchor = 'w', padx = label_pad).grid(row = 0, columnspan = 3, sticky = 'ew')
tk.Label(editor_frame, text = 'Alphabet:',         anchor = 'w', padx = label_pad).grid(row = 2, column = 0, sticky = 'nsew')
tk.Label(editor_frame, text = 'Axiom:',            anchor = 'w', padx = label_pad).grid(row = 3, column = 0, sticky = 'nsew')
tk.Label(editor_frame, text = 'Angle:',            anchor = 'w', padx = label_pad).grid(row = 4, column = 0, sticky = 'nsew')
tk.Label(editor_frame, text = ' ').grid(row = 5, columnspan = 3, sticky = 'nsew')
tk.Label(editor_frame, text = 'Function',          anchor = 'w', padx = label_pad).grid(row = 6, column = 0, sticky = 'nsew')
tk.Label(editor_frame, text = 'Char',              anchor = 'w', padx = label_pad).grid(row = 6, column = 1, sticky = 'nsew')
tk.Label(editor_frame, text = 'Production Rule',   anchor = 'w', padx = label_pad).grid(row = 6, column = 2, sticky = 'nsew')

# Add general editor entry and spinboxes
alphabet_var = tk.StringVar()
axiom_var = tk.StringVar()
angle_var = tk.IntVar()
alphabet_entry = tk.Entry(editor_frame, textvariable = alphabet_var)
axiom_entry = tk.Entry(editor_frame, textvariable = axiom_var)
angle_spinbox = tk.Spinbox(editor_frame, from_ = -180, to = 180, textvariable = angle_var)
alphabet_entry.grid(row = 2, column = 1, columnspan = 2, sticky = 'nsew')
axiom_entry.grid(row = 3, column = 1, columnspan = 2, sticky = 'nsew')
angle_spinbox.grid(row = 4, column = 1, columnspan = 2, sticky = 'nsew')

# Add production rule rows for each character
rule_rows = 8
production_rules = []
def update_rules_box(*_):
    production_rules.clear()
    alphabet = alphabet_entry.get().replace(' ', '').replace(',', '')
    for i in range(rule_rows):
        # Create production rule variables
        char_var = tk.StringVar()
        function_var = tk.StringVar()
        rule_var = tk.StringVar()
        char_var.set(alphabet[i] if i < len(alphabet) else '')
        function_var.set(fractal.functions[char_var.get()] if char_var.get() in fractal.functions else '')
        rule_var.set(' '.join(fractal.rules[char_var.get()]) if char_var.get() in fractal.rules else char_var.get())
        production_rules.append({'char' : char_var, 'function' : function_var, 'rule' : rule_var})

        # Add function option menu
        function_list = turtle_fractals.LFractal.get_functions()
        function_menu = tk.OptionMenu(editor_frame, function_var, *function_list)
        function_menu.grid(row = 7 + i, column = 0, sticky = 'nsew')

        # Add char entry box
        char_label = tk.Label(editor_frame, textvariable = char_var, anchor = 'w', padx = label_pad, fg = 'red', relief = 'sunken')
        char_label.grid(row = 7 + i, column = 1, sticky = 'nsew')

        # Add production rule entry box
        rule_entry = tk.Entry(editor_frame, textvariable = rule_var)
        rule_entry.grid(row = 7 + i, column = 2, sticky = 'nsew')

update_rules_box()

# Add scale widgets
speed_var = tk.IntVar()
iterations_scale = tk.Scale(panel, orient = 'horizontal', from_ = 0, to = 20, label = 'Iterations:',)
speed_scale = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 100, label = 'Speed:', variable = speed_var)
size_scale = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 200, label = 'Unit Length:', resolution = 2)
size_scale.set(100)
iterations_scale.pack(fill = 'x')
speed_scale.pack(fill = 'x')
size_scale.pack(fill = 'x')
    
# Add fractal drawing buttons
draw_button = tk.Button(panel, text = 'Generate')
reset_button = tk.Button(panel, text = 'Reset')
draw_button.pack(fill = 'both')
reset_button.pack(fill = 'both')

# Add text box
textbox_pad = 10
textbox_frame = tk.Frame(panel, pady = textbox_pad, padx = textbox_pad, bg = panel_bg)
textbox_frame.pack(side = 'bottom', fill = 'x')
textbox_var = tk.StringVar()
textbox_var.set('\nTurtle Fractal Drawer\n\nby Tushar Khan\n')
textbox_label = tk.Label(textbox_frame, width = panel_width, relief = 'groove', textvariable = textbox_var)
textbox_label.pack(side = 'bottom', fill = 'x')

# Define and configure button functions
def draw_fractal():
    textbox_var.set('\n\nDrawing fractal...\n\n')
    draw_button.configure(state = 'disabled')
    
    # Generate fractal
    fractal = turtle_fractals.LFractal(turtle)
    fractal.axiom(axiom_var.get())
    fractal.angle(angle_var.get())
    for elem in production_rules:
        fractal.add_character(elem['char'].get(), elem['function'].get(), elem['rule'].get())

    # Draw fractal
    fractal.draw(size_scale.get(), iterations_scale.get())
    screen.update()

    textbox_var.set(f'''\nDONE
in {round(fractal.time_elapsed, 10)} s
{fractal.structures} fractal structure{'s' if fractal.structures > 1 else ''}\n''')
    draw_button.configure(state = 'normal')

def reset_canvas():
    screen.resetscreen()

# Configure button commands
draw_button.configure(command = draw_fractal)
reset_button.configure(command = reset_canvas)

# Add tracer functions
def load_fractal(*_):
    global fractal
    fractal = fractal_dict[fractal_var.get()]
    alphabet_var.set(fractal.alphabet)
    axiom_var.set(' '.join(fractal.axiom()))
    angle_var.set(fractal.angle())
    update_rules_box()
fractal_var.trace_add('write', load_fractal)

alphabet_var.trace_add('write', update_rules_box)

def adjust_speed(*_):
    screen.tracer(speed_var.get(), 10)
speed_var.trace_add('write', adjust_speed)

def update_textbox(*_):
    textbox_label.configure(text = textbox_var.get())
textbox_var.trace_add('write', update_textbox)

# Run tkinter loop
root.mainloop()