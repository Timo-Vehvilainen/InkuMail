import tkinter as tk
import os
import sys
from tkinter import ttk
from code.newsletter import Newsletter
from code.mainTab import MainTab
from code.advancedTab import AdvancedTab
from code.entryDialog import EntryDialog
from collections import OrderedDict
try:
    import xml.etree.cElementTree as ET
    from xml.etree.cElementTree import Element
except ImportError:
    import xml.etree.ElementTree as ET
    from xml.etree.cElementTree import Element


class MainWindow(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        
        self.initialize()
        
    def initialize(self):
        self.parent_folderpath = os.getcwd()
        
        style = ttk.Style()
        style.configure("TRadiobutton", indicatoron = 0)
        
        self.grid()
        
        self.newsletter = Newsletter()
        self.newsletter_type = tk.StringVar()
        self.newsletter_type.set("Viikkomaili")
        
        self.is_default = tk.BooleanVar()
        self.is_default.set(True)
        
        self.notebook = ttk.Notebook(self)
        
        self.checkbutton_default = ttk.Checkbutton(self, variable = self.is_default, text = "Use default config", onvalue = True, offvalue = False, command = self.toggle_default)
        self.combobox_presets = ttk.Combobox(self, state = "readonly")
        #self.combobox_presets.current(0)
        
        if not self.get_default_info(False):
            self.quit()
            
        self.main_tab = MainTab(self.notebook, self.newsletter)
        self.advanced_tab = AdvancedTab(self.notebook, self.newsletter)
        
        self.notebook.add(self.main_tab, text = "Main")
        self.notebook.add(self.advanced_tab, text = "Layout")
        
        #self.radiobutton_viikkomaili = tk.Radiobutton(self, indicatoron = 0, text = "Viikkomaili", variable = self.newsletter_type, value = "Viikkomaili", command = self.get_default_info)
        #self.radiobutton_fuksimaili = tk.Radiobutton(self, indicatoron = 0, text = "Fuksimaili", variable = self.newsletter_type, value = "Fuksimaili", command = self.get_default_info)
        #self.radiobutton_international = tk.Radiobutton(self, indicatoron = 0, text = "International", variable = self.newsletter_type, value = "International", command = self.get_default_info)
        
        self.button_new_preset = ttk.Button(self, text = "New preset...", command = self.make_preset, state = tk.DISABLED)
        self.button_set_defaults = ttk.Button(self, text = "Save preset", command = self.save_preset, state = tk.DISABLED)
        self.button_delete_preset = ttk.Button(self, text = "Delete preset", command = self.delete_preset, state = tk.DISABLED)
        
        self.toggle_default()
        
        self.notebook.enable_traversal()
        self.bind('<Control-w>', self.quit)
        self.bind('<<ComboboxSelected>>', self.select_preset)
        self.checkbutton_default.bind('<Return>', self.invoke_checkbutton)
        
        self.setup_grid()
                
    def setup_grid(self):
        self.notebook.grid(row = 2, column = 0, columnspan = 7, sticky = "nsew")
        #self.radiobutton_viikkomaili.grid(row = 0, column = 2, rowspan = 2)
        #self.radiobutton_fuksimaili.grid(row = 0, column = 3, rowspan = 2)
        #self.radiobutton_international.grid(row = 0, column = 4, rowspan = 2)
        self.checkbutton_default.grid(row = 0, column = 0)
        self.combobox_presets.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "n")
        self.button_new_preset.grid(row = 0, column = 2, rowspan = 2)
        self.button_set_defaults.grid(row = 0, column = 3, rowspan = 2)
        self.button_delete_preset.grid(row = 0, column = 4, rowspan = 2)
        
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_columnconfigure(4, weight = 1)
        self.grid_columnconfigure(5, weight = 1)
        self.grid_columnconfigure(6, weight = 1) 
         
    def select_preset(self, event = None):
        selected_preset = event.widget.get()
        self.newsletter.set_newsletter_type(selected_preset)
        self.newsletter_type.set(selected_preset)
        self.get_default_info()
        self.combobox_presets.selection_clear()
        
    def delete_preset(self, event = None):
        if tk.messagebox.askyesno("InkuMail delete preset", \
                                  "Are you sure you want to delete the preset " + \
                                  self.newsletter.get_newsletter_type() + "?"):
            #delete_archive = tk.messagebox.askokcancel("Preset deletion", \
            #                "Do you also want to delete the archives, articles and active files related to this preset?")
            info_filename = self.parent_folderpath + "/code/default_info.xml"
            try:
                tree = ET.parse(info_filename)
            except IOError as e:
                tk.messagebox.showerror("Error while reading default_info.xml", e)
            root = tree.getroot()
            
            for type in root.findall("./" + "*[@type='"+ self.newsletter.get_newsletter_type() + "']"):
                root.remove(type)
            
            #if delete_archive:
            #    os.removedirs(os.getcwd() + "/" + self.newsletter.get_newsletter_type())
            
            deleted_preset = self.presets.remove(self.newsletter.get_newsletter_type())
            self.combobox_presets.config(values = self.presets)
            self.combobox_presets.current(0)
            tree.write(info_filename, encoding = "utf-8")

            tk.messagebox.showinfo("InkuMail delete preset", "The preset "+self.newsletter_type.get()+" was deleted!")
            self.newsletter.set_newsletter_type(self.presets[0])
            
    def create_preset_directory(self, preset_name):
        print(os.getcwd() + "/" + preset_name)
        os.mkdir(os.getcwd() + "/" +  preset_name)
        os.mkdir(os.getcwd() + "/" +  preset_name + "/archive")
        os.mkdir(os.getcwd() + "/" +  preset_name + "/active")
        os.mkdir(os.getcwd() + "/" +  preset_name + "/articles")
    
    def get_default_info(self, is_initialized = True):
        info_filename = self.parent_folderpath + "/code/default_info.xml"
        try:
            tree = ET.parse(info_filename)
        except IOError as e:
            tk.messagebox.showerror("Error while reading default_info.xml", e)
            return False
        root = tree.getroot()
        if not is_initialized:
            presets_xml = root.findall("newsletter")
            self.presets = []
            for preset in presets_xml:
                self.presets.append(preset.get("type"))
            self.combobox_presets.config(values = self.presets)
            self.combobox_presets.current(0)
        self.newsletter.set_newsletter_type(self.combobox_presets.get())
        newsletter_xml = root.find("./" + "*[@type='"+ self.newsletter.get_newsletter_type() + "']")
        self.newsletter.set_address("from", newsletter_xml.find("from").text)
        self.newsletter.set_address("to", newsletter_xml.find("to").text)
        self.newsletter.set_banner(newsletter_xml.find("banner").text)
        self.newsletter.set_top_icon(newsletter_xml.find("top_icon").text)
        
        colors_xml = newsletter_xml.findall("colors/color")
        colors_dict = {}
        for color in colors_xml:
            colors_dict[color.get("target")] = color.get("value")
        self.newsletter.set_colors(colors_dict)
        
        sections_xml = newsletter_xml.findall("sections/section")
        sections_xml.sort(key = lambda x: x.get("weight"))
        sections_dict = OrderedDict()
        for section in sections_xml:
            sections_dict[section.get("name")] = section.get("color")
        self.newsletter.set_sections(sections_dict)
        
        icons_xml = newsletter_xml.findall("icons/icon")
        icons_dict = {}
        for icon in icons_xml:
            icons_dict[icon.get("target")] = icon.get("address")
        self.newsletter.set_icons(icons_dict)
        
        if is_initialized:
            self.main_tab.update_fields()
            self.advanced_tab.update_fields()
            if not self.is_default.get():
                self.checkbutton_default.invoke()
                
        return True
    
    def make_preset(self, event = None):
        dict = {"preset":""}
        msg = "Give preset name:"
        entry_dialog = EntryDialog(self, msg, (dict, "preset"))
        self.wait_window(entry_dialog)
        preset_name = dict["preset"]
        if preset_name in self.presets:
            tk.messagebox.showerror("New preset", "A preset with that name already exists!")
        elif preset_name != "":
            self.newsletter.set_newsletter_type(preset_name)
            self.presets.append(self.newsletter.get_newsletter_type())
            self.combobox_presets.config(values = self.presets)
            self.combobox_presets.current(len(self.presets) - 1)
            self.newsletter.set_newsletter_type(preset_name)
            self.create_preset_directory(preset_name)
            self.save_preset()
    
    def invoke_checkbutton(self, event = None):
        self.checkbutton_default.invoke()
        
    def toggle_default(self, event = None):
        if self.is_default.get():
            self.button_new_preset.config(state = tk.DISABLED)
            self.button_set_defaults.config(state = tk.DISABLED)
            self.button_delete_preset.config(state = tk.DISABLED)
        else:
            self.button_new_preset.config(state = tk.NORMAL)
            self.button_set_defaults.config(state = tk.NORMAL)
            self.button_delete_preset.config(state = tk.NORMAL)
        self.main_tab.toggle_defaults(self.is_default.get())
        self.advanced_tab.toggle_defaults(self.is_default.get())
        
        
    def save_preset(self):
        if tk.messagebox.askokcancel("Define preset", \
                                  "Are you sure you want to set the current parameter values as defaults for " + \
                                  self.newsletter.get_newsletter_type() + "?"):
            info_filename = self.parent_folderpath + "/code/default_info.xml"
            try:
                tree = ET.parse(info_filename)
            except IOError as e:
                tk.messagebox.showerror("Error while reading default_info.xml", e)
            root = tree.getroot()
            
            from_address = self.main_tab.entry_from.get()
            to_address = self.main_tab.entry_to.get()
            
            newsletter_xml = root.find("./" + "*[@type='"+ self.newsletter.get_newsletter_type() + "']")
            if newsletter_xml == None:
                root.append(Element("newsletter", {"type": self.newsletter.get_newsletter_type()}))
                newsletter_xml = root.find("./" + "*[@type='"+ self.newsletter.get_newsletter_type() + "']")
                newsletter_xml.append(Element("from"))
                newsletter_xml.append(Element("to"))
                newsletter_xml.append(Element("banner"))
                newsletter_xml.append(Element("top_icon"))
                newsletter_xml.append(Element("colors"))
                colors_xml = newsletter_xml.find("colors")
                for target in ["foreground", "background", "text", "intro", "outro", "link"]:
                    colors_xml.append(Element("color", {"target":target, "value":"000000"}))
                newsletter_xml.append(Element("sections"))
                newsletter_xml.append(Element("icons"))
            newsletter_xml.find("from").text = from_address
            newsletter_xml.find("to").text = to_address
            newsletter_xml.find("banner").text = self.newsletter.get_banner()
            newsletter_xml.find("top_icon").text = self.newsletter.get_top_icon()

            colors_xml = newsletter_xml.findall("colors/color")
            for color in colors_xml:
                color.set("value", self.newsletter.get_color(color.get("target"))) 
            
            sections_xml = newsletter_xml.find("sections")
            for section in sections_xml.findall("section"):
                sections_xml.remove(section)
                
            sections_dict = self.newsletter.get_sections()
            for index, section in enumerate(sections_dict):
                sections_xml.append(Element("section", {"name": section, "color": sections_dict[section], "weight": str(index)}))
            
            icons_xml = newsletter_xml.find("icons")
            for icon in icons_xml.findall("icon"):
                icons_xml.remove(icon)
            
            icons_dict = self.newsletter.get_icons()
            for icon in icons_dict:
                icons_xml.append(Element("icon", {"target": icon, "address":icons_dict[icon]}))
            
            tree.write(info_filename, encoding = "utf-8")
            tk.messagebox.showinfo("InkuMail set preset", "New preset values were set!")
            
            if not self.is_default.get():
                self.checkbutton_default.invoke()
    
    def quit(self, event = None):
        self.destroy()
        sys.exit()
        
