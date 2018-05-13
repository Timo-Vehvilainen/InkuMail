'''
The Article class holds all the information regarding one article
within the newsletter. The article is aware of its text contents, 
its title, and which section it belongs to.
'''

class Article:
    
    '''
    Initialiser method
        PARAMETERS:
            - The section which the article belongs to, as an 
              instance of the Section class
            - The title of the article, as a string
            - The text content of the article, as a string
        RETURNS:
            - nothing
    '''
    def __init__(self, section, title, text):
        self.__section = section
        self.__title = title
        self.__text = text
     
    '''
    get_section()
        PARAMETERS:
            - none
        RETURNS:
            - the name of the section the article belongs to, as a string 
    '''
    def get_section(self):
        return self.__section.get_name()
    
    '''
    get_section_weight()
        PARAMETERS:
            - none
        RETURNS:
            - the weight of the section the article belongs to, as an integer
    '''
    def get_section_weight(self):
        return self.__section.get_weight()
    
    '''
    get_color()
        PARAMETERS:
            - none
        RETURNS:
            - the RGB color code of the section the article belongs to, 
              as a hexadecimal string (without a leading '#')
    '''
    def get_color(self):
        return self.__section.get_color()
    
    '''
    set_color()
        PARAMETERS:
            - the new RGB color code for the section of this article, as a
              hexadecimal string (without a leading '#')
        RETURNS:
            - nothing
    '''
    def set_color(self, color):
        self.__section.set_color(color)
    
    '''
    get_title()
        PARAMETERS:
            - none
        RETURNS:
            - the title of the article, as a string
    '''
    def get_title(self):
        return self.__title
    
    '''
    set_title()
        PARAMETERS:
            - the new title for the article, as a string
        RETURNS:
            - nothing
    '''
    def set_title(self, title):
        self.__title = title
    
    '''
    get_text()
        PARAMETERS:
            - none
        RETURNS:
            - the text of the article, as a string
    '''
    def get_text(self):
        return self.__text
    
    '''
    set_text()
        PARAMETERS:
            - the new text for the article, as a string
        RETURNS:
            - nothing
    '''
    def set_text(self, new_text):
        self.__text = new_text
