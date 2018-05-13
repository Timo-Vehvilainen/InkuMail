import tkinter as tk
from tkinter import ttk
import webbrowser as web
from code.loginDialog import LoginDialog
from code.functions import compile_newsletter, get_active_folderpath, \
                            bold_new_titles, unbold_all_titles
import os
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class MainTab(ttk.Frame):
    def __init__(self, parent, newsletter):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.parent_folderpath = os.getcwd()
        
        self.newsletter = newsletter
        
        self.initialize()
        
    def initialize(self):
        self.parent.grid()
        
        #self.is_default = tk.BooleanVar()
        #self.is_default.set(True)
        
        self.label_action_text = tk.StringVar()
        self.label_action_text.set("Ready")
        self.label_action = ttk.Label(self, textvariable = self.label_action_text)
        self.label_from = ttk.Label(self, text = "From: ")
        self.label_to = ttk.Label(self, text = "To: ")
        
        self.entry_from = ttk.Entry(self, textvariable = tk.StringVar(), state = tk.DISABLED)
        self.entry_to = ttk.Entry(self, textvariable = tk.StringVar(), state = tk.DISABLED)
        
        
        self.button_compile = ttk.Button(self, text = "Compile newsletter", command = self.compile)
        
        self.button_bold = ttk.Button(self, text = "Bold new titles", command = self.bold, state = tk.DISABLED)
        self.button_unbold = ttk.Button(self, text = "Unbold all titles", command = self.unbold, state = tk.DISABLED)
        self.bolding = False
        
        self.button_preview = ttk.Button(self, text = "Preview", state = tk.DISABLED, command = self.preview)        
        self.button_login = ttk.Button(self, text = "Log in", state = tk.DISABLED, command = self.login)
        
        self.progress = tk.IntVar()
        self.progressbar = ttk.Progressbar(self, mode = "determinate", variable = self.progress, maximum = 100.01)
        
        self.button_close  = ttk.Button(self, text = "Close", command = self.quit)
        
        self.buttons = [self.button_compile, self.button_preview, self.button_login, self.button_close]
        self.entries = [self.entry_from, self.entry_to]
        self.config_widgets = self.entries
        
        for button in self.buttons:
            button.bind("<Return>", self.press_enter)

        self.setup_grid()
        self.update_fields()
        
    def setup_grid(self):
        self.label_action.grid(row = 5, column = 4, padx = 5, pady = 5)
        self.button_compile.grid(row = 5, column = 1, columnspan = 2, padx = 5, pady = 5)
        self.button_bold.grid(row = 6, column = 1, padx = 5, pady = 5)
        self.button_unbold.grid(row = 6, column = 2, padx = 5, pady = 5)
        self.button_preview.grid(row = 7, column = 1, padx = 5, pady = 5)
        self.button_login.grid(row = 7, column = 2, columnspan = 2, padx = 5, pady = 5)
        self.progressbar.grid(row = 6, column = 4, padx = 5, pady = 5)
        self.label_from.grid(row = 1, column = 0, rowspan = 2, sticky = tk.E, padx = 5, pady = 5)
        self.label_to.grid(row = 3, column = 0, rowspan = 2, sticky = tk.E, padx = 5, pady = 5)
        self.entry_from.grid(row = 1, column = 1, rowspan = 2, columnspan = 5, padx = 5, pady = 5, sticky = tk.W + tk.E)
        self.entry_to.grid(row = 3, column = 1, rowspan = 2, columnspan = 5, padx = 5, pady = 5, sticky = tk.W + tk.E)
        self.button_close.grid(row = 7, column = 5, columnspan = 2, padx = 5, pady = 5)
        
        self.grid_columnconfigure(4, weight = 1)
        self.grid_rowconfigure(5, weight = 1)
            
        
    def update_fields(self):
        addresses = [self.newsletter.get_address("from"), \
                     self.newsletter.get_address("to")]
        for i, entry in enumerate(self.entries):
            entry.config(state = tk.NORMAL)
            entry.delete(0,tk.END)
            entry.insert(0, addresses[i])
            entry.config(state = tk.DISABLED)
    
    def get_newsletter(self):
        return self.newsletter
    
    def set_newsletter(self, newsletter):
        self.newsletter = newsletter
            
    def press_enter(self, event = None):
        event.widget.invoke()
                
    def compile(self):
        self.label_action_text.set("Compiling...")
        self.label_action.update()
        self.progress.set(0)
        self.progressbar.update()
        time.sleep(0.2)
        
        self.newsletter.set_address("from", self.entry_from.get())
        self.newsletter.set_address("to", self.entry_to.get())
        
        success, compilation = compile_newsletter(self.newsletter, self.progressbar, self.bolding)
        if not success:
            tk.messagebox.showerror("Error while compiling", compilation)
            self.progress.set(0)
            self.label_action_text.set("Error while compiling!")
            self.label_action.update()
            return
        self.newsletter = compilation
        self.button_preview.config(state = tk.NORMAL)
        self.button_login.config(state = tk.NORMAL)
        self.button_bold.config(state = tk.NORMAL)
        self.button_unbold.config(state = tk.NORMAL)
        self.progressbar.step(10.0)
        self.progressbar.update()
        self.label_action_text.set("Compiled!")
        self.label_action.update()
        
    def bold(self):
        bold_new_titles(self.newsletter)
        self.bolding = True
        self.compile()
        self.bolding = False

    def unbold(self):
        self.bolding = True
        unbold_all_titles(self.newsletter)
        self.compile()
        self.bolding = False
    
    def preview(self):
        active_folderpath = self.parent_folderpath + get_active_folderpath(self.newsletter.get_newsletter_type())
        filename = "file://" + active_folderpath + "email_html_version.html"
        web.open(filename)
        
    def toggle_defaults(self, is_default):
        for widget in self.config_widgets:
            if is_default:
                widget.config(state = tk.DISABLED)
            else:
                widget.config(state = tk.NORMAL)
        
    def login(self):
        login_dialog = LoginDialog(self, self.newsletter)
        self.wait_window(login_dialog)
        #login_dialog.title("Aalto-Login")
        
        
    def quit(self, event = None):
        self.parent.quit()
    
