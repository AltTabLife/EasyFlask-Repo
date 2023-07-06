#This file is not necessary, but helps organize the logic going from piece to piece to build the website as a whole

from EasyFlask.parse_yamlish import parse_yamlish
from .page_builder import PageBuilder
from .html_generator import HTMLGenerator


from pathlib import Path

def road_map(file_in):
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
    app_to_write = Path(f'output_src/app.py')
    with open(app_to_write, 'w') as app_file:
        app_string = f'''\
#Imports
from flask import Flask, render_template

#Define namespace and config
app = Flask(__name__)

#Routes
'''
        for page in pulled_pages:
            for routes in page.route_list:
                app_string += f'''@app.route("{routes}")\n'''
            app_string += f'''\
def {page.page_name}():
    return render_template("{page.page_name}.html")\n\n'''
        app_string += f'''\

if __name__ == "__main__":
    app.run(debug=True)'''
        app_file.write(app_string)



    for page in pulled_pages:
        template_to_write = Path(f'output_src/templates/{page.page_name}.html')
        with open(template_to_write, 'w') as template:
            template_string = f'''\
                {page.final_html_string}
            '''
            template.write(template_string)
