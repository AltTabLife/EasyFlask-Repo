#This file is not necessary, but helps organize the logic going from piece to piece to build the website as a whole

from EasyFlask.parse_yamlish import parse_yamlish
from .html_generator import HTMLGenerator



class RoadMap:

    def __init__(self, file_in):
        #input from source/debug build
        self.file_in = file_in
        
        #Convert to construct        
        self.data_construct = parse_yamlish(self.file_in)
        
#Pull app name and config

#Pull pages

#Pull Jinja

#Build final html
    def see_data(self):
        return self.data_construct

