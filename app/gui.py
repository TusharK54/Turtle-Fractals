import tkinter as tk

from os import listdir, path
from json import dump, load
from turtle import RawTurtle, TurtleScreen
from fractals import LFractal, symbol_functions
import random

"""
Project started on April 1, 2019
by Tushar Khan
"""

class Window():

    fractals_directory = 'saved_fractals'

    def __init__(self):
        # Set window and window elements constants
        window_height = 750
        canvas_width = window_height
        panel_width = 300

        label_pad = 5
        editor_pad = 5
        textbox_outside_pad = 0
        textbox_inside_pad = 5
        rule_rows = 10
        
        # Create top-level window and add canvas and control panel
        root = tk.Tk()
        root.title('Lindenmayer Turtle Fractals')
        self.canvas = tk.Canvas(root, width = canvas_width, height = window_height, cursor = 'crosshair')
        panel = tk.Frame(root, width = panel_width, height = window_height)
        self.canvas.pack(side = 'left', fill = 'both', expand = True)
        panel.pack(side = 'right', fill = 'y', expand = False)
        panel.pack_propagate(False)

        # Center window on screen
        width = canvas_width + panel_width
        height = window_height
        x = (root.winfo_screenwidth() - width)/2
        y = (root.winfo_screenheight() - height)/2 - 30
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Create turtle objects
        self.screen = TurtleScreen(self.canvas)
        self.turtle = RawTurtle(self.screen)

        # Add fractal editor frame
        self.editor_frame = tk.Frame(panel, width = panel_width, pady = editor_pad)
        self.editor_frame.pack(side = 'top', fill = 'both')

        self.editor_frame.columnconfigure(0, weight = 10)
        self.editor_frame.columnconfigure(1, weight = 1)
        self.editor_frame.columnconfigure(2, weight = 12)

        # Add editor frame labels
        tk.Label(self.editor_frame, text = 'Load Fractal:',     anchor = 'w', padx = label_pad).grid(row = 0, column = 0, sticky = 'ew')
        tk.Label(self.editor_frame, text = 'Alphabet:',         anchor = 'w', padx = label_pad).grid(row = 2, column = 0, sticky = 'nsew')
        tk.Label(self.editor_frame, text = 'Axiom:',            anchor = 'w', padx = label_pad).grid(row = 3, column = 0, sticky = 'nsew')
        tk.Label(self.editor_frame, text = 'Angle:',            anchor = 'w', padx = label_pad).grid(row = 4, column = 0, sticky = 'nsew')
        tk.Label(self.editor_frame, text = ' ').grid(row = 5, columnspan = 3, sticky = 'nsew')
        tk.Label(self.editor_frame, text = 'Function',          anchor = 'w', padx = label_pad).grid(row = 6, column = 0, sticky = 'nsew')
        tk.Label(self.editor_frame, text = 'Char',              anchor = 'w', padx = label_pad).grid(row = 6, column = 1, sticky = 'nsew')
        tk.Label(self.editor_frame, text = 'Production Rule',   anchor = 'w', padx = label_pad).grid(row = 6, column = 2, sticky = 'nsew')

        # Add load fractal option menu widget
        self.fractal_var = tk.StringVar()
        self.fractal_var.set('Custom')
        fractal_dict = self._generate_fractals_dictionary()
        self.fractal_menu = tk.OptionMenu(self.editor_frame, self.fractal_var, *list(fractal_dict.keys()))
        self.fractal_var.trace_add('write', callback = self._load_fractal)
        self.fractal_menu.grid(row = 0, column = 1, columnspan = 2, sticky = 'ew')

        # Add general editor entry and spinboxes
        self.alphabet_var = tk.StringVar()
        self.alphabet_entry = tk.Entry(self.editor_frame, textvariable = self.alphabet_var)
        self.alphabet_var.trace_add('write', callback = self._update_alphabet_entry)
        self.alphabet_entry.grid(row = 2, column = 1, columnspan = 2, sticky = 'nsew')

        self.axiom_var = tk.StringVar()
        self.axiom_entry = tk.Entry(self.editor_frame, textvariable = self.axiom_var)
        self.axiom_var.trace_add('write', callback = lambda *_ : self._update_entry(self.axiom_entry, self.axiom_var, _))
        self.axiom_entry.grid(row = 3, column = 1, columnspan = 2, sticky = 'nsew')

        self.angle_var = tk.IntVar()
        angle_label = tk.Label(self.editor_frame, textvariable = self.angle_var, anchor = 'w', padx = label_pad, relief = 'sunken')
        angle_scale = tk.Scale(self.editor_frame, orient = 'horizontal', from_ = 0, to = 179, resolution = 1, variable = self.angle_var, showvalue = 0)
        angle_label.grid(row = 4, column = 1, sticky = 'nsew')
        angle_scale.grid(row = 4, column = 2, sticky = 'ew')

        # Add production rule rows for each character
        self.production_rules = []
        for i in range(rule_rows):
            # Create production rule variables
            char_var = tk.StringVar()
            function_var = tk.StringVar()
            rule_var = tk.StringVar()
            self.production_rules.append({'char' : char_var, 'function' : function_var, 'rule' : rule_var})

            # Add function option menu
            function_list = symbol_functions()
            function_menu = tk.OptionMenu(self.editor_frame, function_var, '', *function_list)
            function_menu.grid(row = 7 + i, column = 0, sticky = 'nsew')

            # Add char entry box
            char_label = tk.Label(self.editor_frame, textvariable = char_var, anchor = 'w', padx = label_pad, fg = 'red', relief = 'sunken')
            char_label.grid(row = 7 + i, column = 1, sticky = 'nsew')

            # Add production rule entry box
            rule_entry = tk.Entry(self.editor_frame, textvariable = rule_var)
            rule_var.trace_add('write', callback = lambda *_ : self._update_entry(rule_entry, rule_var, _))
            rule_entry.grid(row = 7 + i, column = 2, sticky = 'nsew')

        # Add scale widgets
        self.speed_var = tk.IntVar()
        self.speed_var.trace_add('write', callback = lambda *_ : self.screen.tracer(self.speed_var.get(), 10))
        self.iterations_scale = tk.Scale(panel, orient = 'horizontal', from_ = 0, to = 20, label = 'Iterations:',)
        speed_scale = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 100, label = 'Speed:', variable = self.speed_var)
        self.size_scale = tk.Scale(panel, orient = 'horizontal', from_ = 1, to = 50, label = 'Unit Length:', resolution = 1)
        self.size_scale.set(25)
        self.iterations_scale.pack(fill = 'x')
        speed_scale.pack(fill = 'x')
        self.size_scale.pack(fill = 'x')
            
        # Add and configure fractal buttons
        button_frame = tk.Frame(panel, width = panel_width)
        button_frame.pack(fill = 'x')
        button_frame.columnconfigure(0, weight = 1, minsize = 2/2)
        button_frame.columnconfigure(1, weight = 1, minsize = 2/2)

        self.draw_button = tk.Button(button_frame, text = 'Draw', command = self._draw_fractal)
        self.reset_button = tk.Button(button_frame, text = 'Reset', command = self._reset_fractal)
        self.save_fractal_button = tk.Button(button_frame, text = 'Save Fractal', command = self._save_fractal_popup)
        self.save_image_button = tk.Button(button_frame, text = 'Save Image', command = self._save_image)
        self.draw_button.grid(row = 0, column = 0, sticky = 'nsew')
        self.reset_button.grid(row = 0, column = 1, sticky = 'nsew')
        self.save_fractal_button.grid(row = 1, column = 0, sticky = 'nsew')
        self.save_image_button.grid(row = 1, column = 1, sticky = 'nsew')
        
        # Add text box
        textbox_bg = '#dddddd'
        textbox_frame = tk.Frame(panel, pady = textbox_outside_pad, padx = textbox_outside_pad, bg = textbox_bg)
        textbox_frame.pack(side = 'bottom', fill = 'both', expand = True)
        self.textbox_var = tk.StringVar()
        self.textbox_var.set('Lindenmayer Fractals Drawer')
        self.textbox_label = tk.Label(textbox_frame, width = panel_width, relief = 'groove', font = ('Fixedsys', 7), textvariable = self.textbox_var, wraplength = panel_width - textbox_inside_pad, fg = 'black', bg = textbox_bg)
        self.textbox_var.trace_add('write', callback = lambda *_ : self.textbox_label.configure(text = self.textbox_var.get()))
        self.textbox_label.pack(side = 'bottom', fill = 'both', expand = True)

        # Run tkinter loop
        root.mainloop()

    def _generate_fractals_dictionary(self) -> dict:
        """Loads fractals from save files into a dictionary"""
        fractal_dict = {}
        directory = Window.fractals_directory
        for file in listdir(directory):
            if file.endswith('.json'):
                with open(directory + '/' + file) as f:
                    fractal_tuple = tuple(load(f))
                    fractal_dict[file[:-len('.json')]] = fractal_tuple
        return fractal_dict

    def _load_fractal(self, *_):
        # Load fractal from fractal dictionary
        fractal = LFractal()
        fractal_dict = self._generate_fractals_dictionary()
        fractal.load_tuple(fractal_dict[self.fractal_var.get()])

        # Update window elements
        self.alphabet_var.set(fractal.alphabet)
        self.axiom_var.set(' '.join(fractal.axiom()))
        self.angle_var.set(fractal.angle())
        for i in range(min(len(fractal.alphabet), len(self.production_rules))):
            char = fractal.alphabet[i]
            production_rule = self.production_rules[i]
            production_rule['char'].set(char)
            production_rule['function'].set(fractal.functions.get(char))
            production_rule['rule'].set(fractal.rules.get(char))

    def _generate_fractal(self) -> LFractal:
        """Returns an LFractal generated from the values specified by the GUI elements"""
        fractal = LFractal()
        fractal.alphabet = (list(self.alphabet_var.get().replace(' ', '')))
        fractal.axiom(self.axiom_var.get())
        fractal.angle(self.angle_var.get())
        for elem in self.production_rules:
            fractal.add_character(elem['char'].get(), elem['function'].get(), elem['rule'].get())
        return fractal

    def _draw_fractal(self):
        self.textbox_label.configure(fg = 'black')
        self.textbox_var.set('Drawing fractal...')
        self.draw_button.configure(state = 'disabled')
        
        fractal = self._generate_fractal()
        if self.alphabet_var.get() == '':
            self.textbox_label.configure(fg = 'orange')
            self.textbox_var.set(f'INVALID: Alphabet not defined')
        elif self.axiom_var.get() == '':
            self.textbox_label.configure(fg = 'orange')
            self.textbox_var.set(f'INVALID: Axiom not defined')
        else:
            self.canvas.unbind('<ButtonPress-1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<MouseWheel>')
            try:
                fractal.draw(self.turtle, self.size_scale.get(), self.iterations_scale.get())
            except Exception as e:
                self.textbox_label.configure(fg = 'red')
                self.textbox_var.set(f'ERROR: {e}')
            else:
                self.textbox_label.configure(fg = 'green')
                self.textbox_var.set(f'Done in {round(fractal.time_elapsed, 8)} sec\n{len(fractal.sequence)} character sequence')
            self.canvas.bind('<ButtonPress-1>', self._scroll_start)
            self.canvas.bind('<B1-Motion>', self._scroll_move)
            self.canvas.bind('<MouseWheel>', self._mouse_scroll)

        self.screen.update()
        self.draw_button.configure(state = 'normal')

    def _reset_fractal(self):
        self.turtle.active = False
        self.screen.reset()

    def _save_fractal_popup(self):
        # Create popup window
        self.save_popup = tk.Toplevel()
        self.save_popup.title('Save As')
        self.save_popup.resizable(False, False)

        # Add elements to popup window
        popup_frame = tk.Frame(self.save_popup, padx = 30, pady = 10)
        instruction_text = tk.Label(popup_frame, text = 'Enter name for fractal system:', height = 2)
        self.save_entry = tk.Entry(popup_frame)
        self.save_button1 = tk.Button(popup_frame, text = 'Done', command = lambda : self._save_fractal(overwrite = False), width = 5)
        self.save_button2 = tk.Button(popup_frame, text = 'Cancel', command = self.save_popup.destroy, width = 5)
        self.save_message = tk.Label(popup_frame, width = 41, height = 2)

        # Pack elements into popup window
        popup_frame.pack(expand = True, fill = tk.BOTH)
        instruction_text.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsw')
        self.save_entry.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew')
        self.save_button1.grid(row = 2, column = 0, sticky = 'nsew')
        self.save_button2.grid(row = 2, column = 1, sticky = 'nsew')
        self.save_message.grid(row = 3, column = 0, columnspan = 2)

    def _save_fractal(self, overwrite = False):
        directory = Window.fractals_directory
        fractal_name = ' '.join([word.capitalize() for word in self.save_entry.get().split(' ')])
        filename = directory + '\\' + fractal_name + '.json'

        print(filename)
        if fractal_name.replace(' ', '') == '':
            self.save_message.configure(text = 'You cannot leave the name blank')
        elif path.exists(filename) and not overwrite:
            self.save_message.configure(text = 'This fractal already exists.\nWould you like to overwrite its contents?')
            self.save_entry.configure(state = tk.DISABLED)
            self.save_button1.configure(text = 'Yes', command = lambda : self._save_fractal(overwrite = True))
            self.save_button2.configure(text = 'No', command = self.save_fractal_cancel_overwrite)
        else:
            # Dump fractal tuple to json file
            with open(filename, mode = 'w') as f:
                fractal = self._generate_fractal()
                dump(fractal.get_tuple(), f)

            # Update fractals menu TODO: update menu to show new fractals
            fractal_dict = self._generate_fractals_dictionary()
            self.fractal_menu = tk.OptionMenu(self.editor_frame, self.fractal_var, *list(fractal_dict.keys()))

            # Destroy popup window  
            self.save_popup.destroy()

            # Update textbox
            self.textbox_label.configure(fg = 'black')
            self.textbox_var.set(f'Saved Lindenmayer System as\n{fractal_name}')
    
    def save_fractal_cancel_overwrite(self):
        self.save_message.configure(text = 'Enter a new name for the fractal system')
        self.save_entry.configure(state = tk.NORMAL)
        self.save_button1.configure(text = 'Done', command = lambda : self._save_fractal(overwrite = False))
        self.save_button2.configure(text = 'Cancel', command = self.save_popup.destroy)

    # TODO: IMPROVE
    def _save_image(self):
        self.screen.getcanvas().postscript(file = 'frac.eps')
        self.textbox_var.set('Saved image as frac.eps')

    # TODO: IMPROVE
    def _update_alphabet_entry(self, *_):
        # Create valid alphabet from entry
        valid_chars = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
        new_alphabet = list(dict.fromkeys([char for char in self.alphabet_var.get().upper() if char in valid_chars]))

        # Format alhpabet entry
        index = self.alphabet_entry.index(tk.INSERT)
        self.alphabet_entry.delete(0, tk.END)
        self.alphabet_entry.insert(0, ' '.join(new_alphabet))
        self.alphabet_entry.icursor(index)

        # Update axiom
        self._update_entry(self.axiom_entry, self.axiom_var, _)

        # Update production rules
        previous_rules = {}
        for i in range(len(self.production_rules)):
            character = self.production_rules[i]['char'].get()
            if character == '':
                break
            else:
                function = self.production_rules[i]['function'].get()
                rule = self.production_rules[i]['rule'].get()
                previous_rules[character] = (function, rule)
                self.production_rules[i]['char'].set('')
                self.production_rules[i]['function'].set('')
                self.production_rules[i]['rule'].set('')

        for i in range(min(len(new_alphabet), len(self.production_rules))):
            character = new_alphabet[i]
            self.production_rules[i]['char'].set(character)
            if character in previous_rules:
                self.production_rules[i]['function'].set(previous_rules[character][0])
                self.production_rules[i]['rule'].set(previous_rules[character][1])
            else:
                self.production_rules[i]['rule'].set(character)
                self.alphabet_entry.icursor(index + 1)

    # TODO: IMPROVE
    def _update_entry(self, entry : tk.Entry, var : tk.StringVar, *_):
        # Create valid axiom from entry
        valid_chars = set([char.upper() for char in self.alphabet_entry.get().replace(' ', '')])
        entry_text = list([char for char in var.get().upper() if char in valid_chars])

        # Format axiom entry
        index = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, ''.join(entry_text))
        entry.icursor(index)

    def _scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
        print('scroll start')

    def _scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        print('scroll move')

    def _mouse_scroll(self, event):
        amount = 0.9 if event.delta < 0 else 1.1
        self.canvas.scale(tk.ALL, 0, 0, amount, amount)

if __name__ == '__main__':
    gui = Window()