'''
The Section class holds all information concerning the different sections
that the articles can be divided into. The section is identified by its name, 
weight and a color.
'''

class Section:
    
    '''
    Initialiser method
        PARAMETERS:
            - The section name, as a string
            - The section weight, as an integer. 
              This number determines in which order the sections will be 
              represented. Sections with smaller weight are at the top, sections
              with more weight are at the bottom
            - The RGB color code of the section, as a hexadecimal string 
              (without a leading '#')
    '''
    def __init__(self, section_name, weight, color):
        self.__name = section_name
        self.__weight = weight
        self.__color = color
    
    '''
    get_name()
        PARAMETERS:
            - the name of the section, as a string
        RETURNS:
            - nothing
    '''
    def get_name(self):
        return self.__name
    
    '''
    get_weight()
        PARAMETERS:
            - the weight of the section, as an integer
        RETURNS:
            - nothing
    '''
    def get_weight(self):
        return self.__weight
    
    '''
    get_color()
        PAREMETERS:
            - none
        RETURNS:
            - The RGB color code of the section, as a hexadecimal string 
              (without a leading '#')
    '''
    def get_color(self):
        return self.__color
    
    '''
    set_color()
        PARAMETERS:
            - the new RGB color code of the section, as a hexadecimal string 
              (without a leading '#')
        RETURNS:
            - nothing
    '''
    def set_color(self, color):
        self.__color = color