import tkinter as tk

from os import listdir
from json import dump, load
from turtle import RawTurtle, TurtleScreen
from fractals import LFractal, symbol_functions

"""
Project started on April 1, 2019
by Tushar Khan
"""

# Set window parameters
window_height = 750
canvas_width = window_height
panel_width = 300

# Create top-level window and add canvas and control panel
root = tk.Tk()
root.title('Turtle Fractals')
canvas = tk.Canvas(root, width = canvas_width, height = window_height, cursor = 'crosshair')
panel = tk.Frame(root, width = panel_width, height = window_height)
canvas.pack(side = 'left', fill = 'both', expand = True)
panel.pack(side = 'right', fill = 'y', expand = False)
panel.pack_propagate(False)

# Create turtle objects
screen = TurtleScreen(canvas)
turtle = RawTurtle(screen)

# Load fractals from save files into a dictionary
saved_fractals_dir = 'saved_fractals'
fractal_dict = {}
for file in listdir(saved_fractals_dir):
    if file.endswith('.txt'):
        with open(saved_fractals_dir + '/' + file) as f:
            fractal_tuple = tuple(load(f))
            fractal_dict[file[:-len('.txt')]] = fractal_tuple

fractal = LFractal()

# Add fractal editor frame
editor_pad = 5
editor_frame = tk.Frame(panel, width = panel_width, pady = editor_pad)
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
angle_label = tk.Label(editor_frame, textvariable = angle_var, anchor = 'w', padx = label_pad, relief = 'sunken')
angle_scale = tk.Scale(editor_frame, orient = 'horizontal', from_ = 0, to = 179, resolution = 1, variable = angle_var, showvalue = 0)
alphabet_entry.grid(row = 2, column = 1, columnspan = 2, sticky = 'nsew')
axiom_entry.grid(row = 3, column = 1, columnspan = 2, sticky = 'nsew')
angle_label.grid(row = 4, column = 1, sticky = 'nsew')
angle_scale.grid(row = 4, column = 2, sticky = 'ew')

# Add production rule rows for each character
production_rules = []
def update_rules_box(*_):
    rule_rows = 10
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
        function_list = symbol_functions()
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
size_scale = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 100, label = 'Unit Length:', resolution = 1)
size_scale.set(25)
iterations_scale.pack(fill = 'x')
speed_scale.pack(fill = 'x')
size_scale.pack(fill = 'x')
    
# Add fractal drawing buttons
button_frame = tk.Frame(panel, width = panel_width)
button_frame.pack(fill = 'x')
button_frame.columnconfigure(0, weight = 1, minsize = 2/2)
button_frame.columnconfigure(1, weight = 1, minsize = 2/2)

draw_button = tk.Button(button_frame, text = 'Generate')
reset_button = tk.Button(button_frame, text = 'Reset')
save_fractal_button = tk.Button(button_frame, text = 'Save Fractal')
save_image_button = tk.Button(button_frame, text = 'Save Image')
draw_button.grid(row = 0, column = 0, sticky = 'nsew')
reset_button.grid(row = 0, column = 1, sticky = 'nsew')
save_fractal_button.grid(row = 1, column = 0, sticky = 'nsew')
save_image_button.grid(row = 1, column = 1, sticky = 'nsew')

# Add text box
textbox_pad = 0
textbox_frame = tk.Frame(panel, pady = textbox_pad, padx = textbox_pad)
textbox_frame.pack(side = 'bottom', fill = 'both', expand = True)
textbox_var = tk.StringVar()
textbox_var.set('Turtle Fractal Drawer')
textbox_label = tk.Label(textbox_frame, width = panel_width, relief = 'groove', textvariable = textbox_var)
textbox_label.pack(side = 'bottom', fill = 'both', expand = True)

# Define and configure button functions
def draw_fractal():
    textbox_var.set('Drawing fractal...')
    draw_button.configure(state = 'disabled')
    
    # Generate fractal
    fractal = LFractal()
    fractal.axiom(axiom_var.get())
    fractal.angle(angle_var.get())
    for elem in production_rules:
        fractal.add_character(elem['char'].get(), elem['function'].get(), elem['rule'].get())

    #TODO: pre-compile fractal

    # Draw fractal
    fractal.draw(turtle, size_scale.get(), iterations_scale.get())
    screen.update()

    textbox_var.set(f'Done in {round(fractal.time_elapsed, 10)} s')
    draw_button.configure(state = 'normal')

def reset_canvas():
    screen.resetscreen()

def save_fractal():
    pass

def save_image():
    screen.getcanvas().postscript(file = 'frac.eps')
    textbox_var.set('Saved image as frac.eps')

# Configure button commands
draw_button.configure(command = draw_fractal)
reset_button.configure(command = reset_canvas)
save_fractal_button.configure(command = save_fractal)
save_image_button.configure(command = save_image)

# Add tracer functions
def load_fractal(*_):
    fractal.load_tuple(fractal_dict[fractal_var.get()])
    alphabet_var.set(fractal.alphabet)
    axiom_var.set(' '.join(fractal.axiom()))
    angle_var.set(fractal.angle())
    update_rules_box()
fractal_var.trace_add('write', load_fractal)

def update_alphabet(*_):
    alphabet = alphabet_entry.get().replace(' ', '').replace(',', '')
    new_alphabet = []
    next_open_row = production_rules[0]
    for row in production_rules:
        character = row['char'].get()
        if len(character) == 0:
            next_open_row = row
            break
        if character in alphabet:
            alphabet.replace(character, '')
            new_alphabet.append(character)
        else:               # character removed
            production_rules.remove(row)
    if len(alphabet) > 0:   # character added
        new_alphabet.append(alphabet)
        next_open_row['char'] = alphabet
    alphabet_var.set(new_alphabet)
#alphabet_var.trace_add('write', update_alphabet)

def adjust_speed(*_):
    screen.tracer(speed_var.get(), 10)
speed_var.trace_add('write', adjust_speed)

def update_textbox(*_):
    textbox_label.configure(text = textbox_var.get())
textbox_var.trace_add('write', update_textbox)

# Run tkinter loop
root.mainloop()