#This file is not necessary, but helps organize the logic going from piece to piece to build the project website as a whole

from .parse_yamlish import parse_yamlish

from .page_builder import PageBuilder
from .html_generator import HTMLGenerator
from .file_writing import FileWriting


def full_road_map(file_in, output_dir):
    #input from source/debug build
    
    
    #Convert to construct        
    data_construct = parse_yamlish(file_in)
        
    #Pull app name and config
    
    #Pull pages
    #Need to for loop through creating objects for each page, ideally inside the page_builder.py, returning one object with multiple subclasses.
    
    pulled_pages = PageBuilder().build_pages(data_construct) #array of pages

    
    #Pull Jinja
    #Check for jinja extensions/inclusions and pair classes together


    #Build final html
    
    for pages in pulled_pages:
        pages.final_html_string = HTMLGenerator().generate_html(pages.html_construct)
    

    #Write to files
    f = FileWriting(f'{output_dir}', pulled_pages)
    f.write_all()


