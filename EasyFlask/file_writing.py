import pathlib

class FileWriting:
    def __init__(self, output_directory, pulled_pages):
        self.output_directory = output_directory
        self.pulled_pages = pulled_pages

    def create_folders(self):
        create_directory = pathlib.Path(f'{self.output_directory}/templates')
        if not create_directory.is_dir() and not create_directory.exists():
            create_directory.mkdir(parents=True, exist_ok=True)
        
        css_directory = pathlib.Path(f'{self.output_directory}/static/css')
        if not css_directory.is_dir() and not css_directory.exists():
            css_directory.mkdir(parents=True, exist_ok=True)

        images_directory = pathlib.Path(f'{self.output_directory}/static/images')
        if not images_directory.is_dir() and not images_directory.exists():
            images_directory.mkdir(parents=True, exist_ok=True)
        

    def write_app(self):
        app_to_write = pathlib.Path(f'{self.output_directory}/app.py')
        with open(app_to_write, 'w') as app_file:
            app_string = f'''\
#Imports
from flask import Flask, render_template

#Define namespace and config
app = Flask(__name__)

#Routes
'''
            for page in self.pulled_pages:
                for routes in page.route_list:
                    app_string += f'''@app.route("{routes}")\n'''
                app_string += f'''\
def {page.page_name}():
    return render_template("{page.page_name}.html")\n\n'''
            app_string += f'''\

if __name__ == "__main__":
    app.run(debug=True)'''
            app_file.write(app_string)

    def write_pages(self):
        for page in self.pulled_pages:
            template_to_write = pathlib.Path(f'output_src/templates/{page.page_name}.html')
            with open(template_to_write, 'w') as template:
                template_string = f'''{page.final_html_string}'''
                template.write(template_string)

    def write_all(self):
        self.create_folders()
        self.write_app()
        self.write_pages()
