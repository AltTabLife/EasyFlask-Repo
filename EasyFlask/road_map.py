#This file is not necessary, but helps organize the logic going from piece to piece to build the website as a whole

from EasyFlask.parse_yamlish import parse_yamlish
from .page_builder import PageBuilder
from .html_generator import HTMLGenerator


def road_map(file_in):
    #input from source/debug build
    
    
    #Convert to construct        
    data_construct = parse_yamlish(file_in)
        
    #Pull app name and config
    
    #Pull pages
    #Need to for loop through creating objects for each page, ideally inside the page_builder.py, returning one object with multiple subclasses.
    
    pulled_pages = PageBuilder().build_pages(data_construct)

    #Pull Jinja
    #Check for jinja extensions/inclusions and pair classes together
        
    #Build final html
    
    #pull the final page classes from jinja, and create the html.
    final_html = HTMLGenerator().generate_html(pulled_pages.html_construct)    
    return final_html


