import tkinter as tk
from tkinter import ttk


class EntryDialog(tk.Toplevel):
    def __init__(self, parent, msg, dict_key):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent

        self.grid()
        
        self.label_field = tk.Label(self, text = msg)
        self.label_field.grid(row = 0, column = 0, padx = 10, pady = 5)
        
        self.entry_field = ttk.Entry(self, textvariable = tk.StringVar())
        self.entry_field.grid(row = 1, column = 0, padx = 10, pady = 5)
        
        self.button_ok = ttk.Button(self, text = "OK", command = lambda: self.OK(dict_key))
        self.button_ok.grid(row = 2, column = 0, padx = 10, pady = 5)
        
        self.bind('<Control-w>', self.quit)
        self.bind('<Up>', self.press_up)
        self.bind('<Down>', self.press_down)
        
        self.widgets = [self.entry_field, self.button_ok]
        for widget in self.widgets:
            widget.bind("<Return>", self.press_enter)
            
        self.entry_field.focus()
   
    def press_up(self, event = None):
        event.widget.tk_focusPrev().focus()
        
    def press_down(self, event = None):
        event.widget.tk_focusNext().focus()
        
    def press_enter(self, event = None):
        self.button_ok.invoke()
    
    def OK(self, dict_key):
        data = self.entry_field.get()
        d, key = dict_key
        d[key] = data
        self.destroy()
