from code.article import Article
from code.section import Section
import copy
import collections

'''
The Newsletter class is the main class for handling and storing any information
regarding a newsletter. It is used to store the articles (including intro and
outro), the sender and recipient addresses, the different sections, and all the
different html-colors associated with the letter. The class is also aware of its
newsletter type.
'''
class Newsletter(object):
    
    '''
    Initialiser method
        PARAMETERS:
            - the newsletter type, as a string. This is used to navigate through
            the different folders for articles and archives. The type also
            determines the default sections, colors and icons.
    '''
    def __init__(self, newsletter_type = "Viikkomaili"):
        self.__newsletter_type = newsletter_type
        
        #The articles are stored in a dictionary, where the intro and outro are
        #stored separately from all the other articles. This is because of the
        #formatting differences between the different parts of the letter
        self.__articles = {"INTRO": Article(Section("INTRO", 0, "000001"), "", "")\
                           , "ARTICLES":[], \
                           "OUTRO":Article(Section("OUTRO", 1, "000000"), "", "")}
        
        #sender and recipient addresses are also stored as a dictionary
        self.addresses = {"from": "", "to": ""}
        
        #The banner image and icon for the "to the top"-image are stored a
        #a string containing thhe url address of the images
        self.banner = ""
        self.top_icon = ""
        
        #Colors and icons are stored as dictionaries. For colors, different parts
        #of the mail are used as keys (background, text etc), and RGB color codes
        #are used as values (without a leading '#').
        #For the icons, string patterns (such as '.facebook.com') are used as keys,
        #and image-urls for the urls are used as values
        self.colors = {}
        self.icons = {}
        
        #sections are stored in an ordered dictionary, where sections names are keys,
        #and the values are RGB color codes (without a leading #)
        self.sections = collections.OrderedDict()

    
    def get_newsletter_type(self):
        return self.__newsletter_type
    
    def set_newsletter_type(self, new_type):
        self.__newsletter_type = new_type
    
    def get_intro(self):
        return self.__articles["INTRO"]
    
    def get_outro(self):
        return self.__articles["OUTRO"]
    
    def get_articles(self):
        return self.__articles["ARTICLES"]
    
    def get_address(self, from_or_to):
        return self.addresses[from_or_to]
    
    def set_address(self, from_or_to, address):
        self.addresses[from_or_to] = address
    
    def get_banner(self):
        return self.banner
    
    def set_banner(self, banner):
        if banner == None:
            banner = " "
        self.banner = banner
        
    def delete_section(self, section):
        self.sections.pop(section)
        
    def add_section(self, section, color):
        self.sections[section] = color
    
    def get_sections(self):
        return self.sections
    
    def set_sections(self, sections):
        self.sections = sections
        
    def get_icons(self):
        return self.icons
    
    def get_icon(self, target):
        return self.icons[target]
    
    def set_icon(self, target, address):
        if address == None:
            address = " "
        self.icons[target] = address
         
    def set_icons(self, icons):
        self.icons = icons
        
    def delete_icon(self, target):
        self.icons.pop(target)
        
    def get_top_icon(self):
        return self.top_icon
        
    def set_top_icon(self, top_icon):
        if top_icon == None: 
            top_icon = " "
        self.top_icon = top_icon
        
    def get_colors(self):
        return self.colors
    
    def set_colors(self, colors):
        self.colors = colors
        self.get_intro().set_color(colors["intro"])
        self.get_outro().set_color(colors["outro"])
            
    def get_color(self, part, section = ""):
        
        if part in list(self.sections.keys()):
            return self.sections[part]
        elif part.lower() in ["intro", "outro"]:
            return self.__articles[part.upper()].get_color()
        elif part == "section_text":
            return self.get_section_textcolor(self.sections[section])
        else:
            return self.colors[part.lower()]
    
    def set_color(self, part, color):
        if part in list(self.sections.keys()):
            self.sections[part] = color
        elif part.lower() in ["intro", "outro"]:
            self.__articles[part.upper()].set_color(color)
        self.colors[part.lower()] = color
        
    def clear_articles(self):
        self.__articles["ARTICLES"] = []
    
    def add_article(self, section, title, text):
        
        if section.upper() == "INTRO" or section.upper() == "OUTRO":
            weight = 0
            self.__articles[section] = Article(Section(section.upper(), weight, self.get_color(section.lower())), \
                                               title, text)
        else:
            for section_name in self.sections.keys():
                if section.upper() == section_name.upper():
                    weight = list(self.sections.keys()).index(section_name)
                    self.__articles["ARTICLES"].append(Article(Section(section_name, \
                    weight, self.sections[section_name]), title, text))
                    break
            #The articles are kept sorted by their section weight
            self.__articles["ARTICLES"].sort(key=lambda x: x.get_section_weight())
            
    def get_section_textcolor(self, bg):
        if int(bg, 16) < (int("ffffff", 16) / 2):
            return "#ffffff"
        else:
            return "#000000"
        
    def copy(self):
        temp_newsletter = Newsletter(self.__newsletter_type)
        temp_newsletter.set_sections(self.sections)
        for article in self.get_articles() + [self.get_intro(), self.get_outro()]:
            temp_newsletter.add_article(article.get_section(), article.get_title(), article.get_text())          
        return temp_newsletter
