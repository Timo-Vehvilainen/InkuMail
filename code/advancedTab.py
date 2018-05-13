import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from collections import OrderedDict
from code.entryDialog import EntryDialog
import time
import os

'''
AdvancedTab class represents the UI frame for the advanced section of the
InkuMail interface.
'''
class AdvancedTab(ttk.Frame):

    '''
    Initializer method
        PARAMETERS:
            - the parent tk object
            - the newsletter object that is currently active
    '''
    def __init__(self, parent, newsletter):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent_folderpath = os.getcwd()
        
        self.newsletter = newsletter
        self.initialize()
        
    '''
    initialize()
    This method sets up all the different widgets for the frame.
    '''
    def initialize(self):
        
        #'Set banner' -button and entry screen
        self.text_button_banner = tk.StringVar()
        self.text_button_banner.set("Set banner address")
        self.button_banner = ttk.Button(self, textvariable = self.text_button_banner, command = self.set_banner)
        self.entry_banner = ttk.Entry(self, textvariable = tk.StringVar())
        
        #'Set top-icon' -button and entry screen
        self.text_button_top_icon = tk.StringVar()
        self.text_button_top_icon.set("Set top-icon image")
        self.button_top_icon = ttk.Button(self, textvariable = self.text_button_top_icon, command = self.set_top_icon)
        self.entry_top_icon = ttk.Entry(self, textvariable = tk.StringVar())
        
        #Listboxes:
        #    newsletter colors
        self.listbox_colors = tk.Listbox(self, selectmode = tk.SINGLE, exportselection = 0, height = 6)
        self.label_color = ttk.Label(self, width = 10, anchor = tk.CENTER)
        self.button_set_color = ttk.Button(self, text = "Set color", command = lambda: self.set_color(self.listbox_colors))
        
        
        #    sections and their colors
        self.listbox_sections = tk.Listbox(self, selectmode = tk.SINGLE, height = 6, exportselection = 0)
        self.scrollbar_sections = tk.Scrollbar(self, orient = tk.VERTICAL, command = self.listbox_sections.yview)
        self.listbox_sections.config(yscrollcommand = self.scrollbar_sections.set)
        self.button_delete_section = ttk.Button(self, text = "Delete section", command = lambda: self.delete_list_item(self.listbox_sections))
        
        
        self.label_sectioncolor = ttk.Label(self,  width = 10, anchor = tk.CENTER)
        self.button_set_sectioncolor = ttk.Button(self, text = "Set section color", command = lambda: self.set_color(self.listbox_sections))
        self.button_add_section = ttk.Button(self, text = "Add new section", command = lambda: self.add_list_item(self.listbox_sections))
        
        #    icons and their patterns
        self.listbox_icons = tk.Listbox(self, selectmode = tk.SINGLE, exportselection = 0, height = 6)
        self.scrollbar_icons = tk.Scrollbar(self, orient = tk.VERTICAL, command = self.listbox_icons.yview)
        self.listbox_icons.config(yscrollcommand = self.scrollbar_icons.set)
        self.button_delete_icon = ttk.Button(self, text = "Delete icon", command = lambda: self.delete_list_item(self.listbox_icons))
        
        self.entry_icon = ttk.Entry(self, textvariable = tk.StringVar())
        self.text_button_set_icon = tk.StringVar()
        self.text_button_set_icon.set("Set icon address")
        self.button_set_icon_address = ttk.Button(self, textvariable = self.text_button_set_icon, command = self.set_icon)
        self.button_add_icon = ttk.Button(self, text = "Add new icon", command = lambda: self.add_list_item(self.listbox_icons))
        
        #Aesthetic widgets
        self.separator1 = ttk.Separator(self, orient = tk.VERTICAL)
        self.separator2 = ttk.Separator(self, orient = tk.VERTICAL)
        self.separator3 = ttk.Separator(self, orient = tk.HORIZONTAL)
        self.sizegrip = ttk.Sizegrip(self)
        
        #All the listboxes are also stored in a collective list
        self.boxes = [self.listbox_colors, self.listbox_sections, self.listbox_icons]
        
        #bind keyboard actions to the listboxes
        for box in self.boxes:
            box.bind("<<ListboxSelect>>", self.update_labels)
            box.bind("<Up>", self.select_previous)
            box.bind("<Down>", self.select_next)
        
        #This variable indicates wether the "Use defaults" -checkbox is currently checked
        self.is_default = tk.BooleanVar()
        self.is_default.set(True)
        
        #Place thee widgets in the frame
        self.setup_grid()
        
        #All the configurable widgets are also stored in a collective list
        self.config_widgets = [self.button_banner, self.entry_banner, \
                               self.button_top_icon, self.entry_top_icon, \
                               self.button_set_color, self.button_set_sectioncolor, \
                               self.button_delete_section, \
                               self.button_add_section, self.button_delete_icon, \
                               self.entry_icon, self.button_add_icon, \
                               self.button_set_icon_address]
         
        #bind keyboard actions to all the widgets
        for widget in self.config_widgets:
            widget.bind("<Return>", self.press_enter)
            
        #Get all the content to the different fields via the update-function
        self.update_fields() 
             
    '''
    setup_grid()
    This function places all the different widgets in the grid of the frame
        PARAMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def setup_grid(self):
        self.grid()
        
        #'Set banner' -button and entry screen
        self.button_banner.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.entry_banner.grid(row = 0, column = 2, columnspan = 6, padx = 5, sticky = "ew")
        
        #'Set top-icon' -button and entry screen
        self.button_top_icon.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.entry_top_icon.grid(row = 1, column = 2, columnspan = 6, padx = 5, sticky = "ew")
        
        #horizontal separator
        self.separator3.grid(row = 2, column = 0, columnspan = 6, padx = 5, pady = 5, sticky = "ew")
        
        #newsletter color widgets
        self.listbox_colors.grid(row = 3, column = 0)
        self.label_color.grid(row = 4, column = 0)
        self.button_set_color.grid(row = 5, column = 0, padx = 5, pady = 5)
        
        #vertical separator
        self.separator1.grid(row = 3, column = 1, rowspan = 5, padx = 10, sticky = "ns")
        
        #section widgets
        self.listbox_sections.grid(row = 3, column = 2)
        self.scrollbar_sections.grid(row = 3, column = 3, sticky = "ns")
        self.label_sectioncolor.grid(row = 4, column = 2)
        self.button_set_sectioncolor.grid(row = 5, column = 2, padx = 5, pady = 5)
        self.button_add_section.grid(row = 6, column = 2, padx = 5, pady = 5)
        self.button_delete_section.grid(row = 7, column = 2, padx = 5, pady = 5)
        
        #vertical separator
        self.separator2.grid(row = 3, column = 4, rowspan = 5, padx = 10, sticky = "ns")
        
        #icon widgets
        self.listbox_icons.grid(row = 3, column = 5)
        self.scrollbar_icons.grid(row = 3, column = 6, sticky = "ns")
        self.entry_icon.grid(row = 4, column = 5, columnspan = 3, padx = 5, sticky = "ew")
        self.button_set_icon_address.grid(row = 5, column = 5,  padx = 5, pady = 5)
        self.button_add_icon.grid(row = 6, column = 5, padx = 5, pady = 5)
        self.button_delete_icon.grid(row = 7, column = 5, padx = 5, pady = 5)
        self.sizegrip.grid(row = 8, column = 7, sticky = "es")
        
        #Make it so that the Sizegrip-widgets sticks to the corner, and that the
        #entry fields stretch when the window is resized
        self.grid_columnconfigure(7, weight = 1)
        self.grid_rowconfigure(8, weight = 1)
    
    '''
    update_fields()
    This function updates all the various fields in the widgets to represent 
    the state of the inner variables of the Newsletter object.
        PARAMETERS:
            - optional Tkinter event variable, which is generated anytime a bind-command
              is executed
        RETURNS:
            - nothing
    '''
    def update_fields(self, event = None):
        #Update the banner entry field
        self.entry_banner.config(state = tk.NORMAL)
        self.entry_banner.delete(0, tk.END)
        self.entry_banner.insert(0, self.newsletter.get_banner())
        self.entry_banner.update()
        #    if the entry field is too small, show the end of the url rather than the beginning
        self.entry_banner.xview_moveto(1)
        
        #Update the top icon entry field
        self.entry_top_icon.config(state = tk.NORMAL)
        self.entry_top_icon.delete(0, tk.END)
        self.entry_top_icon.insert(0, self.newsletter.get_top_icon())
        self.entry_top_icon.update()
        #    if the entry field is too small, show the end of the url rather than the beginning
        self.entry_top_icon.xview_moveto(1)
        
        #If "use defaults" is checked, disable the entry fields
        if self.is_default.get():
            self.entry_banner.config(state = tk.DISABLED)
            self.entry_top_icon.config(state = tk.DISABLED)
        
        #Get the values of the various dictionaries represented by listboxes
        box_values = {self.listbox_colors : self.newsletter.get_colors(), \
                    self.listbox_sections : self.newsletter.get_sections(), \
                       self.listbox_icons : self.newsletter.get_icons()}
        
        #Update the listbox values
        for box in box_values:
            box.delete(0, box.size() - 1)
            for index, value in enumerate(list(box_values[box].keys())):
                box.insert(index, value)
            box.select_set(0)
        
        #Update labels also
        self.update_labels()
    
    '''
    update_labels()
    This method updates the labels for the color- and section listboxes
        PARAMETERS:
            - and optional Tkinter event variable, for bindings
        RETURNS:
            - nothing
    '''
    def update_labels(self, event = None):
        label_values = {self.label_color: self.selection(self.listbox_colors), \
                        self.label_sectioncolor : self.selection(self.listbox_sections)}
        for label in label_values:
            color = self.newsletter.get_color(label_values[label])
            fg_color = self.get_label_fgcolor(color)
            label.config(background = "#" + color, foreground = fg_color, text = color)
        
        self.entry_icon.config(state = tk.NORMAL)
        self.entry_icon.delete(0, tk.END)
        target = self.listbox_icons.get(self.listbox_icons.curselection()[0])
        self.entry_icon.insert(0, self.newsletter.get_icon(target))
        self.entry_icon.update()
        self.entry_icon.xview_moveto(1)
        if self.is_default.get():
            self.entry_icon.config(state = tk.DISABLED)
        
    '''
    press_enter()
    this method handles the return-bindings on the interface
        PARAMETERS:
            - optiona Tkinter event object
        RETURNS:
            - nothing
    '''
    def press_enter(self, event = None):
        event.widget.invoke()
        
    '''
    selection()
    This method is used to get the current selection of a given listbox
        PARAMETERS:
            - the listbox object, the current selection of which is desired
        RETURNS:
            - the current selected value of the listbox, as an integer
    '''
    def selection(self, box): 
        return box.get(box.curselection()[0])
        
    '''
    get_label_fgcolor()
    This method figures out what color a label text should be for best readability, 
    depending on the label color. If the label is darker than 50% gray, 
    the text should be white. Otherwise, it should be black.
        PARAMETERS:
            - RGB color code for the background of the label, without a leading '#'
        RETURNS:
            - the RGB color code for the text of the label, with a leading '#'
    '''
    def get_label_fgcolor(self, bg):
        if int(bg, 16) < (int("ffffff", 16) / 2):
            return "#ffffff"
        else:
            return "#000000"
        
    '''
    delete_list_item_bind()
    This method is used as an intermediary between the bind commands and the 
    delete_list_item() function.
        PARAMETERS:
            - the event object, which is received from the bind command
        RETURNS:
            - nothing
    '''
    def delete_list_item_bind(self, event):
        self.delete_list_item(event.widget)
        
    '''
    delete_list_item()
    Deletes the currently selected item from a listbox, and modifies the 
    Newsletter object to correspond with the deletion.
        PARAMETERS:
            - the listbox to be modified
        RETURNS:
            - nothing
    '''
    def delete_list_item(self, box):
        if box == self.listbox_sections:
            self.newsletter.delete_section(self.selection(box))
        elif box == self.listbox_icons:
            self.newsletter.delete_icon(self.selection(box))
        else:
            return
        deleted_index = box.curselection()[0]
        box.delete(deleted_index)
        if box.size() != 0:
            box.select_set(min(box.size() - 1, int(deleted_index)))
        self.update_labels()
    
    '''
    add_list_item()
    Adds a new item to a listbox. The new item value is retrieved from the entry
    field of the corresponding listbox. This modification is forwarded to the 
    Newsletter object, and new key is created in its dictionaries, carrying
    default placeholder values.
        PARAMETERS:
            - the listbox object to be modified
        RETURNS:
            - nothing
    '''
    def add_list_item(self, box):
        dict = {"item":""}
        if box == self.listbox_sections:
            msg = "Give section name:"
            entryDialog = EntryDialog(self, msg, (dict, "item"))
            self.wait_window(entryDialog)
            new_name = dict["item"]
            if new_name != "" and new_name not in list(self.newsletter.get_sections().keys()):
                self.listbox_sections.insert(self.listbox_sections.size(), new_name)
                self.newsletter.add_section(new_name, "000000")
        elif box == self.listbox_icons:
            msg = "Give icon pattern:"
            entryDialog = EntryDialog(self, msg, (dict, "item"))
            self.wait_window(entryDialog)
            new_name = dict["item"]
            if new_name != "" and new_name not in list(self.newsletter.get_icons().keys()):
                self.listbox_icons.insert(self.listbox_icons.size(), new_name)
                self.newsletter.set_icon(new_name, "ICON IMAGE URL HERE")
        
    '''
    select_next()
    Moves the selection on the active listbox one forwards. This is mainly called
    when the down-arrow is pressed.
        PARAMETERS:
            - the Tkinter event object from the bind command
        RETURNS:
            - nothing
    '''
    def select_next(self, event):   
        box = event.widget
        curselection = int(box.curselection()[0])
        box.select_clear(0, box.size()-1)
        box.select_set(min(box.size() - 1, curselection + 1))
        self.update_labels(event)
        
    '''
    select_previous()
    Moves the selection on the active listbox one forwards. This is mainly called
    when the up-arrow is pressed.
        PARAMETERS:
            - the Tkinter event object from the bind command
        RETURNS:
            - nothing
    '''
    def select_previous(self, event):
        box = event.widget
        curselection = int(box.curselection()[0])
        box.select_clear(0, box.size()-1)
        box.select_set(max(0, curselection - 1))
        self.update_labels(event)
       
    '''
    set_banner()
    Sets the text that is currently in the banner entry field as the banner url
    in the Newsletter object. This is called when the 'Set banner' button is pressed.
        PARAMETERS:
            - none
        RETURNS:
            - none
    '''
    def set_banner(self):
        self.text_button_banner.set("Setting new banner...")
        self.button_banner.update()
        time.sleep(0.5)
        self.newsletter.set_banner(self.entry_banner.get())
        self.text_button_banner.set("New banner was set!")
        self.button_banner.update()
        time.sleep(1.0)
        self.text_button_banner.set("Set banner address")
        
    '''
    set_top_icon()
    Sets the text that is currently in the banner entry field as the top-icon url
    in the Newsletter object. This is called when the 'Set top-icon' button is pressed.
        PARAMETERS:
            - none
        RETURNS:
            - none
    '''
    def set_top_icon(self):
        self.text_button_top_icon.set("Setting new icon...")
        self.button_top_icon.update()
        time.sleep(0.5)
        self.newsletter.set_top_icon(self.entry_top_icon.get())
        self.text_button_top_icon.set("New icon was set!")
        self.button_top_icon.update()
        time.sleep(1.0)
        self.text_button_top_icon.set("Set top-icon image")
    
    '''
    set_icon()
    This sets the value of the current text in the icon entry field as the value of
    the selected icon in the listbox
        PARAMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def set_icon(self):
        self.text_button_set_icon.set("Setting icon address...")
        self.button_set_icon_address.update()
        time.sleep(0.5)
        self.newsletter.set_icon(self.selection(self.listbox_icons), self.entry_icon.get())
        self.text_button_set_icon.set("Icon address was set!")
        self.button_set_icon_address.update()
        time.sleep(1.0)
        self.text_button_set_icon.set("Set icon address")
        
    '''
    set_color()
    This method is used to select a new color for a currently selected section 
    or an html element of the newsletter.
        PARAMETERS: 
            - the listbox object to be modified
        RETURNS:
            - nothing
    '''
    def set_color(self, box):
        color = colorchooser.askcolor()
        if color[1] != None:
            hex_color = color[1][1:]
            self.newsletter.set_color(self.selection(box), hex_color)
            fg_color = self.get_label_fgcolor(hex_color)
            if box == self.listbox_colors:
                self.label_color.config(background = color[1], foreground = fg_color, text = hex_color)
            elif box == self.listbox_sections:
                self.label_sectioncolor.config(background = color[1], foreground = fg_color, text = hex_color)
    
    '''
    toggle_defaults()
    This function is supposed to be triggered when the "Use defaults" checkbox
    is either ticked or unticked. It either enables of disables various buttons
    and entries in the interface.
        PARAMETERS:
            - a boolean value, indicating if the "use defaults" checkbox is ticked
        RETURNS:
            - nothing
    '''
    def toggle_defaults(self, is_default):
        self.is_default.set(is_default)
        if is_default:
            for widget in self.config_widgets:
                widget.config(state = tk.DISABLED)
            self.listbox_sections.unbind("<B1-Motion>")
            self.listbox_sections.unbind("<Shift-Up>")
            self.listbox_sections.unbind("<Shift-Down>")
            self.listbox_sections.unbind("<Delete>")
            self.listbox_icons.unbind("<Delete>")
        else:
            for widget in self.config_widgets:
                widget.config(state = tk.NORMAL)
            self.listbox_sections.bind("<B1-Motion>", self.shift_selection)
            self.listbox_sections.bind("<Shift-Up>", self.shift_selection)
            self.listbox_sections.bind("<Shift-Down>", self.shift_selection)
            self.listbox_sections.bind("<Delete>", self.delete_list_item_bind)
            self.listbox_icons.bind("<Delete>", self.delete_list_item_bind)

    '''
    shift_selection()
    This function is used to change the order of the items in the section listbox.
    This can either be done with Shift+Up, Shift+Down, or by dragging items with 
    the mouse. The Newsletter object is also updated to have to corresponding order.
        PARAMETERS:
            - the event object from the bind command
        RETURNS:
            - nothing
            
    '''
    def shift_selection(self, event):
        box = event.widget
        sectionIndex = int(box.curselection()[0])
        
        #identify whether the event is a keypress or a mouse movement
        if event.keysym == "Down":
            shift = min(sectionIndex + 1, box.size() - 1)
        elif event.keysym == "Up":
            shift = max(sectionIndex - 1, 0)
        else:
            shift = box.nearest(event.y)
        
        #shift the selection up or down
        if shift < sectionIndex:
            x = box.get(shift)
            box.delete(shift)   
            box.insert(shift+1, x)
        elif shift > sectionIndex:
            x = box.get(shift)
            box.delete(shift)
            box.insert(shift-1, x)
            
        #update the sections dictionary in the Newsletter object
        sections_dict = OrderedDict()
        for section in range(0, self.listbox_sections.size()):
            color = self.newsletter.get_color(self.listbox_sections.get(section))
            sections_dict[self.listbox_sections.get(section)] = color
        self.newsletter.set_sections(sections_dict)
